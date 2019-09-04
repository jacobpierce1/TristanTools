#!/bin/bash

thisdir=$(dirname $0)

if [ -z ${USING_GPU+x} ]
then
   command="python ${thisdir}/make_mayavi_jet_plots.py $@"
else
   command="vglrun python ${thisdir}/make_mayavi_jet_plots.py $@"
fi 

echo $command
$command


