"""
executing mk_exp multiple times will cause deep copy to be called multiple times, pytest will show process got killed.
"""
from torch import nn
from torchvision import models as torchvisionmodels
from torchvision.models import ResNet50_Weights

from domainlab.algos.msels.c_msel_oracle import MSelOracleVisitor
from domainlab.algos.msels.c_msel_val import MSelValPerf
from domainlab.algos.observers.b_obvisitor import ObVisitor
from domainlab.arg_parser import mk_parser_main
from domainlab.dsets.dset_mnist_color_solo_default import DsetMNISTColorSoloDefault
from domainlab.exp.exp_main import Exp
from domainlab.models.model_erm import mk_erm
from domainlab.tasks.task_dset import mk_task_dset
from domainlab.tasks.utils_task import ImSize
from domainlab.utils.utils_cuda import get_device


def mk_exp(
    task,
    model,
    trainer: str,
    test_domain: str,
    batchsize: int,
    alone=True,
    force_best_val=False,
    msel_loss_tr=False,
):
    """
    Creates a custom experiment. The user can specify the input parameters.

    Input Parameters:
        - task: create a task to a custom dataset by importing "mk_task_dset"
        function from
        "domainlab.tasks.task_dset". For more explanation on the input params
        refer to the
        documentation found in "domainlab.tasks.task_dset.py".
        - model: create a model [NameOfModel] by importing "mk_[NameOfModel]"
        function from
        "domainlab.models.model_[NameOfModel]". For a concrete example and
        explanation of the input
        params refer to the documentation found in
        "domainlab.models.model_[NameOfModel].py"
        - trainer: string,
        - test_domain: string,
        - batch size: int

    Returns: experiment
    """

    str_arg = f"--model=apimodel --trainer={trainer} \
        --te_d={test_domain} --bs={batchsize}"
    if msel_loss_tr:
        str_arg = f"--model=apimodel --trainer={trainer} \
            --te_d={test_domain} --bs={batchsize} --msel=loss_tr"

    parser = mk_parser_main()
    conf = parser.parse_args(str_arg.split())
    device = get_device(conf)
    if alone:
        model_sel = MSelOracleVisitor()
    else:
        model_sel = MSelOracleVisitor(MSelValPerf(max_es=0))
        if force_best_val:
            model_sel.msel._best_val_acc = 1.0
    observer = ObVisitor(model_sel)
    exp = Exp(conf, task, model=model, observer=observer)
    model_sel.update(clear_counter=True)
    return exp


def test_msel_oracle():
    """
    return trainer, model, observer
    """
    task = mk_task_dset(isize=ImSize(3, 28, 28), dim_y=10, taskna="custom_task")
    task.add_domain(
        name="domain1",
        dset_tr=DsetMNISTColorSoloDefault(0),
        dset_val=DsetMNISTColorSoloDefault(1),
    )
    task.add_domain(
        name="domain2",
        dset_tr=DsetMNISTColorSoloDefault(2),
        dset_val=DsetMNISTColorSoloDefault(3),
    )
    task.add_domain(
        name="domain3",
        dset_tr=DsetMNISTColorSoloDefault(4),
        dset_val=DsetMNISTColorSoloDefault(5),
    )

    # specify backbone to use
    backbone = torchvisionmodels.resnet.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    num_final_in = backbone.fc.in_features
    backbone.fc = nn.Linear(num_final_in, task.dim_y)

    # specify model to use
    model = mk_erm(list_str_y=task.list_str_y)(backbone)

    # make trainer for model
    exp = mk_exp(task, model, trainer="mldg", test_domain="domain1", batchsize=32)
    exp.execute(num_epochs=2)

    del exp


def test_msel_oracle1():
    """
    return trainer, model, observer
    """
    task = mk_task_dset(isize=ImSize(3, 28, 28), dim_y=10, taskna="custom_task")
    task.add_domain(
        name="domain1",
        dset_tr=DsetMNISTColorSoloDefault(0),
        dset_val=DsetMNISTColorSoloDefault(1),
    )
    task.add_domain(
        name="domain2",
        dset_tr=DsetMNISTColorSoloDefault(2),
        dset_val=DsetMNISTColorSoloDefault(3),
    )
    task.add_domain(
        name="domain3",
        dset_tr=DsetMNISTColorSoloDefault(4),
        dset_val=DsetMNISTColorSoloDefault(5),
    )

    # specify backbone to use
    backbone = torchvisionmodels.resnet.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    num_final_in = backbone.fc.in_features
    backbone.fc = nn.Linear(num_final_in, task.dim_y)

    # specify model to use
    model = mk_erm(list_str_y=task.list_str_y)(backbone)

    # make trainer for model

    exp = mk_exp(
        task, model, trainer="mldg", test_domain="domain1", batchsize=32, alone=False
    )

    exp.execute(num_epochs=2)
    exp.trainer.observer.model_sel.msel.update(clear_counter=True)
    del exp


def test_msel_oracle2():
    """
    return trainer, model, observer
    """
    task = mk_task_dset(isize=ImSize(3, 28, 28), dim_y=10, taskna="custom_task")
    task.add_domain(
        name="domain1",
        dset_tr=DsetMNISTColorSoloDefault(0),
        dset_val=DsetMNISTColorSoloDefault(1),
    )
    task.add_domain(
        name="domain2",
        dset_tr=DsetMNISTColorSoloDefault(2),
        dset_val=DsetMNISTColorSoloDefault(3),
    )
    task.add_domain(
        name="domain3",
        dset_tr=DsetMNISTColorSoloDefault(4),
        dset_val=DsetMNISTColorSoloDefault(5),
    )

    # specify backbone to use
    backbone = torchvisionmodels.resnet.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    num_final_in = backbone.fc.in_features
    backbone.fc = nn.Linear(num_final_in, task.dim_y)

    # specify model to use
    model = mk_erm(list_str_y=task.list_str_y)(backbone)

    # make trainer for model
    exp = mk_exp(task, model, trainer="mldg", test_domain="domain1", batchsize=32)
    exp.execute(num_epochs=2)


def test_msel_oracle3():
    """
    return trainer, model, observer
    """
    task = mk_task_dset(isize=ImSize(3, 28, 28), dim_y=10, taskna="custom_task")
    task.add_domain(
        name="domain1",
        dset_tr=DsetMNISTColorSoloDefault(0),
        dset_val=DsetMNISTColorSoloDefault(1),
    )
    task.add_domain(
        name="domain2",
        dset_tr=DsetMNISTColorSoloDefault(2),
        dset_val=DsetMNISTColorSoloDefault(3),
    )
    task.add_domain(
        name="domain3",
        dset_tr=DsetMNISTColorSoloDefault(4),
        dset_val=DsetMNISTColorSoloDefault(5),
    )

    # specify backbone to use
    backbone = torchvisionmodels.resnet.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    num_final_in = backbone.fc.in_features
    backbone.fc = nn.Linear(num_final_in, task.dim_y)

    # specify model to use
    model = mk_erm(list_str_y=task.list_str_y)(backbone)

    exp = mk_exp(
        task,
        model,
        trainer="mldg",
        test_domain="domain1",
        batchsize=32,
        alone=False,
        force_best_val=True,
    )
    exp.execute(num_epochs=2)
    del exp


def test_msel_oracle4():
    """
    return trainer, model, observer
    """
    task = mk_task_dset(isize=ImSize(3, 28, 28), dim_y=10, taskna="custom_task")
    task.add_domain(
        name="domain1",
        dset_tr=DsetMNISTColorSoloDefault(0),
        dset_val=DsetMNISTColorSoloDefault(1),
    )
    task.add_domain(
        name="domain2",
        dset_tr=DsetMNISTColorSoloDefault(2),
        dset_val=DsetMNISTColorSoloDefault(3),
    )
    task.add_domain(
        name="domain3",
        dset_tr=DsetMNISTColorSoloDefault(4),
        dset_val=DsetMNISTColorSoloDefault(5),
    )

    # specify backbone to use
    backbone = torchvisionmodels.resnet.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    num_final_in = backbone.fc.in_features
    backbone.fc = nn.Linear(num_final_in, task.dim_y)

    # specify model to use
    model = mk_erm(list_str_y=task.list_str_y)(backbone)
    exp = mk_exp(
        task,
        model,
        trainer="mldg",
        test_domain="domain1",
        batchsize=32,
        alone=False,
        msel_loss_tr=True,
    )
    exp.execute(num_epochs=2)
    exp.trainer.observer.model_sel.msel.best_loss = 0
    exp.trainer.observer.model_sel.msel.update(clear_counter=True)
    del exp
