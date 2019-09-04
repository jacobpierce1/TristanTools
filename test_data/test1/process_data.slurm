#!/bin/bash
#SBATCH --partition=astroplasmas
#SBATCH --ntasks=1 
#SBATCH --time=100
#SBATCH --mem=30G
#SBATCH --error=process_slurm_err
#SBATCH --output=process_slurm_out

module load ffmpeg

~/jacob_astroplasmas/TristanTools/scripts/process_jet_data.sh
