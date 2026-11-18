#!/usr/bin/env python3

from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
import pinocchio as pin
import yaml


def origin_transform(joint):
    origin = joint.find('origin')
    xyz = (np.fromstring(origin.get('xyz', '0 0 0'), sep=' ')
           if origin is not None else np.zeros(3))
    rpy = (np.fromstring(origin.get('rpy', '0 0 0'), sep=' ')
           if origin is not None else np.zeros(3))
    transform = np.eye(4)
    transform[:3, :3] = pin.rpy.rpyToMatrix(rpy)
    transform[:3, 3] = xyz
    return transform


def reach_sphere(urdf, tip):
    by_child = {joint.find('child').get('link'): joint
                for joint in ET.parse(urdf).getroot().findall('joint')}
    chain = []
    while tip in by_child:
        joint = by_child[tip]
        chain.append(joint)
        tip = joint.find('parent').get('link')
    if tip != 'world':
        raise ValueError('tool chain must start at world')
    transform = np.eye(4)
    center = None
    radius = 0.0
    for joint in reversed(chain):
        if joint.get('type') not in ('fixed', 'revolute', 'continuous'):
            raise ValueError('unsupported joint type in arm chain')
        origin = origin_transform(joint)
        if center is None:
            transform = transform @ origin
            if joint.get('type') != 'fixed':
                center = transform[:3, 3].copy()
        else:
            radius += np.linalg.norm(origin[:3, 3])
    if center is None:
        raise ValueError('arm chain has no movable joint')
    return center, float(radius)


def prepare_config(source, destination, random_seed):
    config = yaml.safe_load(Path(source).read_text())
    goal = config['goal_generator']
    model_file = config['file_path']['pinocchio_file']
    model = pin.buildModelFromUrdf(model_file)
    tips = [goal.get(side + '_tip', side + '_tool0')
            for side in ('left', 'right')]
    low, high = float(goal['distance_min']), float(goal['distance_max'])
    if not 0.0 < low < high:
        raise ValueError('invalid grasp-distance bounds')
    margin = min(0.0005, (high - low) / 4.0)
    axis_seed = np.array([0.0, 1.0, 0.0])
    distance_seed = (low + high) / 2.0
    if 'ik_seed_pair' in goal:
        seed = np.asarray(goal['ik_seed_pair'], dtype=float)
        if seed.shape != (12,) or not np.all(np.isfinite(seed)):
            raise ValueError('ik_seed_pair must contain 12 finite values')
        q = pin.neutral(model)
        q[:12] = seed
        data = model.createData()
        pin.framesForwardKinematics(model, data, q)
        positions = [data.oMf[model.getFrameId(tip)].translation.copy()
                     for tip in tips]
        delta = positions[1] - positions[0]
        distance = float(np.linalg.norm(delta))
        if distance > 1.0e-9:
            axis_seed = delta / distance
        distance_seed = (distance if low < distance < high else
                         float(np.clip(distance, low + margin, high - margin)))
    center = np.array([goal['target'][axis] for axis in ('x', 'y', 'z')])
    center += np.array([goal.get('target_offset', {}).get(axis, 0.0)
                        for axis in ('x', 'y', 'z')])
    bounds = [reach_sphere(model_file, tip) for tip in tips]
    rng = np.random.default_rng(random_seed)
    candidates = []
    for index in range(max(1, int(goal.get('axis_samples', 36)))):
        if index == 0:
            axis = axis_seed.copy()
        elif index == 1:
            axis = np.array([0.0, 1.0, 0.0])
        else:
            axis = axis_seed + 0.25 * rng.standard_normal(3)
            axis /= np.linalg.norm(axis)
        distance = (distance_seed if index < 2 else
                    float(rng.uniform(low + margin, high - margin)))
        points = [center - 0.5 * distance * axis,
                  center + 0.5 * distance * axis]
        tolerance = float(goal.get('ik_position_tolerance', 1.0e-4))
        if any(np.linalg.norm(point - bound[0]) > bound[1] + tolerance
               for point, bound in zip(points, bounds)):
            continue
        candidates.append([*axis.tolist(), distance])
    if not candidates:
        raise ValueError('no grasp-axis candidates within arm reach')
    goal['axis_candidates'] = candidates
    goal['preserve_right_world_pose'] = False
    destination = Path(destination)
    destination.write_text(yaml.safe_dump(config, sort_keys=False))
    return destination
