# RaspberryPi with GrovePi sensors

## Initial setup

1. Assembly and setup Raspberry B+ with GrovePi (see [link](http://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/) for details),
1. [GrovePi](https://www.seeedstudio.com/item_detail.html?p_id=1672) which is old version, not to be confused with new ones which are [GrovePi+](https://www.seeedstudio.com/item_detail.html?p_id=2241),
1. Old GrovePi have special instruction for updating firmware:
  * [Updating the firmware for an older GrovePi](https://docs.google.com/document/d/1fe2uCjoLpAE6Vt2HS28n_dhSfbVXZ1p-PhG1aEvIQSM/edit)
  * [grovepi-firmware-update](https://forum.dexterindustries.com/t/grovepi-firmware-update-v1-2-2/581) forum thread
1. Copy your public key to `~/.ssh/authorized_keys` on Raspberry so that you can log in without password,
1. Install [Ansible](http://docs.ansible.com/ansible/index.html) on your laptop, e.g. `brew install ansible` on Mac,
1. Install [gcloud](https://cloud.google.com/sdk/docs/#linux) tool on Raspberry,
1. Activate provided Service Account, see [docs](https://cloud.google.com/sdk/gcloud/reference/auth/activate-service-account).

## Ansible playbook

1. Run `ansible-playbook -i dex.local, setup-pi.yml` to configure Raspberry assuming that hostname is `dex.local`.

## Photos

Hardware consists of:
* [Raspberry Model B+](https://www.raspberrypi.org/products/model-b-plus/) running [Raspbian for Robots](http://www.dexterindustries.com/raspberry-pi-robot-software/) OS
* [GrovePi](http://www.dexterindustries.com/grovepi/)  
![](/.images/grovepi.jpg) 
* [Grove PIR Motion Sensor](http://www.seeedstudio.com/wiki/Grove_-_PIR_Motion_Sensor)  
![](/.images/pir_motion_sensor_top.jpg) ![](/.images/pir_motion_sensor_bottom.jpg)
* [Grove Sound Sensor](http://www.seeedstudio.com/wiki/Grove_-_Sound_Sensor)  
![](/.images/sound_sensor_top.jpg) ![](/.images/sound_sensor_bottom.jpg)
* 8GB SD Card + Charger + USB WiFi Adapter

