#!/bin/bash

# Update
sudo apt-get update && sudo apt-get dist-upgrade -y

# Install PIP and needed packages
sudo apt-get install -y python-pip build-essential python-dev apache2

# TODO: Move to requirements.txt
sudo pip install Flask
