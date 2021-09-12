# socket-mouse

# To see the process running in pm2
pm2 ls

# How to start if script is not running in pm2
pm2 start src/touchcontrol.py --name touchcontrol --restart-delay 3000 --time --interpreter python3
