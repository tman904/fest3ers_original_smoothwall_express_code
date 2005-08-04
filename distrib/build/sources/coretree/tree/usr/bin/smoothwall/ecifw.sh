#!/bin/sh

. /var/smoothwall/adsl/settings
. /var/smoothwall/adsl/eci/$ECITYPE

echo "Modem is a $FULLNAME"
/usr/bin/eci-load1 $VID1 $PID1 $VID2 $PID2 /etc/eciadsl/$FIRM1
/usr/bin/eci-load2 -t 120 $VID2 $PID2 /etc/eciadsl/$FIRM2
