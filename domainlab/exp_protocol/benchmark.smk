import sys
from pathlib import Path

try:
    config_path = workflow.configfiles[0]
except IndexError:
    raise RuntimeError("Please provide a config file using --configfile")



# NOTE: this approach to obtain the path depends on the relative path of
# this file to the domainlab directory

sys.path.insert(0, Path(workflow.basedir).parent.parent.as_posix())


envvars:
    "DOMAINLAB_CUDA_START_SEED"


def experiment_result_files(_):
    """Lists all expected i.csv"""
    from domainlab.utils.hyperparameter_sampling import is_task
    # count tasks
    num_sample_tasks = 0
    num_nonsample_tasks = 0
    for key, val in config.items():
        if is_task(val):
            if 'hyperparameters' in val.keys():
                num_sample_tasks += 1
            else:
                num_nonsample_tasks += 1
    # total number of hyperparameter samples
    total_num_params = config['num_param_samples'] * num_sample_tasks + num_nonsample_tasks
    print(f"total_num_params={total_num_params}")
    print(f"={config['num_param_samples']} * {num_sample_tasks} + {num_nonsample_tasks}")
    return [f"{config['output_dir']}/rule_results/{i}.csv" for i in range(total_num_params)]


rule parameter_sampling:
    input:
        # path to config file as input, thus a full
        # rerun is considered whenever the config yaml changed.
        expand("{path}", path=config_path)
    output:
        dest=expand("{output_dir}/hyperparameters.csv", output_dir=config["output_dir"])
    run:
        from domainlab.utils.hyperparameter_sampling import sample_hyperparameters
        sample_hyperparameters(config, str(output.dest))


rule run_experiment:
    input:
        param_file=rules.parameter_sampling.output
    output:
        # snakemake keyword temporary for temporary directory
        # like f-string in python {index} is generated in the run block as wildcards
        out_file=temporary(expand(
            "{output_dir}/rule_results/{index}.csv",
            output_dir=config["output_dir"],
            allow_missing=True
        ))
    params:
        start_seed_str=os.environ["DOMAINLAB_CUDA_START_SEED"]
    run:
        from domainlab.exp_protocol.run_experiment import run_experiment
        # import sys
        # pos = None
        # try:
        #  pos = sys.argv.index('--envvars')
        # except Exception as ex:
        #  pos = None
        # start_seed = sys.argv[pos+1]

        start_seed_str = params.start_seed_str
        if isinstance(start_seed_str, str) and (len(start_seed_str) > 0):
          # hash will keep integer intact and hash strings to random seed
          start_seed = hash(start_seed_str)
        else:
          start_seed = None
        # {index} defines wildcards named index
        index = int(expand(wildcards.index)[0])
        # :param config: dictionary from the benchmark yaml
        # :param param_file: path to the csv with the parameter samples
        # :param param_index: parameter index that should be covered by this task
        # currently this correspond to the line number in the csv file, or row number
        # in the resulting pandas dataframe
        # :param out_file: path to the output csv
        run_experiment(config,str(input.param_file),index,str(output.out_file), start_seed)


rule agg_results:
    # put different csv file in a big csv file
    input:
        exp_results=experiment_result_files
    output:
        out_file=expand("{output_dir}/results.csv", output_dir=config["output_dir"])
    run:
        import os
        out_file = str(output.out_file)
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        has_header = False
        # print(f"exp_results={input.exp_results}")
        with open(out_file, 'w') as out_stream:
            for res in input.exp_results:
                with open(res, 'r') as in_stream:
                    if has_header:
                        # skip header line
                        in_stream.readline()
                    else:
                        out_stream.writelines(in_stream.readline())
                        has_header = True
                    # write results to common file.
                    out_stream.writelines(in_stream.readlines())


rule agg_partial_results:
    input:
        dir=expand("{output_dir}/rule_results", output_dir=config["output_dir"])
    params:
        out_file=rules.agg_results.output.out_file
    run:
        import os
        out_file = str(params.out_file)
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        has_header = False
        # print(f"exp_results={input.exp_results}")
        with open(out_file, 'w') as out_stream:
            for res in os.listdir(input.dir):
                if not res.endswith('.csv'):
                    # skip non-csv file entries
                    continue
                with open(res, 'r') as in_stream:
                    if has_header:
                        # skip header line
                        in_stream.readline()
                    else:
                        out_stream.writelines(in_stream.readline())
                        has_header = True
                    # write results to common file.
                    out_stream.writelines(in_stream.readlines())


rule gen_plots:
    input:
        res_file=rules.agg_results.output.out_file
    output:
        out_dir=directory(expand("{output_dir}/graphics", output_dir=config["output_dir"]))
    run:
        from domainlab.utils.generate_benchmark_plots import gen_benchmark_plots
        gen_benchmark_plots(str(input.res_file), str(output.out_dir))


rule all:
    # output of plotting generation as input, i.e. all previous stages have to be carried out
    input:
        rules.gen_plots.output
    default_target: True