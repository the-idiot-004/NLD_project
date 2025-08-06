# Chaotic Systems

This module is part of the **Nonlinear Dynamics** project and explores three fundamental chaotic systems: **Lorenz**, **Rössler**, and **Hindmarsh–Rose** models. Each script simulates, visualizes, and analyzes characteristic behaviors such as **Period double route to chaos**, **strange attractors**, and **sensitivity to initial conditions**.

---

## 📁 Modules Overview

### 🔷 Lorenz System

**Theory**: 
The Lorenz system models atmospheric convection using three coupled nonlinear ODEs. It was one of the first systems to demonstrate deterministic chaos and sensitive dependence on initial conditions — often summarized as the "butterfly effect".

**Scripts**
- `lorenz_2d.py` — 2D projections (x–z, y–z) of the Lorenz attractor.
- `lorenz_3d.py` — 3D visualization of the Lorenz attractor.
- `lorenz_PeriodDoubleRoute.py` — Shows period-doubling route to chaos as ρ increases.
- `lorenz_sensitivity.py` — Demonstrates divergence of two nearby trajectories.

**Results**
- `lorenz_attractor3D.png` — 3D phase space view.
- `lorenz_projections2D.png` — x–z and y–z projections.
- `lorenz_period_doubling.png` — Bifurcation diagram as ρ varies.
- `Sensitivity_on_initial_condition(z_vs_t).png` — Time series showing divergence.

---

### 🔶 Rössler System

**Theory**: 
The Rössler system is a simplified continuous-time chaotic oscillator. It was designed to produce chaos with minimal nonlinear terms and captures spiral-type attractors and bifurcations as parameters vary.

**Scripts**
- `rossler2D_PeriodDoubleRoute.py` — 2D phase space and bifurcation views by varying parameter `c`.
- `rossler3D_PeriodDoubleRoute.py` — Full 3D attractor visualization.

**Results**
- Automatically saved `.png` figures show classic spiral attractors and bifurcation structures depending on `c`.

---

### 🔷 Hindmarsh–Rose Neuron Model

**Theory**: 
The Hindmarsh–Rose model is a biologically inspired system modeling the electrical activity of a neuron. It includes a fast membrane potential, a recovery variable, and a slow adaptation current. The model captures transitions between rest, periodic spiking, and chaotic bursting.

**Scripts**
- `HR_model.py` — Simulates the system for different input currents (I), using RK4 integration.
  - I = 1.2 → Quiescence
  - I = 2.0 → Periodic bursting
  - I = 3.2 → Chaotic firing
  - I = 3.9 → Tonic spiking

**Results**
- `hindmarsh-rose_model_dynamics.png` — 12-panel plot showing:
  - (a) Phase space (x–y)
  - (b) Time series x(t)
  - (c) 3D trajectory (x, y, z) for each regime

---

## How to Run

1. Install dependencies (if not already installed):
```bash
pip install numpy matplotlib

