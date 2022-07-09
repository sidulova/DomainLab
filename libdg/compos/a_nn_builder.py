"""
Integrate Chain-of-Responsibility and Builder Pattern for feature extract
"""

import abc

from libdg.compos.pcr.p_chain_handler import AbstractChainNodeHandler
from libdg.utils.utils_class import store_args


class AbstractFeatExtractNNBuilderChainNode(AbstractChainNodeHandler):
    """
    to ensure chain of responsibility node AbstractChainNodeHandler always
    work even some node can not start their heavy weight business object,
    avoid override the initializer so that node construction is always
    light weight.
    """
    def __init__(self, successor_node):
        """__init__.

        :param successor_node:
        """
        self.net_feat_extract = None
        super().__init__(successor_node)

    @store_args
    def init_business(self, flag_pretrain, dim_feat, remove_last_layer=False, args=None):
        """
        initialize **and** return the heavy weight business object for doing
        the real job
        :param request: subclass can override request object to be string or
        function
        :return: the constructed service object
        """
        return NotImplementedError

    def is_myjob(self, args):
        """is_myjob.
        :param args_nname: command line arguments:
            "--nname": name of the torchvision model
            "--npath": path to the user specified python file with neural
            network definition
        """
        return NotImplementedError
