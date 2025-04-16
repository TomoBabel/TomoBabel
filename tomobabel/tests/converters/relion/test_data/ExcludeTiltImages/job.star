
# version 50001

data_job

_rlnJobTypeLabel             relion.excludetilts
_rlnJobIsContinue                       1
_rlnJobIsTomo                           0
 

# version 50001

data_joboptions_values

loop_ 
_rlnJobOptionVariable #1 
_rlnJobOptionValue #2 
cache_size          5 
  do_queue         No 
in_tiltseries CtfFind/job003/tilt_series_ctf.star 
min_dedicated         24 
other_args         "" 
      qsub     sbatch 
qsubscript /public/EM/RELION/relion-slurm-gpu-4.0.csh 
 queuename    openmpi 
 
