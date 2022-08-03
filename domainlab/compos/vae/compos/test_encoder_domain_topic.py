import torch
from domainlab.compos.vae.compos.encoder_domain_topic import EncoderSandwichTopicImg2Zd
from domainlab.arg_parser import parse_cmd_args
from domainlab.utils.utils_cuda import get_device



def test_TopicImg2Zd():
    args = parse_cmd_args()
    args.nname_encoder_sandwich_layer_img2h4zd = "conv_bn_pool_2"
    model = EncoderSandwichTopicImg2Zd(
        zd_dim=64, i_c=3, i_h=64, i_w=64,
        num_topics=5, topic_h_dim=1024, img_h_dim=1024,
        args=args)
    x = torch.rand(20, 3, 64, 64)
    topic = torch.rand(20, 5)
    q_zd, zd_q = model(x, topic)
