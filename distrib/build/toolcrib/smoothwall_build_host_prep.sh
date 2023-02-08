#!/bin/bash

#Date 2/8/2023 @00:28
#Author:Tyler K Monroe aka tman904
#Purpose:Prep host system to execute the smoothwall express build system.
#Version:0.0.1

#Install the programs the build system depends on to build smoothwall properly.
sudo apt-get install build-essential gm2 flex gawk libxml-simple-perl bison inotify-tools

#Create the proper shell symlink that the build system expects.
sudo ln -s /bin/bash /bin/sh
