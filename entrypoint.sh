#!/bin/bash
printenv | grep -v "no_proxy" >> /etc/environment

/bin/sh -c cron && tail -f /var/log/cron.log