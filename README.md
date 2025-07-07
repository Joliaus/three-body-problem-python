# Three-Body Problem: Numerical Methods and Simulation in Python

This project simulates and visualizes the **Three-Body Problem** using various numerical methods in Python, including **Euler**, **Runge-Kutta 4**, and **Bogacki–Shampine** algorithms. Developed in **Visual Studio Code**, it offers comparative insights into the behavior and accuracy of each numerical solver.

## 🌌 Overview

The **Three-Body Problem** involves predicting the motion of three gravitationally interacting bodies. This classic problem in celestial mechanics has no general analytical solution, making numerical methods essential. This repository contains:

- Numerical simulations of the three-body problem
- Implementation of various ODE solvers
- Orbit animations and visual plots
- Comparative analysis between solvers

## 🚀 Usage

Each simulation can be run individually:

- **▶️ Run a specific solver**
  ```bash
  python "Algorithmes/Problème des 3 corps RK4g.py"

- **🎞 Animate the orbits**
  ```bash
  python "Animation graphique RK4g.py"

- **📈 Compare multiple methods**
  ```bash
  python "MI_Equa_Diff_Comparaison_des_methodes_et_courbes.py"

## 📊 Output

- Graphical plots of orbits and positions
- Energy evolution and error metrics
- Output files and images stored in `Output/`

## 📚 Reference Documents

Additional reference documents and theoretical background can be found in the `/Documents` directory. This includes:

- Research paper :
  - `PHSC_2001__5_2_161_0.pdf`
- Methodological guide :
  - `equa-diff.pdf`

## 🧠 Numerical Methods Used

- Euler Method
- Runge-Kutta 4th Order
- Bogacki–Shampine Method (adaptive step size)
- Solver comparison and analysis scripts

## 🛠 Tools & Dependencies

- **Language:** Python 3.x
- **IDE:** Visual Studio Code
- **Libraries:**
  - numpy
  - matplotlib

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Joliaus/three-body-problem-python.git
   cd three-body-problem-python

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

3. **Install the required libraries**
   ```bash
   pip install numpy matplotlib
