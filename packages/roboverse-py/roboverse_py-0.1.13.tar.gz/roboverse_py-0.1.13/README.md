# MetaSim

## Updates
- [2025-02-27] Move documentation (RoboVersePage) to `docs/` folder.
- [2025-02-26] Move `IsaacLab` to `third_party/IsaacLab`. Developers please update the path and reinstall the IsaacLab if necessary.
- [2025-02-13] Use [ruff](https://github.com/astral-sh/ruff) as formatter instead of black and isort. <span style="color:red">Developers please install the [ruff vscode extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)!</span>

## Getting Started
Please refer to the [documentation](https://roboverse.wiki/metasim/).

## Developer Guide
For developers, please install pre-commit hooks:
```bash
sudo apt install pre-commit
pre-commit install
```

And do install the [ruff vscode extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff).

The `.vscode/settings.json` is configured aligning with the pre-commit hooks. Whenever you save the file, it will be formatted automatically.

To migrate new tasks, please refer to the [developer guide](https://roboverse.wiki/metasim/developer_guide/new_task).

## License and Acknowledgments

The RoboVerse project is licensed under the Apache License 2.0.

The RoboVerse project makes use of the following simulation frameworks, renderers, and libraries:
- [Isaac Lab](https://github.com/isaac-sim/IsaacLab), which is built on top of [Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html)
- [Isaac Gym](https://developer.nvidia.com/isaac-gym)
- [MuJoCo](https://github.com/google-deepmind/mujoco)
- [SAPIEN](https://github.com/haosulab/SAPIEN)
- [PyRep](https://github.com/stepjam/PyRep), which is built on top of [CoppeliaSim](https://www.coppeliarobotics.com/)
- [PyBullet](https://github.com/bulletphysics/bullet3)
- [Blender](https://www.blender.org/)
- [cuRobo](https://github.com/NVlabs/curobo)

The RoboVerse project also integrates data from the following projects:
- [RLBench](https://github.com/stepjam/RLBench)
- [Maniskill](https://github.com/haosulab/ManiSkill)
- [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)
- [Meta-World](https://github.com/Farama-Foundation/Metaworld)
- [robosuite](https://github.com/ARISE-Initiative/robosuite)
- [RoboCasa](https://github.com/robocasa/robocasa)
- [GraspNet](https://graspnet.net/)
- [ARNOLD](https://arnold-benchmark.github.io/)
- [GAPartNet](https://github.com/PKU-EPIC/GAPartNet)
- [GAPartManip](https://arxiv.org/abs/2411.18276)
- [UniDoorManip](https://github.com/sectionZ6/UniDoorManip)
- [SimplerEnv](https://github.com/simpler-env/SimplerEnv)
- [RLAfford](https://github.com/hyperplane-lab/RLAfford)
- [Open6DOR](https://github.com/Selina2023/Open6DOR)
- [CALVIN](https://github.com/mees/calvin)
- [GarmentLab](https://github.com/GarmentLab/GarmentLab)
- [vMaterials](https://developer.nvidia.com/vmaterials)

TODO: Add license for assets.
TODO: Is vMaterial ok to be included in the open-source project like RoboVerse?
