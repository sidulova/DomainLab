"""
Test argparser functionality
"""

import os
import sys

import pytest

from domainlab.arg_parser import apply_dict_to_args, mk_parser_main, parse_cmd_args


def test_parse_cmd_args_warning():
    """Call argparser for command line"""
    sys.argv = ["main.py"]
    with pytest.warns(Warning, match="no algorithm conf specified"):
        parse_cmd_args()


def test_parse_yml_args():
    """Test argparser with yaml file"""
    testdir = os.path.dirname(os.path.realpath(__file__))
    rootdir = os.path.join(testdir, "..")
    rootdir = os.path.abspath(rootdir)
    file_path = os.path.join(rootdir, "examples/yaml/demo_config_single_run_diva.yaml")
    sys.argv = ["main.py", "--config=" + file_path]
    args = parse_cmd_args()

    # Checking if arguments are from demo.yaml
    assert args.te_d == "caltech"
    assert args.tpath == "examples/tasks/task_vlcs.py"
    assert args.bs == 2
    assert args.model == "diva"
    assert args.gamma_y == 700000.0


def test_parse_invalid_yml_args():
    """Test argparser with yaml file"""
    testdir = os.path.dirname(os.path.realpath(__file__))
    rootdir = os.path.join(testdir, "..")
    rootdir = os.path.abspath(rootdir)
    file_path = os.path.join(rootdir, "examples/yaml/demo_invalid_parameter.yaml")
    sys.argv = ["main.py", "--config=" + file_path]

    with pytest.raises(ValueError):
        parse_cmd_args()


def test_apply_dict_to_args():
    """Testing apply_dict_to_args"""
    parser = mk_parser_main()
    args = parser.parse_args(args=[])
    data = {"a": 1, "b": [1, 2], "model": "diva"}
    apply_dict_to_args(args, data, extend=True)
    assert args.a == 1
    assert args.model == "diva"
