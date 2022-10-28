from torch.nn import functional as F

from domainlab.compos.nn_zoo.net_adversarial import AutoGradFunReverseMultiply
from domainlab.models.a_model_classif import AModelClassif

def mk_dann(parent_class=AModelClassif):
    """Instantiate a Deep Adversarial Net (DAN) model

    Args:
        parent_class (AModel, optional): Class object determining the task
        type. Defaults to AModelClassif.

    Returns:
        ModelDAN: model inheriting from parent class
    """
    class ModelDAN(parent_class):
        """
        anonymous
        """
        def __init__(self, list_str_y, list_str_d,
                     alpha, net_encoder, net_classifier, net_discriminator):
            super().__init__(list_str_y, list_str_d)
            self.alpha = alpha
            self.net_encoder = net_encoder
            self.net_classifier = net_classifier
            self.net_discriminator = net_discriminator

        def cal_logit_y(self, tensor_x):
            """
            calculate the logit for softmax classification
            """
            return self.net_classifier(self.net_encoder(tensor_x))

        def forward(self, tensor_x, tensor_y, tensor_d):
            return self.cal_loss(tensor_x, tensor_y, tensor_d)

        def cal_loss(self, tensor_x, tensor_y, tensor_d):
            feat = self.net_encoder(tensor_x)
            logit_d = self.net_discriminator(
                AutoGradFunReverseMultiply.apply(feat, self.alpha))
            _, d_target = tensor_d.max(dim=1)
            lc_d = F.cross_entropy(logit_d, d_target, reduction="none")
            lc_y = self.cal_task_loss(tensor_x, tensor_y)
            return lc_d + lc_y

    return ModelDAN
