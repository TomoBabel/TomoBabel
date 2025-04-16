
# version 50001

data_job

_rlnJobTypeLabel             relion.importtomo
_rlnJobIsContinue                       0
_rlnJobIsTomo                           0
 

# version 50001

data_joboptions_values

loop_ 
_rlnJobOptionVariable #1 
_rlnJobOptionValue #2 
        Cs        2.7 
        Q0        0.1 
    angpix      0.675 
  do_queue         No 
dose_is_per_movie_frame         No 
 dose_rate          3 
flip_tiltseries_hand        Yes 
images_are_motion_corrected         No 
        kV        300 
mdoc_files mdoc/*.mdoc 
min_dedicated         24 
movie_files frames/*.mrc 
  mtf_file         "" 
optics_group_name    optics1 
other_args         "" 
    prefix         "" 
      qsub     sbatch 
qsubscript /public/EM/RELION/relion-slurm-gpu-4.0.csh 
 queuename    openmpi 
tilt_axis_angle         85 
 
