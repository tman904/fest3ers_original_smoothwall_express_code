#! /usr/bin/perl

# 32- and 64-bit are different
my $sysType, $pattern, $structSize;
$sysType=`uname -m`;
$pattern = "l!l!ssl";
$structSize = 24 if ($sysType =~ "x86_64");
$structSize = 16 if ($sysType =~ "i.86");

# Find which input device is the power button
$getH = 0;
$event = "";
while ($event eq "") {
  open (eventHDL, "</proc/bus/input/devices");
  while (<eventHDL>) {
    next unless (/^S:.*LNXPWRBN/ or /^H:/);
    if (/^S:.*LNXPWRBN/) {
      $getH = 1;
      next;
    }
    if ($getH and /^H:/) {
      chomp;
      @hFields = split;
      $event = $hFields[2];
      close (eventHDL);
      break;
    }
  }

  # Clearly didn't find it, so wait minute and try again
  if ($event ne "") {
    break;
  } else {
    close (eventHDL);
    sleep 60;
  }
}

# Open the power button event node
open (eventHDL, "</dev/input/$event");
while (true) {
  if (sysread(eventHDL, $buf, $structSize) == $structSize) {
    # Unpack the structure
    ($a, $b, $type, $code, $value) = unpack($pattern, $buf);
    # And shut down if the stars align
    if ($type == 1 and $code == 116 and $value == 1) {
      system('logger -t "powerControl" "Power button pressed; shutting down..."');
      system('shutdown -h -P -t 2 now "Power button pressed"');
    }
  } else {
    close (eventHDL);
    sleep 10;
    open (eventHDL, "</dev/input/$event");
  }
}

