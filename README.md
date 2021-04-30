# Bitcoin Black (BCB) Wallet Server

## Requirements

**Requires Python 3.6 or Newer**

Install requirements on Ubuntu 18.04:
```
apt install python3 python3-dev libdpkg-perl virtualenv nginx
```

Minimum of one **BCB Node** with RPC enabled.

**Redis server** running on the default port 6379

On debian-based systems

```
sudo apt install redis-server
```

## Installation

Generally:

1) Run the app under a dedicated user
2) Clone the repository
3) Configuration
4) Run

```
sudo adduser blackuser # Add blackuser
sudo usermod -aG sudo blackuser # Add blackuser to sudo group
sudo usermod -aG www-data blackuser # Add blackuser to www-data group
sudo su - blackuser # Change to blackuser
git clone https://github.com/tundak/natrium-wallet-server.git balckcast # Clone repository
```

Ensure python3.6 or newer is installed (`python3 --version`) and

```
cd balckcast
git checkout black
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

You must configure using environment variables. You may do this manually, as part of a launching script, in your bash settings, or within a systemd service.

Create the file `.env` in the same directory as `natriumcast.py` with the contents:

```
RPC_URL=http://[::1]:9076 # NANO/BANANO node RPC URL
DEBUG=0                   # Debug mode (0 is off)
FCM_API_KEY=None          # (Optional) Firebase Legacy API KEY (From Firebase Console)
FCM_SENDER_ID=1234        # (Optional) Firebase Sender ID (From Firebase Console)
```

## Running

The recommended configuration is to run the server behind [nginx](https://www.nginx.com/), which will act as a reverse proxy

Next, we'll define a systemd service unit

/etc/systemd/system/balckcast@.service
```
[Unit]
Description=Balck Server
After=network.target

[Service]
Type=simple
User=blackuser
Group=www-data
EnvironmentFile=/home/blackuser/balckcast/.env
WorkingDirectory=/home/blackuser/balckcast
ExecStart=/home/blackuser/balckcast/venv/bin/python natriumcast.py -b --host 127.0.0.1 --port %i --log-file /tmp/balckcast%i.log
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable this service and start it, ensure all is working as expected

```
sudo systemctl enable balckcast@5076
sudo systemctl start balckcast@5076
sudo systemctl status balckcast@5076
```

Next, configure nginx to proxy requests to this server

/etc/nginx/sites-available/app.natrium.io

```
upstream black_nodes {
        least_conn;

        server 127.0.0.1:5076;
}

server {
        server_name wsbeta.bitcoinblack.info;

        location / {
                proxy_pass http://black_nodes;
                proxy_redirect off;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_http_version 1.1;
                proxy_set_header Host $host;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
        }
}

```

Enable this configuration and restart nginx

```
sudo ln -s /etc/nginx/sites-available/wsbeta.bitcoinblack.info /etc/nginx/sites-enabled/wsbeta.bitcoinblack.info
sudo service nginx restart
```

## Let's encrypt

```
sudo add-apt-repository ppa:certbot/certbot
sudo apt update
sudo apt install python-certbot-nginx 
sudo certbot --nginx
```

## Work Server

This server relies on the node for work with the `use_peers` option set to `true`. So you should define your work peers in the config.json as below (if you have any):

```
work_peers: [
  "::ffff:127.0.0.1:5555"
]
```

dPOW support has been removed, because it is recommended to use [Betsy](https://github.com/bbedward/betsy-middleware) if you need that.

## Callback

Callback is required for push notifications and pushing new blocks to clients. This can be configured in the node's config.json as follows:

```
"callback_address": "::ffff:127.0.0.1",
"callback_port": "5076",
"callback_target": "\/callback",
```

## [optional] haproxy node load balancing
Multiple nodes may run on the same server as long as you change the RPC binding port for each. Same for the peering port.
```
global
        log /dev/log    local0
        log /dev/log    local1 notice
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin
        stats timeout 30s
        user haproxy
        group haproxy
        daemon

        # Default SSL material locations
        ca-base /etc/ssl/certs
        crt-base /etc/ssl/private

        # Default ciphers to use on SSL-enabled listening sockets.
        # For more information, see ciphers(1SSL). This list is from:
        #  https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/
        # An alternative list with additional directives can be obtained from
        #  https://mozilla.github.io/server-side-tls/ssl-config-generator/?server=haproxy
        ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!MD5:!DSS
        ssl-default-bind-options no-sslv3

defaults
        log     global
        mode    http
        option  httplog
        option  dontlognull
        timeout connect 5000
        timeout client  50000
        timeout server  50000
        errorfile 400 /etc/haproxy/errors/400.http
        errorfile 403 /etc/haproxy/errors/403.http
        errorfile 408 /etc/haproxy/errors/408.http
        errorfile 500 /etc/haproxy/errors/500.http
        errorfile 502 /etc/haproxy/errors/502.http
        errorfile 503 /etc/haproxy/errors/503.http
        errorfile 504 /etc/haproxy/errors/504.http

frontend rpc-frontend
        bind <this host IP or 127.0.0.1 if same host>:<port>         # different than the default RPC port on a single node
        mode http
        default_backend rpc-backend
        
backend rpc-backend
        balance first
        mode http
        option forwardfor
        timeout server 1000
        option redispatch
        server rpcbackend1 <node 1 server or localhost>:<rpc port> check
        server rpcbackend2 <node 2 server or localhost>:<rpc port> check
        server rpcbackend3 <node 3 server or localhost>:<rpc port> check
```
