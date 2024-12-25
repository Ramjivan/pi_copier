# 1. Run setup script

# 2. Setup autostart on boot

## Add this line in /etc/rc.local

sudo nano /etc/rc.local
python3 /home/pi/copier.py &

## make rc.local executable
sudo chmod +x /etc/rc.local

## execute the program manually once
python3 /home/pi/copier.py

## now reboot
sudo reboot





