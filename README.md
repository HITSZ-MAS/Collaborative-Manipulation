# Collaborative Manipulation with Dual Arms in Narrow Spaces

<!-- <p align="center"><strong>A visual project page for safe, coordinated dual-arm grasping and transport in constrained workspaces.</strong></p> -->

**Installation and startup:** [Setup](#setup).

## Overview

**Experiment video:** [Watch the experiments on Bilibili](https://www.bilibili.com/video/BV1Cusw63Er7/?share_source=copy_web&vd_source=dce2a2149e6063f99b6cbe6f605aab9a).

This work focuses on dual-arm manipulation in narrow spaces. It combines a trajectory generation algorithm, a distributed nonlinear model predictive control (DNMPC) algorithm, and a bilateral position-force control algorithm with adaptive impedance. Simulations utilize a ball and a box to validate the algorithms.
The real-world experiments cover grasping, transporting, placing, and rotating targets with different elastic properties.


<!-- ### Main contributions

- A rapid trajectory-generation method that jointly satisfies collision-avoidance, kinematic, and task constraints while maintaining spatio-temporal consistency.
- A distributed NMPC controller that coordinates both arms through predicted-state exchange.
- A bilateral position-force controller with adaptive impedance for explicit internal-force regulation across targets with different stiffness. -->

**Keywords:** dual arms, trajectory generation, distributed nonlinear model predictive control, position-force control.


### Grasp and transport phases
<p align="center">
  <img src="assets/paper/Grasp3.png" alt="Manipulation phase 1" width="49%">
  <img src="assets/paper/Trasnport3.png" alt="Manipulation phase 2" width="49%">
</p>

### Coordinate system

<p align="center">
  <img src="assets/paper/coordinate-system.png" alt="Dual-arm coordinate system" width="40%">
</p>

## Algorithm design

<p align="center">
  <img src="assets/paper/systemV9.png" alt="Overview of the proposed dual-arm manipulation framework" width="100%">
</p>

### Trajectory generation

<p align="center">
  <img src="assets/paper/algo1_9.png" alt="Trajectory generation algorithm" width="92%">
</p>

#### Constraints in grasping and transporting

<p align="center">
  <img src="assets/paper/constraint_grasp6.png" alt="Constraint model 1" width="49%">
  <img src="assets/paper/constraint_transport6.png" alt="Constraint model 2" width="49%">
</p>

### Distributed nonlinear model predictive control

A distributed nonlinear model predictive control (DNMPC) algorithm is proposed to achieve coordinated trajectory tracking and collision avoidance while reducing the control-command cost. By accounting for the heterogeneous kinematics and physical constraints of the dual arms, the algorithm is proposed to ensure kinematic feasibility while maintaining coordinated manipulation. 
<p align="center">
  <img src="assets/paper/controlblock8.png" alt="Distributed NMPC control architecture" width="92%">
</p>

### Bilateral position-force control

The bilateral position-force control algorithm generates the desired EE positions.

<p align="center">
  <img src="assets/paper/force9.png" alt="Contact forces and internal forces between the target and the EEs" width="70%">
</p>

#### Adaptive impedance and desired-force design

<p align="center">
  <img src="assets/paper/impedance-adaptation.png" alt="Adaptive force design 1" width="32%">
  <img src="assets/paper/Desired_Force_why_v4_a.png" alt="Adaptive force design 2" width="32%">
  <img src="assets/paper/Visio-Desired_Force_why_v3_b.png" alt="Adaptive force design 3" width="32%">
</p>

## Parameter settings and selection

Parameters are selected by balancing successful task completion, trajectory tracking, internal-force regulation, execution time, and computation time. The index $i\in\{\mathrm{l}\;\mathrm{r}\}$ denotes the left or right arm. 

### Prediction horizon

The sampling period is $T_{\mathrm{s}}=20$ ms, corresponding to 50 Hz. The selected number of prediction steps is $N_{\mathrm{p}}=5$, giving a prediction horizon of $t_{\mathrm{d}}=N_{\mathrm{p}}T_{\mathrm{s}}=0.10$ s. We generate 20 transporting trajectories and conduct the comparisons on these trajectories.

In the table, CNMPC denotes centralized nonlinear model predictive control, $E_i$ denotes the total objective of the DNMPC algorithm for the $i$th arm, and Force RMSE is the root mean square error of the target's internal force. 

Increasing $N_{\mathrm{p}}$ from 2 to 5 reduces the reported force RMSE from 1.92 N to 1.88 N. Increasing it to 7 leaves that RMSE unchanged but raises mean computation time from 16.63 ms to 17.48 ms. At 10 steps, mean computation time reaches 25.81 ms and the deadline-miss rate is 22.55%. Five steps therefore provide the reported force-tracking performance with a 0% deadline-miss rate in the tested control cycles. Path generation and trajectory smoothing run offline; the online timing includes bilateral position-force control within DNMPC.

#### Comparison of MPC-based Algorithms under Different Prediction Horizons

| Algorithm | $N_{\mathrm{p}}$ | $t_{\mathrm{d}}$ (s) | $E_i$ | Force RMSE (N) | Mean computation time (ms) | Deadline miss (%) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CNMPC | 2 | 0.04 | 0.09 | 1.63 | 16.67 | 0.20 |
| CNMPC | 5 | 0.10 | 0.09 | 1.61 | 18.67 | 1.05 |
| CNMPC | 7 | 0.14 | 0.09 | 1.61 | 19.87 | 5.30 |
| CNMPC | 10 | 0.20 | 0.09 | 1.60 | 21.55 | 48.70 |
| DNMPC without state exchange | 2 | 0.04 | 0.09 | 2.14 | 15.37 | 0.00 |
| DNMPC without state exchange | 5 | 0.10 | 0.08 | 2.37 | 16.69 | 0.00 |
| DNMPC without state exchange | 7 | 0.14 | 0.08 | 2.39 | 17.48 | 0.10 |
| DNMPC without state exchange | 10 | 0.20 | 0.08 | 2.39 | 25.49 | 30.20 |
| Ours | 2 | 0.04 | 0.09 | 1.92 | 15.33 | 0.00 |
| Ours | 5 | 0.10 | 0.08 | 1.88 | 16.63 | 0.00 |
| Ours | 7 | 0.14 | 0.08 | 1.88 | 17.48 | 0.00 |
| Ours | 10 | 0.20 | 0.08 | 1.88 | 25.81 | 22.55 |

### Trajectory smoothing weights

The parameters are selected according to two principles in this paper. First, the success rate is given the highest priority since the generated trajectories must be feasible. Second, we balance the performance metrics so that improving some metrics does not substantially worsen the others.

The selected weights are:

| $w_{\mathrm{p}i}$ | $w_{\mathrm{u}i}$ | $w_{\mathrm{q}i}$ | $w_{\mathrm{v}i}$ | $w_{\mathrm{p}i,\mathrm{g}}$ | $w_{\mathrm{o}i,\mathrm{g}}$ | $w_{\mathrm{p}i,\mathrm{t}}$ | $w_{\mathrm{o}i,\mathrm{t}}$ | $w_{\mathrm{T}i}$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $10$ | $1$ | $1000$ | $1000$ | $1000$ | $1000$ | $1000$ | $1000$ | $1$ |

In practice, we first select initial parameters according to the task requirements. We then tune one parameter while keeping the others fixed, comparing $\times0$, $\times1$, and $\times2$. When $\times1$ is more suitable according to the two principles above, we fix it and continue to the next weight. For paired weights, both are changed together. The comparisons use 20 grasping trajectories and 20 transporting trajectories.

- **Trajectory length cost, $w_{\mathrm{p}i}=10$.** Selecting $\times0$ increases the trajectory length cost by 2.45% and the optimization time by 1259.72% in the grasping phase and decreases the success rate by 5% in the transporting phase. Selecting $\times2$ decreases the grasping success rate by 5% and increases the transporting optimization time by 26.82%.
- **Joint-velocity cost, $w_{\mathrm{u}i}=1$.** Selecting $\times0$ increases the joint-velocity cost by 210.98% and 81.09% and decreases the success rates by 5% and 10% in the grasping and transporting phases, respectively. Selecting $\times2$ increases the execution time by 4.14% and 10.36% and the optimization time by 23.43% and 24.27% in the grasping and transporting phases, respectively.
- **Other weights.** For the distance and orientation constraint weights during transporting, $w_{\mathrm{p}i,\mathrm{t}}=w_{\mathrm{o}i,\mathrm{t}}=1000$, the joint-position and joint-velocity constraint weights, $w_{\mathrm{q}i}=w_{\mathrm{v}i}=1000$, the terminal distance and orientation constraint weights during grasping, $w_{\mathrm{p}i,\mathrm{g}}=w_{\mathrm{o}i,\mathrm{g}}=1000$, and the time cost weight, $w_{\mathrm{T}i}=1$, selecting $\times0$ or $\times2$ decreases the success rate or substantially worsens the performance metrics, as shown in bold below.

#### Effects of the trajectory smoothing weights in the grasping phase

| Weight setting | Success rate (%) | Trajectory length cost change (%) | Joint-velocity cost change (%) | Execution time change (%) | Optimization time change (%) |
| --- | ---: | ---: | ---: | ---: | ---: |
| $w_{\mathrm{p}i}=0$ | $100.00$ | $\mathbf{+2.45}$ | $-0.43$ | $-0.01$ | $\mathbf{+1259.72}$ |
| $w_{\mathrm{p}i}\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $w_{\mathrm{p}i}\times2$ | $\mathbf{95.00}$ | $-0.22$ | $+0.33$ | $+0.01$ | $-16.65$ |
| $w_{\mathrm{u}i}=0$ | $\mathbf{95.00}$ | $-0.80$ | $\mathbf{+210.98}$ | $-61.41$ | $\mathbf{+88920.47}$ |
| $w_{\mathrm{u}i}\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $w_{\mathrm{u}i}\times2$ | $100.00$ | $+0.25$ | $-3.12$ | $\mathbf{+4.14}$ | $\mathbf{+23.43}$ |
| $(w_{\mathrm{q}i},w_{\mathrm{v}i})=0$ | $\mathbf{95.00}$ | $0.00$ | $0.00$ | $0.00$ | $+0.12$ |
| $(w_{\mathrm{q}i},w_{\mathrm{v}i})\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $(w_{\mathrm{q}i},w_{\mathrm{v}i})\times2$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $\mathbf{+2.99}$ |
| $(w_{\mathrm{p}i,\mathrm{g}},w_{\mathrm{o}i,\mathrm{g}})=0$ | $\mathbf{95.00}$ | $0.00$ | $0.00$ | $0.00$ | $-0.31$ |
| $(w_{\mathrm{p}i,\mathrm{g}},w_{\mathrm{o}i,\mathrm{g}})\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $(w_{\mathrm{p}i,\mathrm{g}},w_{\mathrm{o}i,\mathrm{g}})\times2$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $\mathbf{+1.28}$ |
| $w_{\mathrm{T}i}=0$ | $100.00$ | $-0.01$ | $-3.58$ | $\mathbf{+5.58}$ | $\mathbf{+7.01}$ |
| $w_{\mathrm{T}i}\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $w_{\mathrm{T}i}\times2$ | $100.00$ | $+0.09$ | $\mathbf{+33.03}$ | $-24.82$ | $-38.93$ |

Success rates are reported for 20 trajectories in each phase. The other columns report percentage changes relative to the corresponding $\times1$ setting. For paired weights, both weights are changed together; all other weights remain fixed. Bold entries indicate the performance metrics discussed in the parameter-selection analysis.

#### Effects of the trajectory smoothing weights in the transporting phase

| Weight setting | Success rate (%) | Trajectory length cost change (%) | Joint-velocity cost change (%) | Execution time change (%) | Optimization time change (%) |
| --- | ---: | ---: | ---: | ---: | ---: |
| $w_{\mathrm{p}i}=0$ | $\mathbf{90.00}$ | $+0.96$ | $-1.62$ | $+0.72$ | $-37.12$ |
| $w_{\mathrm{p}i}\times1$ | $95.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $w_{\mathrm{p}i}\times2$ | $95.00$ | $-0.18$ | $+1.19$ | $-0.01$ | $\mathbf{+26.82}$ |
| $w_{\mathrm{u}i}=0$ | $\mathbf{85.00}$ | $-0.44$ | $\mathbf{+81.09}$ | $-23.18$ | $\mathbf{+2031.90}$ |
| $w_{\mathrm{u}i}\times1$ | $95.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $w_{\mathrm{u}i}\times2$ | $95.00$ | $+0.25$ | $-5.61$ | $\mathbf{+10.36}$ | $\mathbf{+24.27}$ |
| $(w_{\mathrm{q}i},w_{\mathrm{v}i})=0$ | $\mathbf{90.00}$ | $0.00$ | $0.00$ | $0.00$ | $-20.16$ |
| $(w_{\mathrm{q}i},w_{\mathrm{v}i})\times1$ | $95.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $(w_{\mathrm{q}i},w_{\mathrm{v}i})\times2$ | $95.00$ | $0.00$ | $0.00$ | $0.00$ | $\mathbf{+0.67}$ |
| $(w_{\mathrm{p}i,\mathrm{t}},w_{\mathrm{o}i,\mathrm{t}})=0$ | $\mathbf{80.00}$ | $0.00$ | $+0.02$ | $-0.03$ | $-43.34$ |
| $(w_{\mathrm{p}i,\mathrm{t}},w_{\mathrm{o}i,\mathrm{t}})\times1$ | $95.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $(w_{\mathrm{p}i,\mathrm{t}},w_{\mathrm{o}i,\mathrm{t}})\times2$ | $95.00$ | $0.00$ | $+0.02$ | $-0.02$ | $\mathbf{+1.91}$ |
| $w_{\mathrm{T}i}=0$ | $\mathbf{90.00}$ | $+0.02$ | $-5.36$ | $\mathbf{+12.85}$ | $\mathbf{+33.53}$ |
| $w_{\mathrm{T}i}\times1$ | $95.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $w_{\mathrm{T}i}\times2$ | $\mathbf{90.00}$ | $+0.02$ | $\mathbf{+22.43}$ | $-21.18$ | $\mathbf{+54.93}$ |

Success rates are reported for 20 trajectories in each phase. The other columns report percentage changes relative to the corresponding $\times1$ setting. For paired weights, both weights are changed together; all other weights remain fixed. Bold entries indicate the performance metrics discussed in the parameter-selection analysis.

### DNMPC weight matrices

The weight matrices vary across the four manipulation stages: Stages 1 and 2 correspond to trajectory tracking and completion of grasping, and Stages 3 and 4 correspond to trajectory tracking and completion of transporting. Here, $I_n$ and $0_n$ denote the $n\times n$ identity and zero matrices, respectively, for $n\in\{3\;6\}$. The weight matrix $W_{\mathrm{d}i}$ is used for the deviation of the $i$th EE from the desired terminal position.

| Phase | Stage | $W_{\mathrm{t}i}$ | $W_{\mathrm{F}i}$ | $W_{\mathrm{o}i}$ | $W_{\mathrm{q}i}$ | $W_{\mathrm{v}i}$ | $W_{\mathrm{d}i}$ | $W_{\mathrm{u}i}$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Grasping | 1 | $0_{3}$ | $0_{3}$ | $0_{3}$ | $10I_{6}$ | $5I_{6}$ | $0_{3}$ | $0.01I_{6}$ |
| Grasping | 2 | $0.5I_{3}$ | $I_{3}$ | $I_{3}$ | $0_{6}$ | $0_{6}$ | $0.1I_{3}$ | $0.01I_{6}$ |
| Transporting | 3 | $40I_{3}$ | $100I_{3}$ | $2I_{3}$ | $7.5I_{6}$ | $3I_{6}$ | $0_{3}$ | $0.02I_{6}$ |
| Transporting | 4 | $1.5I_{3}$ | $I_{3}$ | $I_{3}$ | $0_{6}$ | $0_{6}$ | $10I_{3}$ | $0.01I_{6}$ |

The Stage 3 comparison uses 20 experiments per setting and changes one weight at a time to zero or twice its selected value, holding the others fixed. The terminal-position weight remains $W_{\mathrm{d}i}=0_3$.

- **Relative-position error weight $W_{\mathrm{t}i}$.** Setting the weight to zero decreases the success rate from 100% to 95%. Increasing the weight from $\times1$ to $\times2$ increases the force RMSE by 2.92% and the total DNMPC objective $E_i$ by 1.81%. Therefore, $W_{\mathrm{t}i}=40I_3$ is selected.
- **Orientation coordination weight $W_{\mathrm{o}i}$.** Setting the weight to zero reduces the success rate from 100% to 80%. Increasing the weight from $\times1$ to $\times2$ increases the relative-position RMSE by 23.08%, the force RMSE by 30.19%, and $E_i$ by 4.01% and reduces the success rate from 100% to 70%. Therefore, $W_{\mathrm{o}i}=2I_3$ is selected.
- **Control-command cost weight $W_{\mathrm{u}i}$.** Setting the weight to zero increases the control-command cost by 8.70%. Increasing the weight from $\times1$ to $\times2$ increases the joint RMSE and joint-velocity RMSE by 30.40% and 14.86%, respectively, and increases $E_i$ by 7.57%. Therefore, $W_{\mathrm{u}i}=0.02I_6$ is selected.
- **Joint-configuration tracking error weight $W_{\mathrm{q}i}$.** Setting the weight to zero reduces the success rate from 100% to 0% and increases the joint RMSE by 101.52%. Increasing the weight from $\times1$ to $\times2$ increases the force RMSE by 29.61% and reduces the success rate from 100% to 85%. Therefore, $W_{\mathrm{q}i}=7.5I_6$ is selected.
- **Joint-velocity tracking error weight $W_{\mathrm{v}i}$.** Setting the weight to zero reduces the success rate from 100% to 0% and increases the joint-velocity RMSE by 771.54%. Increasing the weight from $\times1$ to $\times2$ increases the force RMSE by 19.78% and reduces the success rate from 100% to 90%. Therefore, $W_{\mathrm{v}i}=3I_6$ is selected.
- **Weight $W_{\mathrm{F}i}$ for the position-tracking error with respect to the desired EE position generated by the bilateral position-force control algorithm.** Setting the weight to zero increases the force RMSE by 650.64% and reduces the success rate from 100% to 95%. Increasing the weight from $\times1$ to $\times2$ increases the joint-velocity RMSE by 71.29%. Therefore, $W_{\mathrm{F}i}=100I_3$ is selected.

In summary, the $\times1$ settings are selected to maintain successful task completion and balance trajectory tracking, coordination, internal-force regulation, and control-command cost.

#### Effects of the DNMPC objective weights in Stage 3

| Weight setting | Success rate (%) | Joint RMSE change (%) | Relative-position RMSE change (%) | Orientation RMSE change (%) | Joint-velocity RMSE change (%) | Force RMSE change (%) | Command cost change (%) | $E_i$ change (%) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $W_{\mathrm{t}i}=0$ | $\mathbf{95.00}$ | $+0.41$ | $+0.03$ | $-0.27$ | $+0.19$ | $-1.11$ | $+0.02$ | $-0.52$ |
| $W_{\mathrm{t}i}\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $W_{\mathrm{t}i}\times2$ | $100.00$ | $-0.25$ | $+0.04$ | $+0.27$ | $-1.23$ | $\mathbf{+2.92}$ | $-0.02$ | $\mathbf{+1.81}$ |
| $W_{\mathrm{o}i}=0$ | $\mathbf{80.00}$ | $-0.95$ | $-13.58$ | $\mathbf{+19.64}$ | $-2.05$ | $-31.24$ | $+0.01$ | $-2.17$ |
| $W_{\mathrm{o}i}\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $W_{\mathrm{o}i}\times2$ | $\mathbf{70.00}$ | $+2.10$ | $\mathbf{+23.08}$ | $-13.52$ | $+3.94$ | $\mathbf{+30.19}$ | $-0.01$ | $\mathbf{+4.01}$ |
| $W_{\mathrm{u}i}=0$ | $100.00$ | $-0.41$ | $+0.51$ | $-0.05$ | $-3.06$ | $-0.07$ | $\mathbf{+8.70}$ | $-2.59$ |
| $W_{\mathrm{u}i}\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $W_{\mathrm{u}i}\times2$ | $100.00$ | $\mathbf{+30.40}$ | $-0.46$ | $+0.06$ | $\mathbf{+14.86}$ | $+0.08$ | $-8.50$ | $\mathbf{+7.57}$ |
| $W_{\mathrm{q}i}=0$ | $\mathbf{0.00}$ | $\mathbf{+101.52}$ | $\mathbf{+44.10}$ | $-4.93$ | $+32.96$ | $-35.44$ | $-2.89$ | $\mathbf{+58.01}$ |
| $W_{\mathrm{q}i}\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $W_{\mathrm{q}i}\times2$ | $\mathbf{85.00}$ | $-35.24$ | $-16.66$ | $+1.96$ | $-12.85$ | $\mathbf{+29.61}$ | $+1.24$ | $-4.98$ |
| $W_{\mathrm{v}i}=0$ | $\mathbf{0.00}$ | $+66.07$ | $+26.37$ | $-20.52$ | $\mathbf{+771.54}$ | $-15.61$ | $-7.15$ | $\mathbf{+338.53}$ |
| $W_{\mathrm{v}i}\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $W_{\mathrm{v}i}\times2$ | $\mathbf{90.00}$ | $-27.64$ | $-13.21$ | $+5.87$ | $-40.70$ | $\mathbf{+19.78}$ | $+1.95$ | $-5.14$ |
| $W_{\mathrm{F}i}=0$ | $\mathbf{95.00}$ | $-10.33$ | $-19.27$ | $-5.57$ | $-24.26$ | $\mathbf{+650.64}$ | $0.00$ | $\mathbf{+780.75}$ |
| $W_{\mathrm{F}i}\times1$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $W_{\mathrm{F}i}\times2$ | $100.00$ | $+0.52$ | $+0.76$ | $+0.48$ | $\mathbf{+71.29}$ | $-14.44$ | $+0.04$ | $-3.51$ |

Success rates are absolute values, whereas all other entries denote changes relative to the corresponding $\times1$ setting. A negative change denotes a reduction in the corresponding error or cost.

### Adaptive parameters

| Parameter | Selected value | Role in the comparison |
| --- | --- | --- |
| $w_{\mathrm{b}i}$ | 200 | Compared with 0 and 400 |
| $w_{\mathrm{k}i}$ | 10 | Compared with 0 and 20 |
| $k_{0i}$ | 500 | Held fixed |

The adaptive damping weight $w_{\mathrm{b}i}$, the adaptive stiffness weight $w_{\mathrm{k}i}$, and $k_{0i}$ are designed for the proposed adaptive impedance control (AIC) algorithm, where $w_{\mathrm{b}i},w_{\mathrm{k}i},k_{0i}\in\mathbb{R}^+$. Each setting uses 20 trajectories. One adaptive parameter is changed at a time while the others remain fixed.

For the adaptive damping weight $w_{\mathrm{b}i}=200$, setting the parameter to zero increases the relative-position RMSE, joint-velocity RMSE, and control-command cost by 1.41%, 0.26%, and 0.05%, respectively. Increasing the parameter from $\times1$ to $\times2$ increases the force RMSE by 2.41% and reduces the success rate from 100% to 95%. Therefore, $w_{\mathrm{b}i}=200$ is selected.

For the adaptive stiffness weight $w_{\mathrm{k}i}=10$, setting the parameter to zero reduces the success rate from 100% to 0% and increases the relative-position RMSE, joint-velocity RMSE, and control-command cost by 24.13%, 31.93%, and 5.70%, respectively. Increasing the parameter from $\times1$ to $\times2$ increases the force RMSE by 30.77% and reduces the success rate from 100% to 5%. Therefore, $w_{\mathrm{k}i}=10$ is selected.

#### Effects of the adaptive parameters

| Parameter setting | Success rate (%) | Relative-position RMSE change (%) | Force RMSE change (%) | Joint-velocity RMSE change (%) | Control-command cost change (%) |
| --- | ---: | ---: | ---: | ---: | ---: |
| $w_{\mathrm{b}i}=0$ | $100.00$ | $+1.41$ | $-1.68$ | $+0.26$ | $+0.05$ |
| $w_{\mathrm{b}i}=200$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $w_{\mathrm{b}i}=400$ | $\mathbf{95.00}$ | $-1.14$ | $+2.41$ | $-0.19$ | $-0.03$ |
| $w_{\mathrm{k}i}=0$ | $\mathbf{0.00}$ | $+24.13$ | $-4.16$ | $+31.93$ | $+5.70$ |
| $w_{\mathrm{k}i}=10$ | $100.00$ | $0.00$ | $0.00$ | $0.00$ | $0.00$ |
| $w_{\mathrm{k}i}=20$ | $\mathbf{5.00}$ | $-10.35$ | $+30.77$ | $-1.41$ | $-0.26$ |

The baseline settings are $w_{\mathrm{b}i}=200$, $w_{\mathrm{k}i}=10$, and $k_{0i}=500$, where $i$ denotes the arm. One parameter is varied at a time, while the others remain fixed. Each setting uses $20$ trajectories. Success rates are absolute values, and the other columns report percentage changes relative to the corresponding baseline. Bold values indicate success rates below the baseline.

### Selection of the Desired Internal Forces for Different Targets

We first adjust the target and the force sensors so that the normal forces are along the line joining the force sensors' centers and perpendicular to the gravitational force, and stably grasp the target. We then gradually reduce the grasping force until the motion capture system detects slip onset. The force data and target-center positions are recorded simultaneously to determine the slip-onset force. This procedure is repeated five times for each target. The mean slip-onset force is multiplied by 1.5 to set the desired internal force.

In the table below, Center Position (m) is the distance in meters from the left contact point to the position that divides the target into two parts of equal mass.

| Target | Mass (kg) | Grasping Size (m) | Center Position (m) | Mean Slip-Onset Force (N) | Desired Internal Force $F_{\mathrm d}$ (N) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Ball | 0.19 | 0.18 | 0.09 | 10.29 | 15.43 |
| Box | 0.38 | 0.25 | 0.13 | 14.80 | 22.20 |
| Basketball | 0.60 | 0.25 | 0.125 | 21.60 | 32.40 |
| L-shaped wire mesh | 0.15 | 0.29 | 0.21 | 7.57 | 11.35 |
| Plush toy | 0.12 | 0.19 | 0.11 | 11.16 | 16.74 |
| Foam frame | 0.04 | 0.19 | 0.10 | 2.73 | 4.10 |
| Clothes-filled bag | 1.30 | 0.23 | 0.12 | 26.14 | 39.21 |

### Real-world experiment parameters: target ball

| Parameter | Grasping | Transporting |
| --- | --- | --- |
| Safety margin (m) | $0.005$ | $0.039$ |
| Allowable orientation to the other arm, left arm (rad) | $0.25$ | $0.500$ |
| Allowable orientation to the other arm, right arm (rad) | $0.20$ | $0.536$ |
| Allowable orientation to the target, left arm (rad) | $0.25$ | $0.25$ |
| Allowable orientation to the target, right arm (rad) | $0.20$ | $0.21$ |

### Real-world experiment parameters: target box

| Parameter | Grasping | Transporting |
| --- | --- | --- |
| Safety margin (m) | $0.005$ | $0.045$ |
| Allowable orientation to the other arm, left arm (rad) | $0.25$ | $0.428$ |
| Allowable orientation to the other arm, right arm (rad) | $0.20$ | $0.451$ |
| Allowable orientation to the target, left arm (rad) | $0.25$ | $0.25$ |
| Allowable orientation to the target, right arm (rad) | $0.20$ | $0.21$ |

## Simulation

### Ball

<p align="center">
  <a href="assets/demos/simball/d1.gif"><img src="assets/demos-preview/simball/d1.gif" alt="Ball simulation animation" width="480" height="462"></a>
</p>

### Box

<p align="center">
  <a href="assets/demos/simbox/d1.gif"><img src="assets/demos-preview/simbox/d1.gif" alt="Box simulation animation" width="480" height="414"></a>
</p>

## Experimental platform and procedure

Each arm is controlled by its own Intel NUC11 computer with an Intel Core i7-1165G7 CPU at 2.80 GHz and 16 GB RAM, running Ubuntu 20.04 and ROS1.

<p align="center">
  <img src="assets/paper/real3.png" alt="Real-world experimental platform" width="92%">
</p>

### Four-stage manipulation procedure

<p align="center">
  <img src="assets/paper/Stage1.png" alt="Manipulation stage 1" width="24%">
  <img src="assets/paper/Stage2.png" alt="Manipulation stage 2" width="24%">
  <img src="assets/paper/Stage3.png" alt="Manipulation stage 3" width="24%">
  <img src="assets/paper/Stage4.png" alt="Manipulation stage 4" width="24%">
</p>

## Real-world manipulation sequences

### Ball

<table>
  <tr>
    <th align="center" width="50%">With AIC algorithm</th>
    <th align="center" width="50%">Without AIC algorithm</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/ball/dAIC.gif"><img src="assets/demos-preview/ball/dAIC.gif" alt="Ball - With AIC algorithm" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/ball/dWITHOUTAIC.gif"><img src="assets/demos-preview/ball/dWITHOUTAIC.gif" alt="Ball - Without AIC algorithm" width="320" height="180"></a></td>
  </tr>
</table>

### Box

<table>
  <tr>
    <th align="center" width="50%">With AIC algorithm</th>
    <th align="center" width="50%">Without AIC algorithm</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/box/dAIC.gif"><img src="assets/demos-preview/box/dAIC.gif" alt="Box - With AIC algorithm" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/box/dWITHOUTAIC.gif"><img src="assets/demos-preview/box/dWITHOUTAIC.gif" alt="Box - Without AIC algorithm" width="320" height="180"></a></td>
  </tr>
</table>

### Basketball

<table>
  <tr>
    <th align="center" width="50%">With AIC algorithm</th>
    <th align="center" width="50%">Without AIC algorithm</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/basketball/dAIC.gif"><img src="assets/demos-preview/basketball/dAIC.gif" alt="Basketball - With AIC algorithm" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/basketball/dWITHOUTAIC.gif"><img src="assets/demos-preview/basketball/dWITHOUTAIC.gif" alt="Basketball - Without AIC algorithm" width="320" height="180"></a></td>
  </tr>
</table>

### Foam frame

<table>
  <tr>
    <th align="center" width="50%">With AIC algorithm</th>
    <th align="center" width="50%">Without AIC algorithm</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/softbox/dAIC.gif"><img src="assets/demos-preview/softbox/dAIC.gif" alt="Foam frame - With AIC algorithm" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/softbox/dWITHOUTAIC.gif"><img src="assets/demos-preview/softbox/dWITHOUTAIC.gif" alt="Foam frame - Without AIC algorithm" width="320" height="180"></a></td>
  </tr>
</table>

### Plush toy

<table>
  <tr>
    <th align="center" width="50%">With AIC algorithm</th>
    <th align="center" width="50%">Without AIC algorithm</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/mango/dAIC.gif"><img src="assets/demos-preview/mango/dAIC.gif" alt="Plush toy - With AIC algorithm" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/mango/dWITHOUTAIC.gif"><img src="assets/demos-preview/mango/dWITHOUTAIC.gif" alt="Plush toy - Without AIC algorithm" width="320" height="180"></a></td>
  </tr>
</table>

### L-shaped wire mesh

<table>
  <tr>
    <th align="center" width="50%">With AIC algorithm</th>
    <th align="center" width="50%">Without AIC algorithm</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/L/dAIC.gif"><img src="assets/demos-preview/L/dAIC.gif" alt="L-shaped wire mesh - With AIC algorithm" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/L/dWITHOUTAIC.gif"><img src="assets/demos-preview/L/dWITHOUTAIC.gif" alt="L-shaped wire mesh - Without AIC algorithm" width="320" height="180"></a></td>
  </tr>
</table>

### Clothes-filled bag

<table>
  <tr>
    <th align="center" width="50%">With AIC algorithm</th>
    <th align="center" width="50%">Without AIC algorithm</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/cloth/dAIC.gif"><img src="assets/demos-preview/cloth/dAIC.gif" alt="Clothes-filled bag - With AIC algorithm" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/cloth/dWITHOUTAIC.gif"><img src="assets/demos-preview/cloth/dWITHOUTAIC.gif" alt="Clothes-filled bag - Without AIC algorithm" width="320" height="180"></a></td>
  </tr>
</table>

## Experiment results


### Ball: distance, force, constraints, and position

<p align="center">
  <img src="assets/paper/EXP08/ball/distance_during_grasping.png" alt="Ball distance result 1" width="49%">
  <img src="assets/paper/EXP08/ball/distance_during_transporting.png" alt="Ball distance result 2" width="49%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/ball/d_f_legend.png" alt="Legend for distance and force plots" width="72%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/ball/force_during_grasping.png" alt="Ball force result 1" width="49%">
  <img src="assets/paper/EXP08/ball/force_during_transporting.png" alt="Ball force result 2" width="49%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/ball/4bc.png" alt="Ball constraint result 1" width="24%">
  <img src="assets/paper/EXP08/ball/4de.png" alt="Ball constraint result 2" width="24%">
  <img src="assets/paper/EXP08/ball/5bc.png" alt="Ball constraint result 3" width="24%">
  <img src="assets/paper/EXP08/ball/5de.png" alt="Ball constraint result 4" width="24%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/ball/position_legend.png" alt="Legend for ball position plots" width="72%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/ball/position_during_grasping.png" alt="Ball position result 1" width="49%">
  <img src="assets/paper/EXP08/ball/position_during_transporting.png" alt="Ball position result 2" width="49%">
</p>

### Box: distance, force, constraints, and position

<p align="center">
  <img src="assets/paper/EXP08/box/distance_during_grasping.png" alt="Box distance result 1" width="49%">
  <img src="assets/paper/EXP08/box/distance_during_transporting.png" alt="Box distance result 2" width="49%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/box/force_during_grasping.png" alt="Box force result 1" width="49%">
  <img src="assets/paper/EXP08/box/force_during_transporting.png" alt="Box force result 2" width="49%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/box/4bc.png" alt="Box constraint result 1" width="49%">
  <img src="assets/paper/EXP08/box/5bc.png" alt="Box constraint result 2" width="49%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/box/position_legend.png" alt="Legend for box position plots" width="72%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/box/position_during_grasping.png" alt="Box position result 1" width="49%">
  <img src="assets/paper/EXP08/box/position_during_transporting.png" alt="Box position result 2" width="49%">
</p>

### Internal-force results for additional targets

<p align="center">
  <img src="assets/paper/EXP08/basketball/force_during_transporting.png" alt="Additional-target force result 1" width="19.2%">
  <img src="assets/paper/EXP08/softbox/force_during_transporting.png" alt="Additional-target force result 2" width="19.2%">
  <img src="assets/paper/EXP08/mango/force_during_transporting.png" alt="Additional-target force result 3" width="19.2%">
  <img src="assets/paper/EXP08/L/force_during_transporting.png" alt="Additional-target force result 4" width="19.2%">
  <img src="assets/paper/EXP08/cloth/force_during_transporting.png" alt="Additional-target force result 5" width="19.2%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/cloth/d_f_legend2.png" alt="Legend for additional-target force plots" width="26%">
</p>

## Ball transporting under controller fault conditions

Four experiments compare left- and right-controller faults with and without predicted state exchange. The fault lasts 5 s and reverses the sign of one component in one transmitted EE position or orientation state. During the fault, both reference trajectories are held at their values at the fault start, and zero control commands keep the arm with the faulty controller at its current joint configuration.

With predicted state exchange, the controllers exchange current and predicted EE positions and orientations. Without predicted state exchange, they exchange only the current EE positions and orientations. The experiments show that the dual arms maintain the grasp with predicted state exchange under the considered fault conditions.

### Left-controller fault

<table>
  <tr>
    <th align="center" width="50%">With predicted state exchange</th>
    <th align="center" width="50%">Without predicted state exchange</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/fault/dLEFT-ON.gif"><img src="assets/demos-preview/fault/dLEFT-ON.gif" alt="Ball transporting under a left-controller fault - With predicted state exchange" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/fault/dLEFT-OFF.gif"><img src="assets/demos-preview/fault/dLEFT-OFF.gif" alt="Ball transporting under a left-controller fault - Without predicted state exchange" width="320" height="180"></a></td>
  </tr>
</table>

### Right-controller fault

<table>
  <tr>
    <th align="center" width="50%">With predicted state exchange</th>
    <th align="center" width="50%">Without predicted state exchange</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/fault/dRIGHT-ON.gif"><img src="assets/demos-preview/fault/dRIGHT-ON.gif" alt="Ball transporting under a right-controller fault - With predicted state exchange" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/fault/dRIGHT-OFF.gif"><img src="assets/demos-preview/fault/dRIGHT-OFF.gif" alt="Ball transporting under a right-controller fault - Without predicted state exchange" width="320" height="180"></a></td>
  </tr>
</table>

### Force



<p align="center">
  <img src="assets/paper/EXP08/fault/force_during_transporting.png"
       alt="Internal forces during fault-tolerance experiments" width="49%">
</p>

<p align="center">
  <img src="assets/paper/EXP08/fault/d_f_legend.png"
       alt="Legend for fault-tolerance force results" width="49%">
</p>

## Additional tasks

### Placing the ball into a box

<table>
  <tr>
    <th align="center" width="50%">With AIC algorithm</th>
    <th align="center" width="50%">Without AIC algorithm</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/placeball/dAIC.gif"><img src="assets/demos-preview/placeball/dAIC.gif" alt="Placing the ball into a box - With AIC algorithm" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/placeball/dWITHOUTAIC.gif"><img src="assets/demos-preview/placeball/dWITHOUTAIC.gif" alt="Placing the ball into a box - Without AIC algorithm" width="320" height="180"></a></td>
  </tr>
</table>

| Algorithm | EE | Desired Force (N) | Maximum (N) | Minimum (N) | Mean (N) | RMSE (N) |
| --- | :---: | ---: | ---: | ---: | ---: | ---: |
| With AIC | L | 15.43 | 27.66 | 12.51 | 16.88 | 4.30 |
| With AIC | R | 15.43 | 27.79 | 15.10 | 17.89 | 4.24 |
| Without AIC | L | 15.43 | 37.89 | 18.56 | 30.45 | 15.89 |
| Without AIC | R | 15.43 | 34.67 | 22.16 | 28.27 | 13.29 |

### Pouring the contents from one box into another box

<table>
  <tr>
    <th align="center" width="50%">With AIC algorithm</th>
    <th align="center" width="50%">Without AIC algorithm</th>
  </tr>
  <tr>
    <td align="center"><a href="assets/demos/pourbox/dAIC.gif"><img src="assets/demos-preview/pourbox/dAIC.gif" alt="Pouring the contents from one box into another box - With AIC algorithm" width="320" height="180"></a></td>
    <td align="center"><a href="assets/demos/pourbox/dWITHOUTAIC.gif"><img src="assets/demos-preview/pourbox/dWITHOUTAIC.gif" alt="Pouring the contents from one box into another box - Without AIC algorithm" width="320" height="180"></a></td>
  </tr>
</table>

| Algorithm | EE | Desired Force (N) | Maximum (N) | Minimum (N) | Mean (N) | RMSE (N) |
| --- | :---: | ---: | ---: | ---: | ---: | ---: |
| With AIC | L | 22.20 | 25.89 | 15.69 | 20.87 | 2.99 |
| With AIC | R | 22.20 | 24.93 | 15.45 | 20.81 | 2.92 |
| Without AIC | L | 22.20 | 45.00 | 24.31 | 35.91 | 14.84 |
| Without AIC | R | 22.20 | 41.85 | 23.88 | 34.33 | 13.21 |

### Task definitions

<p align="center">
  <img src="assets/paper/placeball_v2.png" alt="Additional task definition 1" width="49%">
  <img src="assets/paper/pourbox_v1.png" alt="Additional task definition 2" width="49%">
</p>

### Force results

<p align="center">
  <img src="assets/paper/EXP08/placeball/force_during_placing.png" alt="Additional task force result 1" width="49%">
  <img src="assets/paper/EXP08/pourbox/force_during_pouring.png" alt="Additional task force result 2" width="49%">
</p>

## Setup

The development environment is **Ubuntu 20.04 LTS with ROS 1 Noetic and Python 3.8**. The ROS workspace is [CM_ws](CM_ws/). Run the commands below in Linux terminals.

### Prerequisites

- **Operating system:** Ubuntu 20.04 LTS (64-bit).
- **ROS:** ROS 1 Noetic with catkin; this workspace is not a ROS 2 package.
- **Simulation:** Gazebo Classic with ROS control plugins.
- **Python:** Python 3.8, NumPy, PyYAML and CasADi 3.6.3 with Ipopt.


Additional dependencies not covered by the commands above:

- **Planning:** Pinocchio and hpp-fcl development libraries, including their CMake package configurations. FCL and hpp-fcl are separate dependencies; both are required by this workspace.

- **Real-world experiments:** the UR ROS driver and robot-side External Control, as described below.

### Compiling

From the repository root:

```bash
source /opt/ros/noetic/setup.bash
cd CM_ws
export CM_WORKSPACE="$PWD"
catkin_make
source devel/setup.bash
```

Run the following in each new terminal, from `CM_ws`:

```bash
source /opt/ros/noetic/setup.bash
source devel/setup.bash
```

The current source layout is:

```text
CM_ws/src/
  simulation/
    cm_ball/
    cm_box/
  real_world_experiment/
    cm_dnmpc/
    cm_trajectory_generation/
  asset/
    robotiq_ft_sensor/
    ur3_description/
    ur5_description/
```


### Quick start


Run one task at a time:

```bash
# Ball
roslaunch cm_ball sim.launch
```

```bash
# Box
roslaunch cm_box sim.launch
```

Each launch starts Gazebo and both controllers. Gazebo starts paused; press **Play** after initialization. 



### Real-world experiments: UR robots and Robotiq FT-300

Single arm launch files are in `cm_dnmpc/launch`. They depend on the existing `ur_robot_driver`, `ur_description` and `ur_client_library` installation, including the file `ur5e_controllers.yaml` and `ur3_controllers.yaml` driver configurations.

```bash
# UR5e: computer 192.168.1.80
roslaunch cm_dnmpc ur5e_urdriver.launch
```

```bash
# UR3: computer 192.168.2.90
roslaunch cm_dnmpc ur3_urdriver.launch
```

On the each arm's computer, the same files are also installed under `ur_robot_driver/launch`, so `roslaunch ur_robot_driver ur5e_urdriver.launch` and `roslaunch ur_robot_driver ur3_urdriver.launch` are available. Use one entry per arm, not both package variants.

| Arm | Robot IP | Computer / reverse IP | Reverse port | Script sender | Trajectory | Script command |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| UR5e / left | 192.168.1.100 | 192.168.1.80 | 50001 | 50002 | 50003 | 50004 |
| UR3 / right | 192.168.2.20 | 192.168.2.90 | 50005 | 50006 | 50007 | 50008 |

<!-- Robot IPs are retained from the original driver. UR3 needs a working route to `192.168.2.20`; its robot IP has not been guessed from the computer IP. Override `robot_ip:=...` and `reverse_ip:=...` if the hardware addresses differ. On each pendant, configure External Control with that arm's computer IP and **script sender** port, then start the program. Driver ports are separate from DNMPC's TCP ports 55005/55006.

The split preserves the existing driver controller settings and unprefixed joint names. The CM real controller currently expects prefixed joint names; resolve this interface mismatch before enabling CM motion. These changes have not been validated by moving hardware. -->

### Real-world experiments: FT300

Grant read/write permission to the actual local serial device before launching its sensor:

```bash
# UR5e
sudo chmod a+rw /dev/ttyUSB1
roslaunch robotiq_ft_sensor ur5e_ft300.launch serial_id:=ttyUSB1
```

```bash
# UR3
sudo chmod a+rw /dev/ttyUSB0
roslaunch robotiq_ft_sensor ur3_ft300.launch serial_id:=ttyUSB0
```

If the UR5e sensor is `ttyUSB0` on its computer, change both occurrences to `ttyUSB0`. Serial devices need read/write permission, not executable permission. Keep sensors unloaded and stationary during controller zero calibration.

### Real-world experiments: target acceleration input

The real controller accepts externally computed target-center acceleration and projects `F_con,i + m_i*g - m_i*a_target` onto the line joining the EEs, where `F_con,i` is the measured contact force. The projected vector is the internal force `F_i`, and its magnitude is used as the internal-force feedback. The mass assigned to each arm is half the `object.mass_kg` value in the object profile. Tool gravity compensation remains separate.

The acceleration input is `geometry_msgs/AccelStamped`: supply the target-center acceleration in `accel.linear`, in m/s² and in the same common frame as the contact forces. Obtain this acceleration by differencing the target-center positions outside the controller. This input is kinematic acceleration; gravity is added separately by the force formula. No motion-capture subscription or position differentiation is performed by the real controller.

The default topic is `/target/acceleration`. Set `--target-acceleration-topic YOUR_ACCELERATION_TOPIC` or the private parameter `~target_acceleration_topic` to the actual input. For `real.launch`, `left.launch`, or `right.launch`, use `target_acceleration_topic:=YOUR_ACCELERATION_TOPIC`. `--target-acceleration-frame FRAME_ID` optionally checks the frame name; it does not transform coordinates. The input must have increasing timestamps synchronized with the controller's ROS clock. `--target-acceleration-timeout` defaults to 0.2 s; missing or stale input is not replaced by zero acceleration. Logs include the supplied acceleration, its timestamp and both internal-force vectors. The existing simulation force model is unchanged.
