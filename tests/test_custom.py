import os
import pytest
from domainlab.compos.exp.exp_main import Exp
from domainlab.models.model_custom import AModelCustom
from domainlab.arg_parser import mk_parser_main


def test_custom():
    testdir = os.path.dirname(os.path.realpath(__file__))
    rootdir = os.path.join(testdir, "..")
    rootdir = os.path.abspath(rootdir)
    mpath = os.path.join(rootdir, "examples/algos/demo_custom_model.py")
    parser = mk_parser_main()
    argsstr = "--te_d=caltech --task=mini_vlcs --aname=custom --bs=2 --debug \
               --apath=%s --nname_argna2val my_custom_arg_name \
        --nname_argna2val alexnet" % (mpath)
    margs = parser.parse_args(argsstr.split())
    exp = Exp(margs)
    exp.trainer.before_tr()
    exp.trainer.tr_epoch(0)
    exp.trainer.post_tr()

def test_custom2():
    testdir = os.path.dirname(os.path.realpath(__file__))
    rootdir = os.path.join(testdir, "..")
    rootdir = os.path.abspath(rootdir)
    mpath = os.path.join(rootdir, "examples/algos/demo_custom_model.py")
    path_net = os.path.join(rootdir, "examples/nets/resnet.py")
    parser = mk_parser_main()
    argsstr = "--te_d=caltech --task=mini_vlcs --aname=custom --bs=2 --debug \
               --apath=%s --npath_argna2val my_custom_arg_name \
        --npath_argna2val %s" % (mpath, path_net)
    margs = parser.parse_args(argsstr.split())
    exp = Exp(margs)
    exp.trainer.before_tr()
    exp.trainer.tr_epoch(0)
    exp.trainer.post_tr()

def test_amodelcustom():
    class Custom(AModelCustom):
        def __init__(self, list_str_y, list_str_d=None):
            super().__init__(list_str_y, list_str_d)
        def dict_net_module_na2arg_na(self):
            super().dict_net_module_na2arg_na()
    mod = Custom(None)
    with pytest.raises(NotImplementedError):
        mod.dict_net_module_na2arg_na()
    with pytest.raises(NotImplementedError):
        mod.cal_logit_y(None)
    with pytest.raises(NotImplementedError):
        mod.forward(None, None, None)
    with pytest.raises(NotImplementedError):
        mod.cal_loss(None, None, None)
