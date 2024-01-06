from domainlab.models.a_model_classif import AModelClassif
from domainlab.utils.override_interface import override_interface
from domainlab.compos.nn_zoo.nn import LayerId


def mk_erm(parent_class=AModelClassif):
    """
    Instantiate a Deepall (ERM) model

    Details:
        Creates a model, which trains a neural network via standard empirical risk minimization
        (ERM). The fact that the training data stems from different domains is neglected, as all
        domains are pooled together during training.

    Args:
        parent_class (AModel, optional):
            Class object determining the task type. Defaults to AModelClassif.

    Returns:
        ModelERM: model inheriting from parent class

    Input Parameters:
        custom neural network, the output dimension must be the number of labels

    Usage:
        For a concrete example, see:
        https://github.com/marrlab/DomainLab/blob/tests/test_mk_exp_erm.py
    """

    class ModelERM(parent_class):
        """
        anonymous
        """
        def __init__(self, net, list_str_y=None):
            dim_y = list(net.modules())[-1].out_features
            if list_str_y is None:
                list_str_y = [f"class{i}" for i in range(dim_y)]
            super().__init__(list_str_y)
            self.add_module("net", net)
            self._net_classifier = LayerId()

        @override_interface(AModelClassif)
        def extract_semantic_feat(self, tensor_x):
            """
            calculate the logit for softmax classification
            """
            logit_y = self.net(tensor_x)
            return logit_y
    return ModelERM
