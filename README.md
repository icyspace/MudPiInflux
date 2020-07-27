# Overview
MudPiInflux is simple interface to Mudpi which subscribes to the Redis PubSub and stores data from your garden in Influx.  Using Grafana you can then enable dashboards and alerting.  This can all run on the mudpi master raspberry pi (or could be configured on a separate machine)

## Limitations 
The interface from Redis to Influx is only written for the following.  (Others will likely work, but this is all I have tested)
* Weather / soil sensors on Arduino 
* Only 1 Relay (relay name not part of message)
* Temp / Humidity Sensor 

## Dashboard
![MudPi Dashboard](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/MudpiGrafanaDashboard.png)

## Email Alerts
![Garden Needs Water](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/Garden%20Needs%20Water%20Alert.png)

![Watering Alert](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/Automated%20Watering%20Alert.png)

![Alert History](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/Alert%20Activation%20History.png)

# Reference sites
## Hardware I used
* [Raspberry SC15184 Pi 4 Model B 2019 Quad Core 64 Bit WiFi Bluetooth (2GB)](http://amzn.com/B07TD42S27)

## Software 
* [MudPi ](https://mudpi.app/) - [MudPi github](https://github.com/mudpi)
* [Influx](https://www.influxdata.com/) - [repo](https://repos.influxdata.com/debian/)
* [Grafana](https://grafana.com/) 

## Walkthroughs 
* [Installing MudPi from Github](https://mudpi.app/guides/6)
* [Installing InfluxDB & Grafana on Raspberry Pi](https://simonhearne.com/2020/pi-influx-grafana/)
* [Install Grafana on Raspberry Pi](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/#1)

# Building Grafana Dashbard on Mudpi
## Prerequisite 
Confirm the sofware installed on raspbery pi are both working  
1. [Installing MudPi from Github](https://mudpi.app/guides/6)
1. Follow This guide to install Influx and Grafana you can skip step 0 - [Guide](https://simonhearne.com/2020/pi-influx-grafana/)
1. (Optional) Follow through with the network speed tutorial if you want to learn more about how data flows from Influx to Grafana. - [Guide](https://simonhearne.com/2020/pi-speedtest-influx)

***

## Deploy interface Script
1. Download the mudpitoinflux3.py script to your download directory <br/>
    ```shell
    cd ~/Downloads 
    wget https://raw.githubusercontent.com/icyspace/MudPiInflux/master/mudpitoinflux3.py
    '''
1. Update mudpitoinflux3.py influx credentials <br/>
    ```shell
    sudo nano mudpitoinflux3.py
    ```
    ![Alert History](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/mudpiinfluxscriptupdate.png) <br/>
    Enter Keys ctl + o  then Enter - to save the file  <br/>
    Enter Keys ctl + x – to exit 
1. Move config file to execution directory 
    <code> sudo nano mudpitoinflux3.py </code> <br/>
1. Add to supervisor Set up
    Navigate to sup supervisor directory <br/>
    <code> cd /etc/supervisor/conf.d </code> <br/>
    Create new conf file for mudpitoinflux3 script <br/>
    </code> sudo nano mudpitoinflux3.conf </code> <br/>
    Paste the following code in the file.  I have my script running out of my home directory.  If you want it to run from a different location you can create that and update this config here. <br/><br/>
    ```
    [program:mudpitoinflux3]
    directory=/home/pi
    command=python3 -u /home/pi/mudpitoinflux3.py
    autostart=true
    autorestart=true
    stderr_logfile=/home/pi/logs/mudpitoinflux3.err.log
    stdout_logfile=/home/pi/logs/mudpitoinflux3.out.log 
    ``` 
    Enter Keys ctl + o  then Enter - to save the file  <br/>
    Enter Keys ctl + x – to exit 
1. move 
  <code> </code>
## Confirming Influx is collecting data 

## Building a Grafana Dashboard

## Enabling Email Alerting 

