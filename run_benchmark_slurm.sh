#!/bin/bash

timestamp() {
#  date +"%T" # current time
  date +"%Y-%m-%d_%H-%M-%S"
}

# CONFIGFILE="examples/yaml/test_helm_benchmark.yaml"
CONFIGFILE=$1
export DOMAINLAB_CUDA_START_SEED=$2

if [ -z "$2" ]
then
      echo "argument 2: DOMAINLAB_CUDA_START_SEED empty, will set to 0"
      export DOMAINLAB_CUDA_START_SEED=0
      # in fact, the smk code will hash empty string to zero, see standalone script,
      # but here we just want to ensure the seed is 0 without worrying a different
      # behavior of the hash function
else
      export DOMAINLAB_CUDA_START_SEED=$2
fi


# ensure all runs sample the same hyperparameters
export DOMAINLAB_CUDA_HYPERPARAM_SEED=0

export NUMBER_GPUS=1
logdir="zoutput/logs"
mkdir -p $logdir
logfile="$logdir/$(timestamp).out"
echo "Configuration file: $CONFIGFILE"
echo "starting seed is: $DOMAINLAB_CUDA_START_SEED"
echo "verbose log: $logfile"
# Helmholtz
snakemake --profile "examples/yaml/slurm" --config yaml_file=$CONFIGFILE --keep-going --keep-incomplete --notemp --cores 3 -s "domainlab/exp_protocol/benchmark.smk" --configfile "$CONFIGFILE" 2>&1 | tee "$logfile"
