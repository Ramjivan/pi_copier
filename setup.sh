#!/bin/bash

#give pi user sudo root priveleges 
sudo usermod -aG  sudo pi

#making bash files executable
chmod +x copy.sh
chmod +x cpo.sh
chmod +x copier.py
chmod +x /etc/rc.local

# startup script | adding to rc.local
sed '$i\
python copier.py &' ~/tmp | tee ~/tmp
echo "$(<~/tmp )" > /etc/rc.local
rm ~/tmp

sudo echo 'done' > ~/copy_completed.txt

