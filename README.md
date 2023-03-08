# DomainLab: Playground for Domain Generalization

![GH Actions CI ](https://github.com/marrlab/DomainLab/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/marrlab/DomainLab/branch/master/graph/badge.svg)](https://app.codecov.io/gh/marrlab/DomainLab)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/bc22a1f9afb742efb02b87284e04dc86)](https://www.codacy.com/gh/marrlab/DomainLab/dashboard)

## Domain Generalization and DomainLab

Domain Generalization aims at learning domain invariant features by utilizing data from multiple domains so the learned feature can generalize to new unseen domains. Domain generalization algorithms try to learn domain invariant features by adding regularization upon the ERM (Emperical Risk Minimization) loss. A typical setting of evaluating domain generalization algorithms is the so called leave-one-domain-out scheme, where one dataset is collected from each distribution. Each time, one dataset/domain is left as test-set to estimate the generalization performance of a model trained upon the rest of domains/datasets.


## Why a dedicated package

DomainLab is designed by maximal decoupling of different software componets and enhance maximal code reuse.

To maximally decouple different attributing factors like loss function, neural network, training method, data feed method, DomainLab was implemented with software design patterns, where

- Domain generalization algorithms include models with associated loss function, training of the model and data feed process. They were implemented by decoupled respective classes. 

- Models was implemented in a way that keeps the underlying neural network architecture transparent, i.e. the concrete neural network architecture can be replaced like a plugin through specifying a custom neural network architecture implemented in a python file. See [Specify Custom Neural Networks for an algorithm](./docs/doc_custom_nn.md)

- To evaluate a domain generalization algorithm's performance on your custom data, the user can specify a "Task" in the form of custom python file and feed into the command line argument, thus it is at the user's discretion on how to evaluate an algorithm, so that all domain generalization algorithms could be compared fairly. See [Task Specification](./docs/doc_tasks.md). To simply test an algorithm's performance, there is no need to change any code inside this repository, the user only need to extend this repository to fit their custom need.
- The benchmark across several algorithms can be done via a single line command along with some configuration files. 


## Getting started
### Installation

-   Install via python-poetry:
Read the python-poetry documentation https://python-poetry.org/ and use the configuration file in this repository.

-   **Or** only install dependencies via pip
Suppose you have cloned the repository and have changed directory to the cloned repository.

```bash
pip install -r requirements.txt
```

### Basic usage
Suppose you have cloned the repository and the dependencies ready, change directory to the repository:
DomainLab comes with some minimal toy-dataset to test its basis functionality. To train a domain generalization model with a user-specified task, one can execute a command similar to the following.

```bash
python main_out.py --te_d=caltech --tpath=examples/tasks/task_vlcs.py --debug --bs=2 --aname=diva --gamma_y=7e5 --gamma_d=1e5 --nname=alexnet --nname_dom=conv_bn_pool_2
```

where `--tpath` specifies the path of a user specified python file which defines the domain generalization task, see Example in [Task Specification](./docs/doc_tasks.md). `--aname` specifies which algorithm to use, see [Available Algorithms](./docs/doc_algos.md), `--bs` specifies the batch size, `--debug` restrain only running for 2 epochs and save results with prefix 'debug'. For DIVA, the hyper-parameters include `--gamma_y=7e5` which is the relative weight of ERM loss compared to ELBO loss, and `--gamma_d=1e5`, which is the relative weight of domain classification loss compared to ELBO loss.
`--nname` is to specify which neural network to use for feature extraction for classification, `--nname_dom` is to specify which neural network to use for feature extraction of domains.
For usage of other arguments, check with

```bash
python main_out.py --help
```

See also [Examples](./docs/doc_examples.md).

### Output structure (results storage) and Performance Measure
[Output structure and Performance Measure](./docs/doc_output.md)

## Custom Usage

### Define your task
Do you have your own data that comes from different domains? Create a task for your data and benchmark different domain generlization algorithms according to the following example. See
[Task Specification](./docs/doc_tasks.md)

### Custom Neural network
This library decouples the concept of algorithm (model) and neural network architecture where the user could plugin different neural network architectures for the same algorithm. See
[Specify Custom Neural Networks for an algorithm](./docs/doc_custom_nn.md)

## Software Design Pattern, Extend or Contribution, Credits
[Extend or Contibute](./docs/doc_extend_contribute.md)
