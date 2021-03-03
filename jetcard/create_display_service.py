import argparse
import getpass
import os
import jetcard.utils

STATS_SERVICE_TEMPLATE = """
[Unit]
Description=JetCard display service

[Service]
Type=simple
User=%s
PermissionsStartOnly=true
ExecStartPre=/bin/chmod 660 %s
ExecStartPre=/bin/chgrp i2c %s
ExecStart=/bin/sh -c "python3 -m jetcard.display_server"
WorkingDirectory=%s
Restart=always

[Install]
WantedBy=multi-user.target
"""

STATS_SERVICE_NAME = 'jetcard_display'


def get_stats_service():
    i2c_bus_path = "/sys/bus/i2c/drivers/ina3221x/7-0040/iio:device0/in_power0_input"
    # chip_id = int(os.popen("cat /sys/module/tegra_fuse/parameters/tegra_chip_id").read())
    if jetcard.utils.platform_is_nano():
    #if chip_id in [33]:
        i2c_bus_path = "/sys/devices/50000000.host1x/546c0000.i2c/i2c-6/6-0040/iio:device0/in_power0_input"
    else:
        i2c_bus_path = "/sys/bus/i2c/drivers/ina3221x/7-0040/iio:device0/in_power0_input"

    return STATS_SERVICE_TEMPLATE % (getpass.getuser(), i2c_bus_path, i2c_bus_path, os.environ['HOME'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='jetcard_display.service')
    args = parser.parse_args()

    with open(args.output, 'w') as f:
        f.write(get_stats_service())
