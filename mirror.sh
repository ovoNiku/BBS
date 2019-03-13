#!/usr/bin/env bash
set -ex


cp /var/www/bbs/misc/sources.list /etc/apt/sources.list
mkdir -p /root/.pip
cp /var/www/bbs/misc/pip.conf /root/.pip/pip.conf
apt-get update