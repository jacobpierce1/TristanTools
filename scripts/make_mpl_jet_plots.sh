#!/bin/bash

thisdir=$(dirname $0)


command="python ${thisdir}/make_mpl_jet_plots.py $@"

echo $command
$command


