sudo pigpiod
sleep 1
cd "${0%/*}"
git pull
byobu new-session -d -s tufftuff 'sudo python3 main.py --real'

