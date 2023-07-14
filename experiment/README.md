## Description
Following directories include LSF scripts to run `Perses` for each target system with different force fields.

## Manifest
- `cdk2/`: Cyclin dependent kinase 2
    - `espaloma-0.2.2/`
    - `espaloma-0.3.0rc6/`
    - `espaloma-0.3.0rc6-complex/`
    - `openff-2.1.0/`
- `mcl1/`: Myeloid cell leukemia 1
    - `espaloma-0.3.0rc6/`
    - `espaloma-0.3.0rc6-complex/`
    - `openff-2.1.0/`
- `p38/`: P38 mitogen-activated protein kinase
    - `espaloma-0.3.0rc6/`
    - `espaloma-0.3.0rc6-complex/`
    - `openff-2.1.0/`
- `tyk2/`: Tyrosine kinase 2
    - `espaloma-0.2.2/`
    - `espaloma-0.3.0rc6/`
    - `espaloma-0.3.0rc6-complex/`
    - `openff-2.1.0/`
- `script/`: Scripts to run the benchmark using Perses and analyze the results
    - `run_benchmark.py`
    - `benchmark_analysis.py`

## Basic Usage
- Move to one of the directories (e.g. `tyk2/openff-2.1.0/states12/`)
- Run LSF job to run Perses benchmark
    >bsub < LSF-job-template.sh

    - This will run the benchmark python script `run_benchmark.py` found [here](https://github.com/kntkb/protein-ligand-benchmark-custom/tree/main/script), but the same python script used to run the benchmark is also stored locally (`script/run_benchmark.py`).
- Analyze and plot relative and absolute free energy correlations respect to experimental values
    >python ../../../script/benchmark_analysis.py --target tyk2