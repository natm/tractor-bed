# Seth's tractor bed controller!

Seth's tractor bed logic and controller, MQTT etc

## RaspberryPi setup

PI zero setup notes:

* Burn raspbian stretch minimal to a micro sd card
* Connect to HDMI + USB
* Login
* Edit `/etc/wpa_supplicant/wpa_supplicant.conf`, add in SSID
* Reboot
* Edit `/etc/hostname`
* Edit `/etc/tractordaemon.conf` (see `tractordaemon-example.conf` in repo)

Setup local Ansible environment, on laptop:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Bootstrap it using the included Ansible playbook:

```
ssh pi@tractorbed.home.nat.ms "mkdir .ssh"
scp ~/.ssh/id_ecdsa.pub pi@tractorbed.home.nat.ms:.ssh/authorized_keys
ansible-playbook -i deploy/hosts deploy/playbooks/tractorbed.yml -u pi -l dev
```
