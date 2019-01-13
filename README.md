# Seth's tractor bed controller!

Seth's tractor bed logic and controller, MQTT etc

## Peripherals

Inputs:

* 5 x Push buttons connected directly to RaspberryPi GPIO pins with 10k pullup resistors

Outputs:

* 4 x Status LEDS; 1 green and 3 yellow.
* 8 x 5v powered relays, capable of switching 220v @ 10A
  * 1 x 5v roof amber beacon
  * 2 x 12v LED headlights
  * 4 x 12v LED roof side lights
  * 1 spare relay (wired with 12v out)

All outputs are driven using an MCP23017 expander.

  
  
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
