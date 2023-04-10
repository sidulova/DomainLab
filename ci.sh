#!/bin/bash -x -v
set -e  # exit upon first error
starttime=`date +%s`
bash -x -v ci_run_examples.sh
sh ci_pytest_cov.sh
./run_benchmark.sh examples/yaml/demo_benchmark.yaml 10 101
git checkout doc2
git merge master -m "."
sh gen_doc.sh
endtime=`date +%s`
runtime=$((endtime-starttime))
echo "total time used:"
echo "$runtime"


