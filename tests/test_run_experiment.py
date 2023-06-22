"""
Tests run_experiment.py
"""
import pytest
import torch
import yaml

from domainlab.exp_protocol.run_experiment import run_experiment


def test_run_experiment():
    """Checks the run_experiment function on a minimal basis"""
    with open("examples/benchmark/demo_benchmark.yaml", "r", encoding="utf8") as stream:
        config = yaml.safe_load(stream)
    if torch.cuda.is_available():
        torch.cuda.init()
    config['epos'] = 1
    config['startseed'] = 1
    config['endseed'] = 1
    config['test_domains'] = ['caltech']
    param_file = "data/ztest_files/test_parameter_samples.csv"
    param_index = 0
    out_file = "zoutput/benchmarks/demo_benchmark/rule_results/0.csv"

    run_experiment(config, param_file, param_index, out_file, misc={'testing': True})
    config['test_domains'] = []
    run_experiment(config, param_file, param_index, out_file)

    config['domainlab_args']['batchsize'] = 16
    with pytest.raises(ValueError):
        run_experiment(config, param_file, param_index, out_file)
