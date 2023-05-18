from domainlab.arg_parser import parse_cmd_args
from domainlab.compos.exp.exp_cuda_seed import set_seed  # reproducibility
from domainlab.compos.exp.exp_main import Exp
from domainlab.exp_protocol import aggregate_results
from domainlab.utils.logger import Logger

if __name__ == "__main__":
    args = parse_cmd_args()
    if args.bm_dir:
        aggregate_results.agg_main(args.bm_dir)
    else:
        set_seed(args.seed)
        exp = Exp(args=args)
        exp.execute()
