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
## Prerequisits 
Confirm the sofware installed on raspbery pi are both working  
1. Install MudPi
1. Install Influx and Grafana

## Deploy interface Script

## Confirming Influx is collecting data 

## Building a Grafana Dashboard

## Enabling Email Alerting 

