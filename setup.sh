pip install -r requirements.txt

cd /opt/hidscanner2mqtt/ \
    && sudo cp systemd/hidscanner2mqtt.service /etc/systemd/system/hidscanner2mqtt.service \
    && sudo systemctl daemon-reload \
    && sudo systemctl enable hidscanner2mqtt.service \
    && sudo systemctl restart hidscanner2mqtt.service \
    && sudo systemctl status hidscanner2mqtt.service
