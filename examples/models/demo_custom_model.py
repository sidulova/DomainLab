"""
Template class to inherit from if user need custom neural network
"""
import torch
from torch.nn import functional as F

from domainlab.models.model_custom import AModelCustom
from domainlab.algos.builder_custom import make_basic_trainer


class ModelCustom(AModelCustom):
    """
    Template class to inherit from if user need custom neural network
    """
    @property
    def dict_net_module_na2arg_na(self):
        """
        we use this property to associate the module "net_predict" with commandline argument
        "my_custom_arg_name", so that one could use "net_predict" while being transparent to
        what exact backbone is used.
        """
        return {"net_predict": "my_custom_arg_name"}

    def cal_logit_y(self, tensor_x):
        """
        calculate the logit for softmax classification
        """
        logit_y = self.net_predict(tensor_x)
        return logit_y

    def cal_loss(self, tensor_x, tensor_y, tensor_d, others=None):
        """cal_loss.

        :param tensor_x:
        :param tensor_y:
        :param tensor_d:
        """
        logit_y = self.net_predict(tensor_x)
        if (tensor_y.shape[-1] == 1) | (len(tensor_y.shape) == 1):
            y_target = tensor_y
        else:
            _, y_target = tensor_y.max(dim=1)
        lc_y = F.cross_entropy(logit_y, y_target, reduction="none")
        # regularization loss is zero
        return lc_y, torch.Tensor([0]), lc_y


def get_node_na():
    """In your custom python file, this function has to be implemented
    to return the custom algorithm builder"""
    return make_basic_trainer(ModelCustom)
