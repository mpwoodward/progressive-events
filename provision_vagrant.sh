#!/usr/bin/env bash

echo "Running apt-get update ..."
apt-get update

echo "Installing required Python and other packages ..."
apt-get install -y build-essential python3-pip python3-dev python-pip python-dev python-psycopg2 libssl-dev libjpeg8-dev libjpeg62 zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libaio1 g++ git wget curl vim zip unzip libpq-dev postgresql postgresql-contrib openssl libncurses5-dev libffi-dev libreadline-dev

apt-get install -y libffi6 libffi-dev libxml2 libxml2 libxslt1-dev python-libxslt1 libxslt1-dev libcairo2 libcairo2-dev pango1.0-dev gir1.2-coglpango-1.0 libgdal1i libgdal-dev

apt-get build-dep -y gdal

apt-get install -y python-gdal

if [ ! -d /var/log/progressive-events ]
then
    echo "Creating log directory /var/log/progressive-events ..."
    mkdir /var/log/progressive-events
    chmod -R 777 /var/log/progressive-events
fi

echo "Provisioning complete."

