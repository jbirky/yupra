---
layout: default
title: Configuration
nav_order: 2
---

# Configuration
{: .no_toc }


## Software installations

Required Installations:
- [Windows subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install)
- [anaconda](https://docs.anaconda.com/free/anaconda/install/linux/)


## 1. Set up a new conda environment
```bash
conda create -n yupra python==3.9
conda activate yupra
```



## 2. Installing packages with conda or pip
```bash
conda install numpy pandas astropy scipy
```


## 3. Install some custom packages for this project

Create a new file directory to install pakages from github. As an example, my file structure looks like this:
```bash
/research
	/alabi
	/vplanet
	/vplanet_inference
	...
```
To create these directories, navigate to your home directory (or somewhere where you have enough disk space):
```bash
cd ~/
```
Next, create a directory to store all research related stuff, and enter that directory:
```bash
mkdir research
cd research
```

Install `vplanet`: this is the main package for running stellar/exoplanet models in C:
```bash
git clone https://github.com/VirtualPlanetaryLaboratory/vplanet
cd vplanet
python setup.py develop
cd ..
```

Install `vplanet_inference`: this is the code we'll be using to run `vplanet` models using Python.

```bash
git clone https://github.com/jbirky/vplanet_inference
cd vplanet_inference
python setup.py install
cd ..
```

Install `alabi`: this is the code we'll be using for running statistics with our models.
```bash
git clone https://github.com/jbirky/alabi  
cd alabi  
python setup.py install
cd ..
```

## 4. Add repository paths to your bash profile
Next create an environmental variable for each of these packages. In terminal, copy these lines, replacing `path_to` with the base directory of your research folder:
```bash
echo "export PYTHONPATH=$PYTHONPATH:/path_to/research/alabi" >> ~/.bash_profile
echo "export PYTHONPATH=$PYTHONPATH:/path_to/research/vplanet" >> ~/.bash_profile
echo "export PYTHONPATH=$PYTHONPATH:/path_to/research/vplanet_inference" >> ~/.bash_profile
```