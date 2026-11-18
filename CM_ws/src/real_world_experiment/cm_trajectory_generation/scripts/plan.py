#!/usr/bin/env python3

import argparse
import datetime
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import yaml

RANDOM_SEED = 20260728


def workspace_path():
    if os.environ.get('CM_WORKSPACE'):
        candidates = [Path(os.environ['CM_WORKSPACE']).expanduser().resolve()]
    else:
        candidates = list(Path(__file__).resolve().parents)
    for candidate in candidates:
        if (candidate / 'src/real_world_experiment/cm_trajectory_generation').is_dir():
            return candidate
    raise ValueError('Set CM_WORKSPACE to the built source workspace')


def path_value(workspace, value):
    if not value:
        raise ValueError('Required path is empty; edit config/offline.yaml')
    path = Path(value).expanduser()
    return (path if path.is_absolute() else workspace / path).resolve()


def input_file(workspace, value):
    path = path_value(workspace, value)
    if not path.is_file():
        raise ValueError('Missing input: {}'.format(path))
    return path


def positive(value, name, integer=False):
    number = float(value)
    if not math.isfinite(number) or number <= 0 or (integer and int(number) != number):
        raise ValueError('{} must be positive{}'.format(name, ' integer' if integer else ''))
    return int(number) if integer else number


def check_settings(workspace, config, name):
    settings = config['objects'][name]
    runtime, family = settings['runtime'], settings['family']
    if runtime != 'sim' or family != 'ball':
        raise ValueError('{} requires runtime=sim and family=ball'.format(name))
    phases = settings['phases']
    if not isinstance(phases, list) or not phases or len(set(phases)) != len(phases):
        raise ValueError('phases must be a nonempty list without duplicates')
    if any(phase not in ('catch', 'move') for phase in phases):
        raise ValueError('phases may contain only catch and move')
    if phases != ['catch', 'move']:
        raise ValueError('The simulation planner generates both phases; use [catch, move]')
    positive(config['planning']['max_iterations'], 'planning.max_iterations', True)
    positive(config['planning']['timeout_s'], 'planning.timeout_s')
    for phase in phases:
        scene_value = settings['sim_scenes'].get(phase)
        if not scene_value:
            raise ValueError('Empty objects.{}.{}_scenes.{} in config/offline.yaml'.format(name, runtime, phase))
        source = input_file(workspace, scene_value)
        scene = yaml.safe_load(source.read_text(encoding='utf-8'))
        model = scene['file_path']['pinocchio_file'].replace(
            '/home/mas-2/3rd_party/CM_ws/', workspace.as_posix() + '/')
        input_file(workspace, model)
    return settings


def relocated(value, workspace):
    if isinstance(value, dict):
        return {key: relocated(item, workspace) for key, item in value.items()}
    if isinstance(value, list):
        return [relocated(item, workspace) for item in value]
    if isinstance(value, str):
        return value.replace('/home/mas-2/3rd_party/CM_ws/', workspace.as_posix() + '/')
    return value


def snapshot_scene(source, workspace, output, phase):
    scene = relocated(yaml.safe_load(source.read_text(encoding='utf-8')), workspace)
    model = input_file(workspace, scene['file_path']['pinocchio_file'])
    model_copy = output / (phase + '_scene.urdf')
    model_copy.write_text(relocated(model.read_text(encoding='utf-8'), workspace), encoding='utf-8')
    scene['file_path']['pinocchio_file'] = str(model_copy)
    for section in ('planned_path', 'kirara_path'):
        scene[section] = {side: str(output / (phase + '_' + side + '_' + section + '.txt'))
                          for side in ('left', 'right')}
    if 'goal_generator' in scene:
        scene['goal_generator']['output_file'] = str(output / (phase + '_goal_generator.yaml'))
        scene['goal_generator']['debug_file'] = str(output / (phase + '_goal_generator.log'))
    destination = output / (phase + '_scene.yaml')
    destination.write_text(yaml.safe_dump(scene, sort_keys=False), encoding='utf-8')
    return destination


def run_pipeline(workspace, config, name, settings, output, execute):
    binary = workspace / 'devel/lib'
    plan = config['planning']
    scenes = {phase: snapshot_scene(input_file(workspace, settings['sim_scenes'][phase]),
                                     workspace, output, phase) for phase in ('catch', 'move')}
    execute([binary / 'cm_trajectory_generation' / 'generate_socket_ball_plan.py',
             '--workspace', workspace, '--output-dir', output / 'paths',
             '--catch-config', scenes['catch'], '--move-config', scenes['move'],
             '--seed', RANDOM_SEED,
             '--max-iterations', plan['max_iterations'], '--timeout', plan['timeout_s'],
             '--no-update-latest'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('object', nargs='?', choices=('simball',), default='simball')
    parser.add_argument('--config', type=Path)
    parser.add_argument('--check', action='store_true', help='validate inputs without planning')
    args = parser.parse_args()
    try:
        name = args.object
        workspace = workspace_path()
        source = args.config or workspace / 'src/real_world_experiment/cm_trajectory_generation/config/offline.yaml'
        config = yaml.safe_load(source.read_text(encoding='utf-8'))
        settings = check_settings(workspace, config, name)
        print('Object: {} | runtime: {} | phases: {}'.format(name, settings['runtime'], settings['phases']))
        if args.check:
            print('Inputs checked; no planning or hardware commands executed.')
            return
        output = path_value(workspace, config['output_root']) / (
            name + '_' + settings['runtime'] + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        output.mkdir(parents=True, exist_ok=False)
        (output / 'settings.yaml').write_text(yaml.safe_dump(config, sort_keys=False), encoding='utf-8')
        env = os.environ.copy()
        env['CM_WORKSPACE'] = str(workspace)
        commands = []
        def execute(command):
            command = [str(item) for item in command]
            commands.append(command)
            (output / 'commands.json').write_text(json.dumps(commands, indent=2), encoding='utf-8')
            print('Running: {}'.format(Path(command[0]).name), flush=True)
            subprocess.run(command, check=True, env=env)
        status = {'object': name, 'runtime': settings['runtime'], 'status': 'running'}
        try:
            run_pipeline(workspace, config, name, settings, output, execute)
            status['status'] = 'completed'
        except BaseException as exc:
            status.update(status='failed', error=str(exc))
            raise
        finally:
            (output / 'status.json').write_text(json.dumps(status, indent=2), encoding='utf-8')
            print('Results: {}'.format(output), flush=True)
    except (ValueError, KeyError, OSError, EOFError, yaml.YAMLError, subprocess.CalledProcessError) as exc:
        parser.exit(2, 'Offline planning stopped: {}\n'.format(exc))


if __name__ == '__main__':
    main()
