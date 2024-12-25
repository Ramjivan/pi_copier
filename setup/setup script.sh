#!/bin/bash

git clone https://github.com/Ramjivan/pi_copier.git
sudo mv pi_copier/* . && sudo rm -r pi_copier/
sudo chmod +x *

sudo echo 'done' > /home/pi/copy_completed.txt

