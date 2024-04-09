# How setup an MQTT broker

## Cloud hosting
This is the easiest/hassle-free setup. There are several options for providers. One of the most used ones is HiveMQ, which we'll be convering here:

#### Setup
1. Register: https://console.hivemq.cloud
2. Bring up an AWS broker instance (with the free plan, you can get 100 MQTT clients & 10 GB traffic/month)
3. In the "OVERVIEW" you can check your broker's config (URL, ports...)
4. In the "ACCESS MANAGEMENT" you can create MQTT client credentials.

#### Testing
You can test your broker using e.g. MQTT Explorer or the [HiveMQ websocket client](https://www.hivemq.com/demos/websocket-client/).

## Local (on premises) hosting

### Mosquitto MQTT Broker (using docker)

#### Setup
These instructions will work on any Debian based OS  

_By default the config allows only to use local connections for security reasons but since authentication is enabled below, that's not the case._

1. Install `docker` and `docker-compose`

2. Create base folder for mqtt configuration

```bash
mkdir mqtt5
cd mqtt5

# for storing mosquitto.conf and pwfile (for password)
mkdir config
```

3. Create Mosquitto config file - mosquitto.conf
```bash
nano config/mosquitto.conf
```

Basic configuration file content below including websocket config
```
allow_anonymous false
listener 1883
listener 9001
protocol websockets
persistence true
password_file /mosquitto/config/pwfile
persistence_file mosquitto.db
persistence_location /mosquitto/data/
```

4. Create Mosquitto password file - pwfile

```bash
touch config/pwfile
```

5. From the `protocols/mqtt` dir: `sudo docker-compose -p mqtt5 up -d`

6. Get in the container and create a user/password in the pwfile. Here are some example commands for user administration:

```bash
# login interactively into the mqtt container
sudo docker exec -it <container-id> sh

# Create new password file and add user and it will prompt for password
mosquitto_passwd -c /mosquitto/config/pwfile user1

# Add additional users (remove the -c option) and it will prompt for password
mosquitto_passwd /mosquitto/config/pwfile user2

# delete user command format
mosquitto_passwd -D /mosquitto/config/pwfile <user-name-to-delete>
```


7. Restart the container 
```bash
sudo docker restart <container-id>
```

#### Testing

You can test using a dummy client on the MQTT server.

1. Install mosquitto client tools for testing: 
```bash
sudo apt install mosquitto-clients
```

2. Start a subscriber with topic name: `'hello/topic'`

```bash
# Without authentication
mosquitto_sub -v -t 'hello/topic'

# With authentication
mosquitto_sub -v -t 'hello/topic' -u user1 -P <password>

# Alternate way in url format
# Format => mqtt(s)://[username[:password]@]host[:port]/topic
mosquitto_sub -v -L mqtt://user1:pwd1@localhost:1883/hello/topic
```

3. Start publising to that topic

```bash
# Without authentication
mosquitto_pub -t 'hello/topic' -m 'hello MQTT'

# With authentication
mosquitto_pub -t 'hello/topic' -m 'hello MQTT' -u user1 -P <password>

# Alternate way in url format 
# Format => mqtt(s)://[username[:password]@]host[:port]/topic
mosquitto_pub -L mqtt://user1:user1Password@localhost:1883/hello/topic -m 'hello MQTT'
```
