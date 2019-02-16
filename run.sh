#!/bin/bash
path=`pwd`
file="epk_gather_old.py"
cd $path && (nohup python ./$file >/dev/null 2>&1 &);
