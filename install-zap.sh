#!/bin/bash 

yum update -y
sudo yum install wget -y
sudo wget -c https://github.com/zaproxy/zaproxy/releases/download/v2.12.0/ZAP_2.12.0_Linux.tar.gz
tar -xvf *.gz