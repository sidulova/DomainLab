import torch.optim as optim

from domainlab.algos.trainers.a_trainer import AbstractTrainer


class TrainerBasic(AbstractTrainer):
    def __init__(self, model, task, observer, device, aconf):
        super().__init__(model, task, observer, device, aconf)
        self.optimizer = optim.Adam(self.model.parameters(), lr=aconf.lr)

    def before_tr(self):
        """
        check the performance of randomly initialized weight
        """
        self.model.evaluate(self.loader_te, self.device)

    def tr_epoch(self, epoch):
        self.model.train()
        self.epo_loss_tr = 0
        for ind_batch, (tensor_x, vec_y, vec_d, *_) in enumerate(self.loader_tr):
            tensor_x, vec_y, vec_d = \
                tensor_x.to(self.device), vec_y.to(self.device), vec_d.to(self.device)
            self.optimizer.zero_grad()
            loss = self.model.cal_loss(tensor_x, vec_y, vec_d)  # @FIXME
            loss = loss.sum()
            loss.backward()
            self.optimizer.step()
            self.epo_loss_tr += loss.detach().item()
            self.after_batch(epoch, ind_batch)
        flag_stop = self.observer.update(epoch)  # notify observer
        return flag_stop
