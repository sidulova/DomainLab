from domainlab.algos.a_algo_builder import NodeAlgoBuilder
from domainlab.algos.trainers.train_basic import TrainerBasic
from domainlab.algos.msels.c_msel import MSelTrLoss
from domainlab.algos.msels.c_msel_oracle import MSelOracleVisitor
from domainlab.algos.observers.b_obvisitor import ObVisitor
from domainlab.utils.utils_cuda import get_device
from domainlab.compos.zoo_nn import FeatExtractNNBuilderChainNodeGetter


def make_basic_trainer(class_name_model):
    class NodeAlgoBuilderCustom(NodeAlgoBuilder):
        def set_args(self, args, val_arg_na, prefix, argname):
            if getattr(args, argname) is None:
                setattr(args, prefix+val_arg_na, None)
                return
            list_args = getattr(args, argname)
            ind = list_args.index(val_arg_na)
            if ind+1 >= len(list_args):
                raise RuntimeError("\n nname_argna2val or npath_argna2val should \
                                   \n always be specified in pairs instead of \
                                   odd number:\
                                   \n %s" % (
                                       str(list_args)))
            val = list_args[ind+1]
            setattr(args, prefix+val_arg_na, val)

        def set_nets_from_dictionary(self, args, task, model):
            """set_nets_from_dictionary.
            :param dict_net:
            """
            for key_module_na, val_arg_na in \
                    model.dict_net_module_na2arg_na.items():
                #
                if args.nname_argna2val is None and \
                        args.npath_argna2val is None:
                    raise RuntimeError("either specify nname_argna2val or \
                                        npath_argna2val")
                self.set_args(args, val_arg_na, "nname", "nname_argna2val")
                self.set_args(args, val_arg_na, "npath", "npath_argna2val")
                #
                builder = FeatExtractNNBuilderChainNodeGetter(
                    args, arg_name_of_net="nname"+val_arg_na,
                    arg_path_of_net="npath"+val_arg_na)()

                net = builder.init_business(
                    flag_pretrain=True, dim_out=task.dim_y,
                    remove_last_layer=False, args=args,
                    i_c=task.isize.i_c, i_h=task.isize.i_h, i_w=task.isize.i_w)
                model.add_module("%s" % (key_module_na), net)

        def init_business(self, exp):
            """
            return trainer, model, observer
            """
            task = exp.task
            args = exp.args
            device = get_device(args.nocu)
            model_sel = MSelOracleVisitor(MSelTrLoss(max_es=args.es))
            observer = ObVisitor(exp, model_sel, device)
            model = class_name_model(list_str_y=task.list_str_y)
            self.set_nets_from_dictionary(args, task, model)
            trainer = TrainerBasic(model, task, observer, device, args)
            return trainer
    return NodeAlgoBuilderCustom