
# version 50001

data_job

_rlnJobTypeLabel             relion.motioncorr.own
_rlnJobIsContinue                       0
_rlnJobIsTomo                           1
 

# version 50001

data_joboptions_values

loop_ 
_rlnJobOptionVariable #1 
_rlnJobOptionValue #2 
   bfactor        150 
bin_factor          2 
do_even_odd_split        Yes 
do_float16        Yes 
do_own_motioncor        Yes 
  do_queue         No 
do_save_ps        Yes 
eer_grouping         32 
 fn_defect         "my_defect_file.mrc"
fn_gain_ref         "my_gain_file.mrc"
fn_motioncor2_exe /public/EM/MOTIONCOR2/MotionCor2 
 gain_flip "No flipping (0)" 
  gain_rot "No rotation (0)" 
   gpu_ids          0 
group_for_ps          4 
group_frames          1 
input_star_mics Import/job001/tilt_series.star 
min_dedicated         24 
    nr_mpi         32 
nr_threads          4 
other_args         "" 
other_motioncor2_args         "" 
   patch_x          1 
   patch_y          1 
      qsub     sbatch 
qsubscript /public/EM/RELION/relion-slurm-gpu-4.0.csh 
 queuename    openmpi 
 
