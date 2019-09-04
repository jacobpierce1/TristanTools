#!/bin/bash

thisdir=$(dirname $0)

if [ -z ${USING_GPU+x} ]
then
   command="python ${thisdir}/mayavi_jet_analysis.py $@"
else
   command="vglrun python ${thisdir}/mayavi_jet_analysis.py $@"
fi 

echo $command
$command
