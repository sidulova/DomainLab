"""
"""
from torch import nn
from torchvision import models as torchvisionmodels
from torchvision.models import ResNet50_Weights


from domainlab.algos.msels.c_msel_oracle import MSelOracleVisitor
from domainlab.algos.observers.b_obvisitor import ObVisitor
from domainlab.models.model_deep_all import mk_deepall
from domainlab.utils.utils_cuda import get_device
from domainlab.arg_parser import mk_parser_main
from domainlab.compos.exp.exp_main import Exp

from domainlab.dsets.dset_mnist_color_solo_default import DsetMNISTColorSoloDefault
from domainlab.tasks.task_dset import mk_task_dset
from domainlab.tasks.utils_task import ImSize


def mk_exp(task, model, trainer: str, test_domain: str, batchsize: int):
    """
    Creates a custom experiment. The user can specify the input parameters.

    Input Parameters:
        - task: create a task to a custom dataset by importing "mk_task_dset" function from
        "domainlab.tasks.task_dset". For more explanation on the input params refer to the
        documentation found in "domainlab.tasks.task_dset.py".
        - model: create a model [NameOfModel] by importing "mk_[NameOfModel]" function from
        "domainlab.models.model_[NameOfModel]". For a concrete example and explanation of the input
        params refer to the documentation found in "domainlab.models.model_[NameOfModel].py"
        - trainer: string,
        - test_domain: string,
        - batch size: int

    Returns: experiment
    """

    str_arg = f"--aname=apimodel --trainer={trainer} --te_d={test_domain} --bs={batchsize}"
    parser = mk_parser_main()
    conf = parser.parse_args(str_arg.split())
    device = get_device(conf)
    model_sel = MSelOracleVisitor()
    observer = ObVisitor(model_sel, device)
    exp = Exp(conf, task, model=model, observer=observer)
    return exp


def test_msel_oracle():
    """
    return trainer, model, observer
    """
    task = mk_task_dset(isize=ImSize(3, 28, 28),  dim_y=10, taskna="custom_task")
    task.add_domain(name="domain1",
                    dset_tr=DsetMNISTColorSoloDefault(0),
                    dset_val=DsetMNISTColorSoloDefault(1))
    task.add_domain(name="domain2",
                    dset_tr=DsetMNISTColorSoloDefault(2),
                    dset_val=DsetMNISTColorSoloDefault(3))
    task.add_domain(name="domain3",
                    dset_tr=DsetMNISTColorSoloDefault(4),
                    dset_val=DsetMNISTColorSoloDefault(5))

    # specify backbone to use
    backbone = torchvisionmodels.resnet.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    num_final_in = backbone.fc.in_features
    backbone.fc = nn.Linear(num_final_in, task.dim_y)

    # specify model to use
    model = mk_deepall()(backbone)

    # make trainer for model
    exp = mk_exp(task, model, trainer="mldg", test_domain="domain1", batchsize=32)
    exp.execute(num_epochs=2)