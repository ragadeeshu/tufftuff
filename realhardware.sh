sudo pigpiod
sleep 1
cd "${0%/*}"
git pull
byobu new-session -s tufftuff 'sudo python3 main.py --real'

