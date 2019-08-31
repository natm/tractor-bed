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

HATs:

* Pimoroni SpeakerPhat

### RaspberryPi GPIO

| BCM      | Raspberry Pi | Mode   | Usage         |
|----------|--------------|--------|---------------|
|          | GPIO #5      | Input  | Push button 1 |
|          | GPIO #6      | Input  | Push button 2 |
|          | GPIO #13     | Input  | Push button 3 |
|          | GPIO #25     | Input  | Push button 4 |
|          | GPIO #26     | Input  | Push button 5 |

### MCP23017 Expander 1

| MCP Name | MCP Pin | Mode   | Usage             |
|----------|---------|--------|-------------------|
| GPB0     | 1       | Output | Push button 1     |
| GPB1     | 2       | Output | Push button 1     |
| GPB2     | 3       | Output | Push button 1     |
| GPB3     | 4       | Output | Push button 1     |
| GPB4     | 5       | Output | Push button 1     |
| GPB5     | 6       | Output | Push button 1     |
| GPB6     | 7       | Output | Push button 1     |
| GPB7     | 8       | Output | Push button 1     |
| GPA0     | 21      | Output | Push button 1     |
| GPA1     | 22      | Output | Push button 1     |
| GPA2     | 23      | Output | Push button 1     |
| GPA3     | 24      | Output | Push button 1     |
| GPA4     | 25      | Output | Push button 1     |
| GPA5     | 26      | Output | Push button 1     |
| GPA6     | 27      | Output | Push button 1     |
| GPA7     | 28      | Output | Push button 1     |

Output cable

| Colour |    |
|--------|----|
| Black  |    |
| Red    | ![](https://placehold.it/15/f03c15/000000?text=+)
| Green  |
| Blue   |
| Yellow |
| White  |
| Brown  |



## MQTT

The unit is fully controllable via MQTT, startup and regular messages are published.
  
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
