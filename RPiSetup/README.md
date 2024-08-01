# Basic Set-Up of the Raspberry Pi Devices

In this section, we will guide you through installing the operating system and setting up network configurations on your headless Raspberry Pi devices starting from scratch.

The cluster that we will be working with consists of four Raspberry Pi 4 Model B units, each equipped with 8GB of RAM and a microSD card of 32GB capacity. Every Raspberry Pi, along with your own device, is interconnected via a network switch, facilitating communication between all devices through Ethernet cables. We will use Debian 12 Bookworm as the latest release when this project starts.

## Flashing the Raspberry Pi OS and Enable SSH

First of all, we flash the operating system to the SD cards. It is recommended to install Raspberry Pi OS(previously called Raspbian) with [Raspberry Pi Imager](https://www.raspberrypi.com/software/), it comes with advanced options to directly configure SSH and network settings, ect. It is also possible to use other utilities to flash the image such as [balenaEtcher](https://etcher.balena.io/). In this tutorial, we use Raspberry Pi Imager to flash Raspberry Pi OS Full (64-bit). After selecting the RPi device, OS and storage, go to Next and Edit Settings: 

1. Set hostname as rpi0, rpi1, rpi2, and rpi3 for each of the four RPis.
2. Enable SSH - Use password authentication.
3. Set username and password, the default setting is 'pi' and 'raspberry'.

## Share Internet Access and Prepare Available IP Addresses

In this step, we will share Internet connection to the RPis through an Ethernet cable. For detailed instructions on how to do this, see [Linux](https://www.tecmint.com/share-internet-in-linux/) and [Mac](https://support.apple.com/guide/mac-help/share-internet-connection-mac-network-users-mchlp1540/mac#:~:text=Turn%20on%20Internet%20Sharing%2C%20then,internet%20over%20Ethernet%2C%20choose%20Ethernet.). 

In my case, I will use the IP addresses as the table below for the next step.

|   Node        |    Hostname   | IP Address     |
| ------------- |:-------------:| :-------------:|
| master        | rpi0          | 10.42.0.250  |
| slave         | rpi1          | 10.42.0.251  |
| slave         | rpi2          | 10.42.0.252  |
| slave         | rpi3          | 10.42.0.253  |

## Set up Static IP Address

Power the RPis up, connect the Ethernet cable, and enable network sharing on your machine. Connect to each RPi via ssh, the password is "raspberry" by default.

~~~bash
ssh [username]@[hostname].local
~~~

Check the current network configuration. Look for the NAME with TYPE `ethernet` to find the correct connection. The default name for the wired ethernet connection is "Wired connection 1" for English locales. 
~~~bash
sudo nmcli -p connection show
~~~

Set the static IP address. Substitute 'Wired connection 1' with the internet connection name you used, and substitute '192.168.1.11x' with IP addresses from the previous step.
~~~bash
sudo nmcli c mod "Wired connection 1" ipv4.addresses 10.42.0.25x/24 ipv4.method manual
sudo nmcli con mod "Wired connection 1" ipv4.gateway 10.42.0.2
sudo nmcli con mod "Wired connection 1" ipv4.dns "8.8.8.8"
sudo nmcli c down "Wired connection 1" && sudo nmcli c up "Wired connection 1"
sudo reboot
~~~

## set up passwordless SSH among the rpi nodes
1. Generate SSH keys on each node. (Press enter to accept the default file location and press enter to leave the passphrase blank for no passphrase)
~~~bash
ssh-keygen -t rsa
~~~
2. Copy the public key to every node include itself.
~~~bash
ssh-copy-id pi@hostname
~~~
3. Check if there is 4 public keys inside ~/.ssh/authorized_keys file and try to SSH into the target node.
~~~bash
ssh pi@hostname
~~~


The basic set up is now completed. Try to ssh to each RPi using the configured static ip address with `ssh [username]@[ip address]`, it should work the same as `ssh [username]@[hostname].local`.
