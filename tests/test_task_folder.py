import pytest
import os
from domainlab.arg_parser import mk_parser_main
from domainlab.tasks.task_folder_mk import mk_task_folder
from domainlab.tasks.task_folder import NodeTaskFolder
from domainlab.tasks.utils_task import ImSize
from torchvision import transforms
path_this_file = os.path.dirname(os.path.realpath(__file__))


def test_fun():
    # from domainlab.tasks.utils_task import img_loader2dir
    # import os
    node = mk_task_folder(extensions={"caltech": "jpg", "sun": "jpg", "labelme": "jpg"},
                            list_str_y=["chair", "car"],
                            dict_domain_folder_name2class={
                                "caltech": {"auto": "car",
                                            "stuhl": "chair"},
                                "sun": {"vehicle": "car",
                                        "sofa": "chair"},
                                "labelme": {"drive": "car",
                                            "sit": "chair"}
                            },
                            dict_domain_img_trans={
                                "caltech": transforms.Compose(
                                    [transforms.Resize((224, 224)),
                                    transforms.ToTensor()]),
                                "sun": transforms.Compose(
                                    [transforms.Resize((224, 224)),
                                    transforms.ToTensor()]),
                                "labelme": transforms.Compose(
                                    [transforms.Resize((224, 224)),
                                    transforms.ToTensor()]),
                            },
                            img_trans_te=transforms.Compose(
                                [transforms.Resize((224, 224)),
                                transforms.ToTensor()]),
                            isize=ImSize(3, 224, 224),
                            dict_domain2imgroot={
                                "caltech":
                                    "data/vlcs_mini/caltech/",
                                "sun":
                                    "data/vlcs_mini/sun/",
                                "labelme":
                                    "data/vlcs_mini/labelme/"},
                            taskna="mini_vlcs",
                            succ=None)



    _ = mk_task_folder(extensions={"caltech": "jpg", "sun": "jpg", "labelme": "jpg"},
                          list_str_y=["chair", "car"],
                          dict_domain_folder_name2class={
                              "caltech": {"auto": "car", "stuhl": "chair"},
                              "sun": {"viehcle": "car", "sofa": "chair"},
                              "labelme": {"drive": "car", "sit": "chair"}
                          },
                               img_trans_te=transforms.Compose(
                                   [transforms.Resize((224, 224)),
                                    transforms.ToTensor()]),

                          dict_domain_img_trans={
                              "caltech": transforms.Compose([transforms.Resize((224, 224)), ]),
                              "sun": transforms.Compose([transforms.Resize((224, 224)), ]),
                              "labelme": transforms.Compose([transforms.Resize((224, 224)), ]),
                          },
                          isize=ImSize(3, 224, 224),
                          dict_domain2imgroot={
                              "caltech": "data/vlcs_mini/caltech/",
                              "sun": "data/vlcs_mini/sun/",
                              "labelme": "data/vlcs_mini/labelme/"},
                          taskna="mini_vlcs")

    parser = mk_parser_main()
    # batchsize bs=2 ensures it works on small dataset
    args = parser.parse_args(["--te_d", "1", "--bs", "2", "--aname", "diva"])
    node.init_business(args)
    node.get_list_domains()
    print(node.list_str_y)
    print(node.list_domain_tr)
    print(node.task_name)
    node.sample_sav(args.out)
    # alternatively:
    # folder_na = os.path.join(args.out, "task_sample", node.task_name)
    # img_loader2dir(node.loader_te,
    #               list_domain_na=node.get_list_domains(),
    #               list_class_na=node.list_str_y,
    #               folder=folder_na,
    #               batches=10)

    # img_loader2dir(node.loader_tr,
    #               list_domain_na=node.get_list_domains(),
    #               list_class_na=node.list_str_y,
    #               folder=folder_na,
    #               batches=10)


@pytest.fixture
def pacs_node():
    # FIXME: make me work with mk_task_folder
    node = NodeTaskFolder()
    node.set_list_domains(["cartoon", "photo"])
    node.extensions = {"cartoon": "jpg", "photo": "jpg"}
    node.list_str_y = ["dog", "elephant"] 
    node.dict_domain2imgroot = {
        "cartoon": "data/pacs_mini_10/cartoon/",
        "photo": "data/pacs_mini_10/photo/"
    }
    return node

@pytest.fixture
def folder_args():
    parser = mk_parser_main()
    args = parser.parse_args(["--te_d", "1", "--bs", "2", "--aname", "diva"])
    return args

def test_nodetaskfolder(pacs_node, folder_args):
    pacs_node.init_business(folder_args)

def test_nodetaskfolder_transforms(pacs_node, folder_args):
    pacs_node._dict_domain_img_trans = {
        "cartoon": transforms.Compose([transforms.Resize((224, 224)), ]),
        "photo": transforms.Compose([transforms.Resize((224, 224)), ])
    }
    pacs_node.img_trans_te = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    pacs_node.init_business(folder_args)

def test_nodetaskfolder_split_error(pacs_node, folder_args):
    folder_args.split = True
    with pytest.raises(RuntimeError):
        pacs_node.init_business(folder_args)