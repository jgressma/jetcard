import argparse
import getpass
import os

STATS_SERVICE_TEMPLATE = """
[Unit]
Description=JetCard display service

[Service]
Type=simple
User=%s
PermissionsStartOnly=true
ExecStartPre=/bin/chmod 660 /sys/bus/i2c/drivers/ina3221x/7-0040/iio:device0/in_power0_input
ExecStartPre=/bin/chgrp i2c /sys/bus/i2c/drivers/ina3221x/7-0040/iio:device0/in_power0_input
ExecStart=/bin/sh -c "python3 -m jetcard.display_server"
WorkingDirectory=%s
Restart=always

[Install]
WantedBy=multi-user.target
"""

STATS_SERVICE_NAME = 'jetcard_display'


def get_stats_service():
    return STATS_SERVICE_TEMPLATE % (getpass.getuser(), os.environ['HOME'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='jetcard_display.service')
    args = parser.parse_args()

    with open(args.output, 'w') as f:
        f.write(get_stats_service())
