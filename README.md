# Asterisk Call History

This application shows the call history of all calls from asterisk server (Master.csv).

## Installation
```
sudo git clone https://github.com/bkbilly/Asterisk-Call-History.git /opt/Asterisk-Call-History
sudo pip install -r /opt/Asterisk-Call-History/requirements.txt
sudo cp /opt/Asterisk-Call-History/configuration_template.json /opt/Asterisk-Call-History/configuration.json

sudo cp /opt/Asterisk-Call-History/autostart/asteriskcallhistory.service /etc/systemd/system/asteriskcallhistory.service
sudo chmod +x /etc/systemd/system/asteriskcallhistory.service
sudo systemctl enable asteriskcallhistory
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
