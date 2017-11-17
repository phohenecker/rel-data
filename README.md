rel-data
========


Installation
------------

For production use, this package can be installed via pip:
```
pip install git+http://git.paho.at/phohenecker/rel-data
```

If you want to contribute to this project, though, then you should clone this repository and create a
[Conda environment](https://conda.io/docs/), as specified by [environment.yaml](./environment.yaml), for
coding and testing:
```
git clone ssh://git@git.paho.at:22022/phohenecker/rel-data.git
cd rel-data
conda env create -f environment.yaml
source activate rel-data
```
The resulting environment will contain all dependencies as described in [setup.py](./setup.py).
