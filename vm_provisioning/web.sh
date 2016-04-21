#!/bin/bash

# Update
sudo apt-get update && sudo apt-get dist-upgrade -y

# Install PIP and needed packages
sudo apt-get install python-pip -y
sudo pip install virtualenv
