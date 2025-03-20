# Hamiltonian-Informed Optimal Neural (Hion) Controller
Author: Josue N Rivera

---

**Paper:** "Receding Hamiltonian-Informed Optimal Control and State Estimation for Continuous Closed-Loop Dynamical Systems"

This projects implements Hamiltonian-Informed Optimal Neural (Hion) controllers, a novel class of neural network-based controllers for dynamical systems and explicit non-linear model-predictive control. Hion controllers estimate future states and develop an optimal control strategy using Pontryagin’s Maximum Principle. The proposed framework, along with our Taylored Multi-Faceted Approach for Neural ODE and Optimal Control (T-mano) architecture, allows for custom transient behavior, predictive control, and closed-loop feed back, addressing limitations of existing methods. Comparative analyses with established model-predictive controllers revealed Hion controllers’ superior optimality and tracking ca
pabilities. Optimal control strategies are also demonstrated for both linear and non-linear dynamical systems

### Demos

* [`Compare MPCs`](https://github.com/wzjoriv/Hion/blob/main/docs/demos/Compare%20MPCs/presentation.ipynb)

## Development

## Install

```bash
pip install hionx
```

### Train

```bash
python train-t-mano.py -c "configs/config.linear.json"
```

### Test

```bash
python test-t-mano.py -c "logs/checkpoints/linear(controller).checkpoint.pth"
```

## Citation

```bibtex
@article{rivera2024receding,
  title={Receding Hamiltonian-Informed Optimal Neural Control and State Estimation for Closed-Loop Dynamical Systems},
  author={Rivera, Josue N and Sun, Dengfeng},
  journal={arXiv preprint arXiv:2411.01297},
  year={2024}
}

@phdthesis{rivera2024multi,
  author = "Josue N Rivera",
  title = "{Multi-Scale Design and Control of Complex Advanced UAV Systems}",
  year = "2024",
  month = "12",
  url = "https://hammer.purdue.edu/articles/thesis/Multi-Scale_Design_and_Control_of_Complex_Advanced_UAV_Systems/27937332",
  doi = "10.25394/PGS.27937332.v1"
}
```