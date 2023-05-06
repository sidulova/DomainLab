import torch.nn as nn
from torchvision import models as torchvisionmodels

from domainlab.compos.nn_zoo.nn import LayerId
from domainlab.compos.nn_zoo.nn_torchvision import NetTorchVisionBase


class costum_ResNet(nn.Module):
    def __init__(self, flag_pretrain):
        resnet50 = torchvisionmodels.resnet.resnet50(pretrained=flag_pretrain)
        # freez all batchnormalisation layers
        for module in resnet50.modules():
            if module._get_name() == 'BatchNorm2d':
                module.requires_grad_(False)

        self.resnet50_first_part = nn.Sequential(*(list(resnet50.children())[:-1]))
        self.resnet50_second_part = list(resnet50.children())[-1]
        self.dropout = nn.Dropout()

    def forward(self, x):
        x = self.resnet50_first_part(x)
        x = self.dropout(x)
        x = self.resnet50_second_part(x)
        return x


class ResNetBase(NetTorchVisionBase):
    """
    Since ResNet can be fetched from torchvision
    """
    def fetch_net(self, flag_pretrain, Domainbed_version=False):
        """fetch_net.

        :param flag_pretrain:
        """
        if Domainbed_version:
            self.net_torchvision = costum_ResNet(flag_pretrain)
        else:
            self.net_torchvision = torchvisionmodels.resnet.resnet50(
                pretrained=flag_pretrain)
        # CHANGEME: user can modify this line to choose other neural>
        # network architectures from 'torchvision.models'


class ResNet4DeepAll(ResNetBase):
    """
    change the size of the last layer
    """
    def __init__(self, flag_pretrain, dim_y):
        """__init__.

        :param flag_pretrain:
        :param dim_y:
        """
        super().__init__(flag_pretrain)
        num_final_in = self.net_torchvision.fc.in_features
        self.net_torchvision.fc = nn.Linear(num_final_in, dim_y)
        # CHANGEME: user should change "fc" to their chosen neural
        # network's last layer's name


class ResNetNoLastLayer(ResNetBase):
    """ResNetNoLastLayer."""

    def __init__(self, flag_pretrain):
        """__init__.

        :param flag_pretrain:
        """
        super().__init__(flag_pretrain)
        self.net_torchvision.fc = LayerId()
        # CHANGEME: user should change "fc" to their chosen neural
        # network's last layer's name


# CHANGEME: user is required to implement the following function
# with **exact** signature to return a neural network architecture for
# classification of dim_y number of classes if remove_last_layer=False
# or return the same neural network without the last layer if
# remove_last_layer=False.
def build_feat_extract_net(dim_y, remove_last_layer):
    """
    This function is compulsory to return a neural network feature extractor.
    :param dim_y: number of classes to be classify can be None
    if remove_last_layer = True
    :param remove_last_layer: for resnet for example, whether
    remove the last layer or not.
    """
    if remove_last_layer:
        return ResNetNoLastLayer(flag_pretrain=True)
    return ResNet4DeepAll(flag_pretrain=True, dim_y=dim_y)
