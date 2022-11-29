from os import system

snames = ["PPN-R02F015A01-f4",
          "PPN-R02F015A01-f2",
          "PPN-R02F015A01",
          "PPN-R02F015A01-f4-AMD",
          "PPN-R02F015A01-f2-AMD",
          "PPN-R02F015A01-AMD",
          "PPN-R01F015A01-f4",
          "PPN-R01F015A01-f2",
          "PPN-R01F015A01",
          "PPN-R01F015A01-f4-AMD",
          "PPN-R01F015A01-f2-AMD",
          "PPN-R01F015A01-AMD",
          #"PPN-R01F015A01",
          #"PPN-R01F015A01-f2",
          #"PPN-R01F015A01-f4",
          #"PPN-R01F015A30-f2",
          ]

verbose = 1
aux_filename = "aux_pbs_twake.sh"
data_dir = "data/"
remove_checkpoints = False

omit_PPN = True
PPN = "PPN-"

pbs_script = \
"""#!/bin/bash -l
#PBS -A UMCP0012
#PBS -N {0}
#PBS -o logs/{1}.log
#PBS -e logs/{1}.log
#PBS -l walltime=23:45:00
#PBS -q casper
#PBS -l select=1:ncpus=1:ngpus=1
#PBS -l gpu_type=v100
#PBS -M tchor@umd.edu
#PBS -m abe

# Clear the environment from any previously loaded modules
module purge
module load ncarenv/1.3 gnu/11.2.0 ncarcompilers/0.5.0
module load netcdf/4.8.1 openmpi/4.1.1 julia/1.6.0 cuda/11.6
#module load peak_memusage
module li

#/glade/u/apps/ch/opt/usr/bin/dumpenv # Dumps environment (for debugging with CISL support)

export JULIA_DEPOT_PATH="/glade/work/tomasc/.julia"
#export JULIA_DEBUG="CUDAnative"

time julia --check-bounds=no --project twake.jl --simname={1} --factor=1 2>&1 | tee logs/{1}.out

qstat -f $PBS_JOBID >> logs/{1}.out
"""

for sname in snames:

    if omit_PPN and sname.startswith(PPN):
        sname_omit = sname.replace(PPN, "")
    else:
        sname_omit = sname

    if remove_checkpoints:
        cmd0 = f"rm data/chk.{sname}*.jld2"
        if verbose>0: print(cmd0)
        system(cmd0)
    auxfile1 = pbs_script.format(sname_omit, sname)
    if verbose>1: print(auxfile1)

    with open(aux_filename, "w") as f:
        f.write(auxfile1)

    cmd1 = f"qsub {aux_filename}"
    if verbose>0: print(cmd1)
    system(cmd1)

    print()
