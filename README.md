# Alchemical protein-ligand free energy benchmark study using Perses and espaloma-0.3.0
This repository includes scripts to validate `espaloma-0.3.0` force field with relative alchemical protein-ligand binding free energy infrastrcuture, [Perses](https://github.com/choderalab/perses). This repository is part of [espaloma-0.3.0-manuscript](https://github.com/choderalab/espaloma-0.3.0-manuscript).

## Description
Here, we compare the relative alchemical protein-ligand binding free energy calculation accuracy using `espaloma-0.3.0`, `espaloma-0.2.2`, and `openff-2.1.0` force fields against a custom [protein-ligand benchmark dataset](https://github.com/kntkb/protein-ligand-benchmark-custom) which was original taken from the [OpenFF protein-ligand-benchmark](https://github.com/openforcefield/protein-ligand-benchmark). 

Proteins are parameterized with Amber ff14SB and solvated with TIP3P water model with Joung and Cheatham monovalent counterions to neuralize the system. Small molecules are parameterized with either `espaloma-0.3.0`, `espaloma-0.2.2`, or `openff-2.1.0` force field. Additional experiments are conducted where both the proteins and small molecules are parameterized with `espaloma-0.3.0`.


## Manifest
- `experiment/`: Stores directories and scripts to run Perses
    - `cdk2/`
        - `espaloma-0.2.2/`
        - `espaloma-0.3.0rc6/`
        - `espaloma-0.3.0rc6-complex/`
        - `openff-2.1.0/`
    - `mcl1/`
        - `espaloma-0.3.0rc6/`
        - `espaloma-0.3.0rc6-complex/`
        - `openff-2.1.0/`
    - `p38/`
        - `espaloma-0.3.0rc6/`
        - `espaloma-0.3.0rc6-complex/`
        - `openff-2.1.0/`
    - `tyk2/`
        - `espaloma-0.2.2/`
        - `espaloma-0.3.0rc6/`
        - `espaloma-0.3.0rc6-complex/`
        - `openff-2.1.0/`
    - `script/`: Scripts to run the benchmark using Perses and analyze the results
        - `run_benchmark.py`
        - `benchmark_analysis.py`
- `figures/`: Stores scripts to plot figures
    - `01-plotall/`: Plot free energy calculation results for all targets
    - `02-compare-plot/`: Compare the first and second Perses runs
- `envs/`: Stores conda environment files
    - `environment-0.2.4.yaml`: Conda environment to run Perses with `espaloma-0.2.2` to parameterize small molecules
    - `environment-0.3.0.yaml`: Conda environment to run Perses with `openff-2.1.0` and `espaloma-0.3.0` to parameterize small molecules
    - `environment-0.3.0-v3.yaml`: Conda environment to run Perses with `espaloma-0.3.0` that parameterize both small molecules and proteins

## Note
- `espaloma-0.3.0rc6` refers to `espaloma-0.3.0`
- `espaloma-0.2.2` is the first generation espaloma model described in the [original paper of espaloma](https://pubs.rsc.org/en/content/articlelanding/2022/sc/d2sc02739a)

## Environment
Core dependencies are `perses 0.10.1` and modified version of `openmmforcefield 0.11.0` (commit hash: [6d2c3dcd33d9800a32032d28b6b2dca92f348a43](https://github.com/kntkb/openmmforcefields/tree/6d2c3dcd33d9800a32032d28b6b2dca92f348a43)) to support `espaloma-0.3.0`. A modified version of `perses 0.10.1` (commit hash: [0d069fc1cf31b8cce1ae7a1482c3fa46bc1382d2](https://github.com/kntkb/perses/tree/0d069fc1cf31b8cce1ae7a1482c3fa46bc1382d2)) is required to run Perses to parameterize both small molecules and proteins with `espaloma-0.3.0`.
All figures are plotted using a modified version of `cinnabar 0.3.0` (commit hash: [de7bc6623fb25d75848aa1c9f538b77cd02a4b01](https://github.com/kntkb/cinnabar/tree/de7bc6623fb25d75848aa1c9f538b77cd02a4b01)) to support arbitrary tick frequency when plotting the alchemical free energy calculation results.

## Citation
If you find this helpful please cite the following:

```
@misc{takaba2023espaloma030,
      title={Espaloma-0.3.0: Machine-learned molecular mechanics force field for the simulation of protein-ligand systems and beyond}, 
      author={Kenichiro Takaba and Iván Pulido and Mike Henry and Hugo MacDermott-Opeskin and John D. Chodera and Yuanqing Wang},
      year={2023},
      eprint={2307.07085},
      archivePrefix={arXiv},
      primaryClass={physics.chem-ph}
}
```