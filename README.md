# Gratipay Bot!

This repo holds the source code for [**@gratipay-bot**](https://github/gratipay-bot).


## Deployment

Here's how to install Gratipay Bot on a fresh Ubuntu 14.04 server:

```bash
apt-get install unattended-upgrades
dpkg-reconfigure unattended-upgrades

apt-get install git
git clone https://github.com/gratipay/bot.git
cd bot

apt-get install python3.4-venv
python3 -m venv env
env/bin/pip install --upgrade pip

./update.sh
```

Note that Gratipay Bot also kicks off team review tickets from inside the [web
app](/gratipay/gratipay.com).
