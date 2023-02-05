"""
use random start to generate adversarial images
"""
import torch
import torch.nn.functional as F
from domainlab.algos.trainers.train_basic import TrainerBasic


class TrainerDIAL(TrainerBasic):
    """
    Trainer Domain Invariant Adversarial Learning
    """
    def gen_adversarial(self, device, img_natural, vec_y, steps_perturb=3,
                        scale=0.001, step_size=0.003, epsilon=0.031):
        """
        use naive trimming to find optimize img in the direction of adversarial gradient,
        this is not necessarily constraint optimal due to nonlinearity,
        as the constraint epsilon is only considered ad-hoc
        """
        # @FIXME: is there better way to initialize adversarial image?
        # ensure adversarial image not in computational graph
        img_adv_ini = img_natural.detach()
        img_adv_ini = img_adv_ini + scale * torch.randn(img_natural.shape).to(device).detach()
        img_adv = img_adv_ini
        for _ in range(steps_perturb):
            img_adv.requires_grad_()
            loss_gen_adv = self.model.cal_loss_gen_adv(img_natural, img_adv, vec_y)
            grad = torch.autograd.grad(loss_gen_adv, [img_adv])[0]
            # instead of gradient descent, we gradient ascent here
            img_adv = img_adv_ini.detach() + step_size * torch.sign(grad.detach())
            img_adv = torch.min(torch.max(img_adv, img_natural - epsilon), img_natural + epsilon)
            img_adv = torch.clamp(img_adv, 0.0, 1.0)
        return img_adv

    def tr_batch(self, epoch, ind_batch):
        """
        anneal parameter for each batch
        """
        self.model.hyper_update(epoch*self.num_batches + ind_batch, self.hyper_scheduler)
        return super().tr_epoch(epoch)

    def tr_epoch(self, epoch):
        self.model.train()
        self.epo_loss_tr = 0
        for ind_batch, (tensor_x, vec_y, vec_d, *_) in enumerate(self.loader_tr):
            tensor_x, vec_y, vec_d = \
                tensor_x.to(self.device), vec_y.to(self.device), vec_d.to(self.device)
            self.optimizer.zero_grad()
            loss = self.model.cal_loss(tensor_x, vec_y, vec_d)  # @FIXME
            tensor_x_adv = self.gen_adversarial(self.device, tensor_x, vec_y)
            loss_dial = self.model.cal_loss(tensor_x_adv, vec_y, vec_d)  # @FIXME
            loss = loss.sum() + loss_dial.sum()
            loss.backward()
            self.optimizer.step()
            self.epo_loss_tr += loss.detach().item()
            self.after_batch(epoch, ind_batch)
        flag_stop = self.observer.update(epoch)  # notify observer
        return flag_stop
