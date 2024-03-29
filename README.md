[Skip to walkthrough](https://github.com/icyspace/MudPiInflux#building-grafana-dashbard-on-mudpi)

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
* [LM393 Rain Drops Sensor Weather Moisture Monitor Sensor](http://amzn.com/B01DK29K28)
* [BACOENG 1" DC12V Electric Solenoid Valve (NPT, Brass, Normally Closed)](http://amzn.com/B010LT2D3Q)
* [Capacitive Soil Moisture Sensor Corrosion Resistant](http://amzn.com/B07SYBSHGX)
* [2 Channel DC 5V Relay Module with Optocoupler Low Level Trigger Expansion Board](http://amzn.com/B00E0NTPP4)
* [5pcs DHT11 Temperature Humidity Sensor Module Digital Temperature Humidity Sensor](http://amzn.com/B01DKC2GQ0)

## Software 
* [MudPi ](https://mudpi.app/) - [MudPi github](https://github.com/mudpi)
* [Influx](https://www.influxdata.com/) - [repo](https://repos.influxdata.com/debian/)
* [Grafana](https://grafana.com/) 

## Walkthroughs 
* [Installing MudPi from Github](https://mudpi.app/guides/6)
* [Installing InfluxDB & Grafana on Raspberry Pi](https://simonhearne.com/2020/pi-influx-grafana/)
* [Install Grafana on Raspberry Pi](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/#1)

# Building Grafana Dashboard on Mudpi
## Prerequisite 
Confirm the software installed on raspberry pi are both working  
1. [Installing MudPi from Github](https://mudpi.app/guides/6)
1. Follow This guide to install Influx and Grafana you can skip step 0 - [Guide](https://simonhearne.com/2020/pi-influx-grafana/)
1. (Optional) Follow through with the network speed tutorial if you want to learn more about how data flows from Influx to Grafana. - [Guide](https://simonhearne.com/2020/pi-speedtest-influx)
1. (Optional) if installing influx on a different machine you can run this script on that machine or you can install influxdb-client on the PI instedad.   
    ```shell
    pip3 install influxdb
    ```
    should upgrade to the new client     pip3 install influxdb-client

***

## Deploy Interface Script
1. Download the mudpitoinflux3.py script to your download directory <br/>
    ```shell
    cd ~/Downloads 
    ```
    ```shell
    wget https://raw.githubusercontent.com/icyspace/MudPiInflux/master/mudpitoinflux3.py
    ```
1. Update mudpitoinflux3.py influx credentials <br/>
    ```shell
    sudo nano mudpitoinflux3.py
    ```
    ![Alert History](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/mudpiinfluxscriptupdate.png) <br/>
    Enter Keys ctl + o  then Enter - to save the file  <br/>
    Enter Keys ctl + x – to exit 
1. Move config file to execution directory
    Move py file with your saved configurations to the directory you would like to run it from.  I am just running this from my home dir. 
    ```shell
    mv mudpitoinflux3.py ~/
    ```
1. Add to supervisor config
    If you would like this file to run automatically on startup and restart on failures it's good to added it to supervisor.  Just like Mudpi is running. 
    Navigate to sup supervisor directory <br/>
    ```shell
    cd /etc/supervisor/conf.d
    ```
    Create new conf file for mudpitoinflux3 script <br/>
    ```shell
    sudo nano mudpitoinflux3.conf 
    ```
    Paste the following code in the file.  I have my script running out of my home directory.  If you want it to run from a different location you can create that and update this config here. <br/>
    ```
    [program:mudpitoinflux3]
    directory=/home/pi
    user=pi
    command=python3 -u /home/pi/mudpitoinflux3.py
    autostart=true
    autorestart=true
    stderr_logfile=/home/pi/logs/mudpitoinflux3.err.log
    stdout_logfile=/home/pi/logs/mudpitoinflux3.out.log 
    ``` 
    Enter Keys <code> ctl + o </code>  then <code>Enter </code> - to save the file  <br/>
    Enter Keys <code>ctl + x </code> – to exit <br/> 
    Start Supervisor 
    ```shell
    sudo supervisorctl update

    sudo supervisorctl start mudpitoinflux3
    ```
    To check the status
    ```shell
    sudo supervisorctl start mudpitoinflux3
    ```
    or review error log in the location you specified in the supervisor config file
## Confirming Influx is collecting data 
1. Connect to influx
    Go to home dir
    ```shell 
    cd ~ 
    ```
    ```shell 
    influx 
    ```
1. Select the home database (or the table you configured the mudpitoinflux3.py to write to)
    ```shell 
    use home 
    ```
1. List and query measurements being collected   
   ```shell 
    show measurements 
    ```
    You should see your sensors by name listed here.  Select one and use it in the query below. 
    ```sql 
    Select * from <measurement> limit 100 
    ```
    This will display the data in the measurement of the time series database. If you see your data you are good to go.  
    ![influx Results](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/influxquery.png)

## Building a Grafana Dashboard
1. Log into Grafana 
    Open a browser and navigate to your Pi IP address ``` http://<your.rpi.address>:3000 ```
1. Create new data source <br/> 
    Navigate to ``` Configuration > Data Sources ```
    Search for "Influx"
    ![search for influx](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/SelectInfluxDataSource.png) <br/>
    Below is my configuration and is fairly standard if you installed Grafana on the same raspberry pi as Mudpi and influx <br/>
    ![influxconfig1](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/InfluxConfiguration1.png) <br/>
    ![influxconfig2](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/InfluxConfiguration2.png) <br/>
1. Create new Dashboard 
![GrafanaQuery](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/GrafanaQuery.gif)<br/>
![GrafanaSettings](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/GrafanaSettings.png)<br/>
![GrafanaSettings1](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/GrafanaSettings1.png)<br/>
![influxconfig2](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/InfluxConfiguration2.png)<br/>
## Enabling Email Alerting 
To use alerting you must set up a Notification Channel.  Grafana supports a large range of options [here](https://grafana.com/docs/grafana/latest/alerting/notifications/). 
1. For Email Edit the Grafana Config <br/>
    ![gmailconfig](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/gmailconfig.png)<br/>
1. Set up a notification channel <br/>
    ![notificationChannel](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/notificationChannel.png)    <br/>
1. Edit your dashboard and add alerts <br/>
    ![EmailGardenAlertConfig](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/EmailGardenAlertConfig.png)<br/>
    ![GrafanaAlertConfiguration](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/GrafanaAlertConfiguration.png) <br/>
    ![GrafanaAlertDashboard](https://raw.githubusercontent.com/icyspace/MudPiInflux/master/img/GrafanaAlertDashboard.png)<br/>
# Summary
At this point you should have a low maintenance  solution to collect, view, and be alerted on your garden’s performance.  
<b> Happy Growing! </b>
