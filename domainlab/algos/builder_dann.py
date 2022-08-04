from domainlab.algos.a_algo_builder import NodeAlgoBuilder
from domainlab.algos.trainers.train_basic import TrainerBasic
from domainlab.algos.msels.c_msel import MSelTrLoss
from domainlab.algos.msels.c_msel_oracle import MSelOracleVisitor
from domainlab.algos.observers.b_obvisitor import ObVisitor
from domainlab.utils.utils_cuda import get_device
from domainlab.compos.nn_zoo.nn_alex import AlexNetNoLastLayer
from domainlab.compos.nn_zoo.net_classif import ClassifDropoutReluLinear
from domainlab.models.model_dann import ModelDAN
from domainlab.compos.zoo_nn import FeatExtractNNBuilderChainNodeGetter
from domainlab.compos.utils_conv_get_flat_dim import get_flat_dim
from domainlab.algos.observers.c_obvisitor_cleanup import ObVisitorCleanUp


class NodeAlgoBuilderDANN(NodeAlgoBuilder):
    def init_business(self, exp):
        """
        return trainer, model, observer
        """
        task = exp.task
        args = exp.args
        device = get_device(args.nocu)
        msel = MSelOracleVisitor(MSelTrLoss(max_es=args.es))
        observer = ObVisitor(exp, msel, device)
        observer = ObVisitorCleanUp(observer)

        builder = FeatExtractNNBuilderChainNodeGetter(
            args, arg_name_of_net="nname",
            arg_path_of_net="npath")()  # request, #FIXME, constant string

        net_encoder = builder.init_business(
            flag_pretrain=True, dim_out=task.dim_y,
            remove_last_layer=False, args=args,
            i_c=task.isize.i_c,
            i_w=task.isize.i_w,
            i_h=task.isize.i_h)

        dim_feat = get_flat_dim(net_encoder,
                                task.isize.i_c,
                                task.isize.i_h,
                                task.isize.i_w)

        net_classifier = ClassifDropoutReluLinear(dim_feat, task.dim_y)
        net_discriminator = ClassifDropoutReluLinear(
            dim_feat, len(task.list_domain_tr))

        model = ModelDAN(list_str_y=task.list_str_y,
                         list_str_d=task.list_domain_tr,
                         alpha=args.gamma_reg,
                         net_encoder=net_encoder,
                         net_classifier=net_classifier,
                         net_discriminator=net_discriminator)

        trainer = TrainerBasic(model, task, observer, device, args)
        return trainer
