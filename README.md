# Seth's tractor bed controller!

Seth's tractor bed logic and controller, MQTT etc

## Peripherals

Inputs:

* DHT11 temperature + humidity sensor
* 5 x Push buttons connected directly to RaspberryPi GPIO pins with 10k pullup resistors

Outputs:

* 4 x Status LEDS; 1 green and 3 yellow.
* 8 x 5v powered relays, capable of switching 220v @ 10A
  * 1 x 12v roof amber beacon
  * 2 x 12v LED headlights
  * 4 x 12v LED roof side lights
  * 1 spare relay (wired with 5v out on rear cable)

All outputs are driven using an MCP23017 expander.

HATs:

* Pimoroni SpeakerPhat

### RaspberryPi GPIO

| BCM      | Raspberry Pi | Mode   | Usage         |
|----------|--------------|--------|---------------|
|          | GPIO #5      | Input  | Push button 1 |
|          | GPIO #6      | Input  | Push button 2 |
|          | GPIO #13     | Input  | Push button 3 |
|          | GPIO #22     | Input  | DHT11 sensor  |
|          | GPIO #25     | Input  | Push button 4 |
|          | GPIO #26     | Input  | Push button 5 |

### MCP23017 Expander 1

TODO: add documentation, both MCP pin, plus i2c address

| MCP Name | MCP Pin | Mode   | Usage             |
|----------|---------|--------|-------------------|
| GPB0     | 1       | Output |     |
| GPB1     | 2       | Output |      |
| GPB2     | 3       | Output |      |
| GPB3     | 4       | Output |     |
| GPB4     | 5       | Output |    |
| GPB5     | 6       | Output |     |
| GPB6     | 7       | Output |     |
| GPB7     | 8       | Output |     |
| GPA0     | 21      | Output |      |
| GPA1     | 22      | Output |      |
| GPA2     | 23      | Output |      |
| GPA3     | 24      | Output |      |
| GPA4     | 25      | Output |     |
| GPA5     | 26      | Output |     |
| GPA6     | 27      | Output |    |
| GPA7     | 28      | Output |    |

Cable to rear cabin

| Colour |                                                   | Voltage | Relay pin | Purpose   |
|--------|---------------------------------------------------|---------|-----------|-----------|
| Black  | ![](https://placehold.it/15/000000/000000?text=+) | Ground  |           |           |
| Red    | ![](https://placehold.it/15/eb4034/000000?text=+) | 12v     | 3         | Roof light          |
| Green  | ![](https://placehold.it/15/3bfa19/000000?text=+) | 12v     | 4         | Roof light           |
| Blue   | ![](https://placehold.it/15/3719fa/000000?text=+) | 12v     | 5         | Roof light           |
| Yellow | ![](https://placehold.it/15/ffea00/000000?text=+) | 12v     | 6         | Roof light           |
| White  | ![](https://placehold.it/15/dedede/000000?text=+) | 12v     | 7         | Amber beacon  |
| Brown  | ![](https://placehold.it/15/785020/000000?text=+) | 5v      | 8         |           |

Cable at front bumper

| Colour |                                                   | Voltage | Relay pin | Purpose   |
|--------|---------------------------------------------------|---------|-----------|-----------|
| Green/Yellow  | ![](https://placehold.it/15/3bfa19/000000?text=+)![](https://placehold.it/15/ffea00/000000?text=+) | Ground  |           |           |
| Blue   | ![](https://placehold.it/15/3719fa/000000?text=+) | 12v     | 1         | Head light |
| Brown  | ![](https://placehold.it/15/785020/000000?text=+) | 5v      | 2         | Head light |


## MQTT

The unit is fully controllable via MQTT, startup and regular messages are published.

| Topic                                                   |  Type                   |  Purpose          | Example payload |   
|---------------------------------------------------------|-------------------------|------------------|-----------------|
| `tractorbed/{deviceid}/status`                          |  Pub                    | once a minute    |                 |
| `tractorbed/{deviceid}/uptime`                          |  Pub                    | seconds since startup     | 302             |
| `tractorbed/{deviceid}/version`                         |  Pub                    |                  |                 |
| `tractorbed/{deviceid}/humidity`                        |  Pub                    | once a minute    |  61.3               |
| `tractorbed/{deviceid}/temperature`                     |  Pub                    | once a minute    |  22.5               |
| `tractorbed/{deviceid}/service/cmnd/reset`              |  Sub                    |                  |                 |
| `tractorbed/{deviceid}/service/cmnd/localcontrol`       |  Sub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/service/stat/localcontrol`       |  Pub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/sounds/play`                     |  Sub                    | Play MP3         | `sheep`         |
| `tractorbed/{deviceid}/sounds/playing`                  |  Pub                    |                  | `sheep`         |
| `tractorbed/{deviceid}/sounds/available/all`            |  Pub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/sounds/available/{dir}`          |  Pub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/inputs/button1`                  |  Pub                    | Button 1         | `PRESSED`       |
| `tractorbed/{deviceid}/inputs/button2`                  |  Pub                    | Button 1         | `PRESSED`       |
| `tractorbed/{deviceid}/inputs/button3`                  |  Pub                    | Button 1         | `PRESSED`       |
| `tractorbed/{deviceid}/inputs/button4`                  |  Pub                    | Button 1         | `PRESSED`       |
| `tractorbed/{deviceid}/inputs/button5`                  |  Pub                    | Button 1         | `PRESSED`       |
| `tractorbed/{deviceid}/outputs/cmnd/ledpower`           |  Sub                    | Shows if local buttons are enabled                 | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/ledpower`           |  Pub                    | Shows if local buttons are enabled                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/led1`               |  Sub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/led1`               |  Pub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/led2`               |  Sub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/led2`               |  Pub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/led3`               |  Sub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/led3`               |  Pub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/relay1`             |  Sub                    | Headlight        | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/relay1`             |  Pub                    | Headlight        | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/relay2`             |  Sub                    | Headlight        | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/relay2`             |  Pub                    | Headlight        | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/relay3`             |  Sub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/relay3`             |  Pub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/relay4`             |  Sub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/relay4`             |  Pub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/relay5`             |  Sub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/relay5`             |  Pub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/relay6`             |  Sub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/relay6`             |  Pub                    |                  | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/relay7`             |  Sub                    | Amber roof beacon | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/relay7`             |  Pub                    | Amber roof beacon | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/cmnd/relay8`             |  Sub                    | Not connected    | `ON` or `OFF`   |
| `tractorbed/{deviceid}/outputs/stat/relay8`             |  Pub                    | Not connected    | `ON` or `OFF`   |

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
