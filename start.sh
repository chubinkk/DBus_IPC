#!/bin/bash

sudo systemctl stop GEmu.service
sudo systemctl stop GHub.service
sudo systemctl stop GCtrl.service

sudo systemctl start GEmu.service
sudo systemctl start GHub.service
sudo systemctl start GCtrl.service

systemctl status GEmu.service
systemctl status GHub.service
systemctl status GCtrl.service
systemctl status myAppA.service

./GCli

