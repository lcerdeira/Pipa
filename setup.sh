#!/bin/bash

apt install software-properties-common

add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/"

apt update

apt install default-jre

apt install -y bioperl ncbi-blast+ gzip unzip git

apt install -y libdatetime-perl libxml-simple-perl libdigest-md5-perl git bioperl \
    libjson-perl libtext-csv-perl libpath-tiny-perl liblwp-protocol-https-perl libwww-perl

apt install -y libmoo-perl liblist-moreutils-perl libjson-perl

apt install -y  build-essential zlib1g-dev qtbase5-dev libqt5svg5-dev

apt install locate

apt install ncbi-blast+

apt install -y python3

apt install -y python3-pip

apt install -y r-base

install.packages("devtools")
devtools::install_git("https://gitlab.com/sirarredondo/mlplasmids")

library(mlplasmids)

python3 setup.py
