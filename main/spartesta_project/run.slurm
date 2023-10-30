#!/bin/bash
#SBATCH --job-name=kbarbey
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=0-02:00:00
#SBATCH --partition=p5
#SBATCH --mail-user=kent.barbey@epfl.ch
#SBATCH --mail-type=ALL
# Load the necessary modules
module purge  # Unload previously loaded modules to avoid conflicts
module load GCCcore/10.2.0  # Specify your required modules here
module load Python/3.9.6  # This depends on how Python is installed on your cluster

# Activate your virtual environment
source /home/astro/kbarbey/venv/env_pdm_Python-3.8.6/bin/activate

# Use srun to run your Python script
python /home/astro/kbarbey/pdm/run_sparta.py

# Deactivate your virtual environment when done
deactivate