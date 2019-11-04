# Asterisk Call History

This application shows the call history of all calls from asterisk server (Master.csv).

## Installation
```
cd /opt/
sudo git clone https://github.com/bkbilly/Asterisk-Call-History.git
cd /opt/Asterisk-Call-History/
sudo pip install -r /opt/Asterisk-Call-History/requirements.txt
sudo cp /opt/Asterisk-Call-History/configuration_template.json /opt/Asterisk-Call-History/configuration.json
sudo chmod +x /opt/Asterisk-Call-History/asteriskcallhistory
sudo ln -s /opt/Asterisk-Call-History/asteriskcallhistory /etc/init.d/asteriskcallhistory
sudo update-rc.d asteriskcallhistory defaults
sudo service asteriskcallhistory start
```

## How to use configuration.json

* `options.callDataFile` (str) Location of the Master.csv file
* `options.externalNumbers` (list str) The external numbers using the Asterisk Regular Expression format
* `options.internalNumbers` (list str) The internal numbers using the Asterisk Regular Expression format

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
