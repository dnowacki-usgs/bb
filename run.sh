#!/bin/bash
#$ -S /bin/bash
#
# This header must come first - it defines options that define the
# behavior of the queue system.
#
# See "man qsub" for a list of all options available.  Common options
# are listed and used below. Lines beginning with '#$' are treated as
# directives to the queue scheduler.  Lines beginning with a '#' but
# not '#$' are comments.  Unwanted options below can be disabled by
# removing the line or adding another '#' to comment them out.
#
# (recommended) option requests - note that these must come before
# other SGE options
##$ -l h_rt=01:00:00,num_proc=12
#$ -l num_proc=12
#
# (recommended) specify the queue to run the job in.  If not
# specified, the scheduler will try to determine the queue for you,
# which may not be what you want.  Options include default.q,
# scavenger.q and private queues.
#$ -q short.q
##$ -q medium.q
##$ -q default.q
##$ -q long.q
##$ -q unlim.q
##$ -q scavenger.q
#
# (optional) Turn on validation for errors.  This is needed if
# you want an immediate abort in case of error.  Otherwise your job
# may sit in the queue until the error is resolved.
#$ -w e
#
# (optional) Turn on reservations.  This has a negative performance
# impact on the scheduler itself.  It should not be used for serial
# jobs or small jobs, but may be necessary for large jobs when the
# queue is full.  If not set, small jobs may take priority over
# large jobs.
##$ -R yes
#
# (optional) provide a name for this job.  Will default to the name
# of this script if not specified.
##$ -N swan
#
# (required) Set the Parallel Environment and number of procs.
#$ -pe mpi 48
#
# (required for default.q, do not use for scavenger.q) Set the
# project.  This is used to determine which project allocation to
# use for accounting purposes.
#$ -P USGS
#
# (optional) set mail criteria and address
##$ -m a
##$ -M dnowacki@usgs.gov
#
# (optional) run in the current working directory
#$ -cwd
#
# (optional) stdout and stderr files.  If not specified, will default
# to <jobname>.[e|o]<JobID>
#$ -o stdout.out
#$ -e stderr.err
#
# (optional) specify any required environment variables
# the format is:
#  -v variable[=value],...
#
# if the value is not specified, it will be taken from the context of this
# script
##$ -v LD_LIBRARY_PATH
##$ -v LD_LIBRARY_PATH=/scratch/abeudin/netcdf/lib
##$ -v MPI_HOME
#
#
# Put your Job commands here.
#
# see "man qsub" for a listing of environment variables that can be
# set and/or queried for diagnostic and record keeping purposes.
#
#------------------------------------------------
echo "Starting Run"
echo "using $NSLOTS CPUs"
echo `date`

PATH=$MPI_HOME/bin:$PATH
PATH=$PATH:/scylla-a/home/dnowacki/swash:/scylla-a/home/dnowacki/swan4101
module load intel
##module load pgi

# OpenMPI will automatically get the number of cpus/nodes
# and hostnames from SGE environment variables.
#
# Redirecting stdout and stderr on the command line
# below is discouraged for performance reasons (unless the files
# are local rather than on an nfs mount). Use the -e and -o
# options to SGE instead.  If you are debugging and need to
# bypass SGE's output buffering, redirect on the command line.

##mpiexec -prefix $MPI_HOME coawstM ocean_chinco.in

#mpiexec -prefix $MPI_HOME -np 120 coawstM coupling_chinco.in > coupling_chinco.out

#/scylla-a/home/dnowacki/swash/swashrun -input pspace -

/scylla-a/home/dnowacki/swan4101/swanrun_djn -input bb -mpi 48

echo $PBS_NODENAME

echo "Finish Run"
echo `date`
