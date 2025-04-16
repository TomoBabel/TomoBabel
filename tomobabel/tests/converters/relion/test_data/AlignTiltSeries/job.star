
# version 50001

data_job

_rlnJobTypeLabel             relion.aligntiltseries
_rlnJobIsContinue                       0
_rlnJobIsTomo                           0
 

# version 50001

data_joboptions_values

loop_ 
_rlnJobOptionVariable #1 
_rlnJobOptionValue #2 
aretomo_thickness        200 
aretomo_tiltcorrect         No 
do_aretomo         No 
do_imod_fiducials        Yes 
do_imod_patchtrack         No 
  do_queue         No 
fiducial_diameter         10 
   gpu_ids         "" 
in_tiltseries ExcludeTiltImages/job004/selected_tilt_series.star 
min_dedicated         24 
other_args         "" 
patch_overlap         50 
patch_size        100 
      qsub     sbatch 
qsubscript /public/EM/RELION/relion-slurm-gpu-4.0.csh 
 queuename    openmpi 
 
