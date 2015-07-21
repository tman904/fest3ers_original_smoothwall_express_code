#!/usr/bin/perl
#
# SmoothWall CGIs
#
# (c) SmoothWall Ltd, 2005

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );

my $version = "1.0.0";

my %apcupsdsettings;
my %checked; my %selected;

&showhttpheaders();

$apcupsdsettings{'ACTION'} = '';
$apcupsdsettings{'VALID'} = '';
$apcupsdsettings{'ENABLE'} = 'off';
$apcupsdsettings{'STANDALONE'} = '';
$apcupsdsettings{'UPSIP'} = '';
$apcupsdsettings{'UPSPORT'} = '';
$apcupsdsettings{'ALERTADDR'} = '';
$apcupsdsettings{'CC1ADDR'} = '';
$apcupsdsettings{'CC2ADDR'} = '';
$apcupsdsettings{'UPSUSER'} = '';
$apcupsdsettings{'UPSAUTH'} = '';
$apcupsdsettings{'POLLTIME'} = '60';
$apcupsdsettings{'BATTLEVEL'} = '15';
$apcupsdsettings{'RTMIN'} = '10';
$apcupsdsettings{'BATTDELAY'} = '10';
$apcupsdsettings{'MAILSVR'} = '';
$apcupsdsettings{'FROMADDR'} = '';
$apcupsdsettings{'UPSMODE'} = '';
$apcupsdsettings{'TESTING'} = 'off';
$apcupsdsettings{'TO'} = '0';
$apcupsdsettings{'ANNOY'} = '300';
$apcupsdsettings{'NISPORT'} = '3551';
$apcupsdsettings{'UPSNAME'} = '';
$apcupsdsettings{'KILLPOWER'} = 'off';
$apcupsdsettings{'MSGPOWEROUT'} = 'off';
$apcupsdsettings{'MSGPOWERBACK'} = 'off';
$apcupsdsettings{'MSGKILLPOWER'} = 'off';
$apcupsdsettings{'MSGEMERGENCY'} = 'off';
$apcupsdsettings{'MSGCHANGEME'} = 'off';
$apcupsdsettings{'MSGFAILING'} = 'off';
$apcupsdsettings{'MSGANNOY'} = 'off';
$apcupsdsettings{'MSGCOMMFAILURE'} = 'off';
$apcupsdsettings{'MSGCOMMOK'} = 'off';
$apcupsdsettings{'MSGONBATTERY'} = 'off';
$apcupsdsettings{'MSGOFFBATTERY'} = 'off';
$apcupsdsettings{'MSGTIMEOUT'} = 'off';
$apcupsdsettings{'MSGLOADLIMIT'} = 'off';
$apcupsdsettings{'MSGRUNLIMIT'} = 'off';
$apcupsdsettings{'MSGDOSHUTDOWN'} = 'off';
$apcupsdsettings{'MSGREMOTEDOWN'} = 'off';
$apcupsdsettings{'MSGSTARTSELFTEST'} = 'off';
$apcupsdsettings{'MSGENDSELFTEST'} = 'off';
$apcupsdsettings{'MSGBATTATTACH'} = 'off';
$apcupsdsettings{'MSGBATTDETACH'} = 'off';

&getcgihash(\%apcupsdsettings);

my $errormessage = '';

if ($apcupsdsettings{'ACTION'} eq $tr{'save&restart'})
{
	if ((($apcupsdsettings{'UPSMODE'} eq '0')
	  or ($apcupsdsettings{'UPSMODE'} eq '1')
	  or ($apcupsdsettings{'UPSMODE'} eq '2')
	  or ($apcupsdsettings{'UPSMODE'} eq '3')
	  or ($apcupsdsettings{'UPSMODE'} eq '5')) && ($apcupsdsettings{'TO'}) ne '0')
        {
        $errormessage = 'Please leave \'Shutdown after time On Battery\' 0 (Disabled) for SmartUPS & Modbus';
        goto ERROR;       
        }

	if  ((($apcupsdsettings{'UPSMODE'} eq '1') or ($apcupsdsettings{'UPSMODE'} eq '3')
	  or ($apcupsdsettings{'UPSMODE'} eq '5')) && ($apcupsdsettings{'UPSPORT'}) ne '' )
        {
        $errormessage = 'Please leave Serial Port blank for USB & PCNET';
        goto ERROR;
        }

	if ($apcupsdsettings{'UPSMODE'} eq '5' && (!(&validip($apcupsdsettings{'UPSIP'}))))
        {
	 $errormessage = 'Invalid UPS IP Address';
	 delete $apcupsdsettings{'UPSIP'};
	 goto ERROR;
	 }

 	 if ($apcupsdsettings{'UPSMODE'} eq '5' && $apcupsdsettings{'UPSUSER'} eq '' ) 
	 {
	 $errormessage = 'Please enter a username';
        goto ERROR;
	 }
        
	if ($apcupsdsettings{'UPSMODE'} eq '5' && $apcupsdsettings{'UPSAUTH'} eq '' )
        {
        $errormessage = 'Please enter a password';
        goto ERROR;
        }

	if (($apcupsdsettings{'UPSMODE'} eq '0')
	 or ($apcupsdsettings{'UPSMODE'} eq '2')
	 or ($apcupsdsettings{'UPSMODE'} eq '6')
	 or ($apcupsdsettings{'UPSMODE'} eq '7')
	 or ($apcupsdsettings{'UPSMODE'} eq '8')
	 or ($apcupsdsettings{'UPSMODE'} eq '9')
	 or ($apcupsdsettings{'UPSMODE'} eq '10')
	 or ($apcupsdsettings{'UPSMODE'} eq '11')
	 or ($apcupsdsettings{'UPSMODE'} eq '12')
	 or ($apcupsdsettings{'UPSMODE'} eq '13')
	 or ($apcupsdsettings{'UPSMODE'} eq '14')
	 or ($apcupsdsettings{'UPSMODE'} eq '15')
	 or ($apcupsdsettings{'UPSMODE'} eq '16')
	 or ($apcupsdsettings{'UPSMODE'} eq '17')
	 or ($apcupsdsettings{'UPSMODE'} eq '18'))
        {
           unless ($apcupsdsettings{'UPSPORT'} =~ /^\/dev\/tty[A-Z][0-9]/ )
            {
            $errormessage = 'Please enter a valid Serial Port <BR>e.g. /dev/ttyS0';
            goto ERROR;
            }
        }

	if ((($apcupsdsettings{'UPSMODE'} eq '6')
	  or ($apcupsdsettings{'UPSMODE'} eq '7')
	  or ($apcupsdsettings{'UPSMODE'} eq '8')
	  or ($apcupsdsettings{'UPSMODE'} eq '9')
	  or ($apcupsdsettings{'UPSMODE'} eq '10')
	  or ($apcupsdsettings{'UPSMODE'} eq '11')
	  or ($apcupsdsettings{'UPSMODE'} eq '12')
	  or ($apcupsdsettings{'UPSMODE'} eq '13')
	  or ($apcupsdsettings{'UPSMODE'} eq '14')
	  or ($apcupsdsettings{'UPSMODE'} eq '15')
	  or ($apcupsdsettings{'UPSMODE'} eq '16')
	  or ($apcupsdsettings{'UPSMODE'} eq '17')
	  or ($apcupsdsettings{'UPSMODE'} eq '18')) && ($apcupsdsettings{'TO'}) <= '119')
         {
         $errormessage = 'Please select a \'Shutdown after time On Battery\' of at least 120 seconds for simple signalling';
	  goto ERROR;
         }

	if ((($apcupsdsettings{'UPSMODE'} eq '0')
	  or ($apcupsdsettings{'UPSMODE'} eq '1')
	  or ($apcupsdsettings{'UPSMODE'} eq '2')
	  or ($apcupsdsettings{'UPSMODE'} eq '3')
	  or ($apcupsdsettings{'UPSMODE'} eq '6')
	  or ($apcupsdsettings{'UPSMODE'} eq '7')
	  or ($apcupsdsettings{'UPSMODE'} eq '8')
	  or ($apcupsdsettings{'UPSMODE'} eq '9')
	  or ($apcupsdsettings{'UPSMODE'} eq '10')
	  or ($apcupsdsettings{'UPSMODE'} eq '11')
	  or ($apcupsdsettings{'UPSMODE'} eq '12')
	  or ($apcupsdsettings{'UPSMODE'} eq '13')
	  or ($apcupsdsettings{'UPSMODE'} eq '14')
	  or ($apcupsdsettings{'UPSMODE'} eq '15')
	  or ($apcupsdsettings{'UPSMODE'} eq '16')
	  or ($apcupsdsettings{'UPSMODE'} eq '17')
	  or ($apcupsdsettings{'UPSMODE'} eq '18')) && ($apcupsdsettings{'UPSIP'}) ne '')
         {
         $errormessage = 'Please leave IP Address blank when directly connected via Serial or USB cable';
	  goto ERROR;
         }

 	if ($apcupsdsettings{'UPSMODE'} ne '5' && $apcupsdsettings{'UPSUSER'} ne '' ) 
	  {
	  $errormessage = 'User name not required unless using PCNET';
         goto ERROR;
	  }

	if ($apcupsdsettings{'UPSMODE'} ne '5' && $apcupsdsettings{'UPSAUTH'} ne '' )
         {
         $errormessage = 'Password not required unless using PCNET';
         goto ERROR;
         }


	if ($apcupsdsettings{'UPSMODE'} eq '4' && ($apcupsdsettings{'TO'}) eq '')
         {
         $errormessage = 'Please enter a \'Shutdown after time On Battery\' value, or enter "0" (zero) to disable.';
         goto ERROR; 
         }

	if ($apcupsdsettings{'UPSMODE'} eq '4' && ($apcupsdsettings{'UPSPORT'}) ne '' )
         {
         $errormessage = 'Please leave Serial Port blank for SLAVE working';
         goto ERROR;
         }

	if ($apcupsdsettings{'UPSMODE'} eq '4' && ($apcupsdsettings{'KILLPOWER'}) eq 'on')
         {
         $errormessage = '<B>UPS Killpower on shutdown</B> is not compatible with SLAVE working.<BR>Only available for MASTER (e.g. directly connected via USB or Serial) systems.';
         goto ERROR;
         }

	if ($apcupsdsettings{'UPSMODE'} eq '4' && ($apcupsdsettings{'UPSIP'}) eq '')
         {
         $errormessage = 'Please enter a valid IP Address for the Master Controller.';
         goto ERROR;
         }

	if ($apcupsdsettings{'POLLTIME'} >= 301 || $apcupsdsettings{'POLLTIME'} <= 19 ) 
         {
         $errormessage = 'Invalid Poll time, enter a value between 20 and 300';
         delete $apcupsdsettings{'POLLTIME'};
	  goto ERROR;
	  }

	unless ($apcupsdsettings{'FROMADDR'} =~ (/^[A-z0-9_\-\.]+[@][A-z0-9_\-.]+[A-z]{2,}$/))
         {
         $errormessage = 'Please enter a valid From address';
         delete $apcupsdsettings{'FROMADDR'};
         goto ERROR;
         }

	unless ($apcupsdsettings{'ALERTADDR'} =~ (/^[A-z0-9_\-\.]+[@][A-z0-9_\-.]+[A-z]{2,}$/))
	 {
	 $errormessage = 'Please enter a valid Alert address';
	 delete $apcupsdsettings{'ALERTADDR'};
	 goto ERROR;
	 }

	 if ($apcupsdsettings{'CC1ADDR'} ne '') {
	 unless ($apcupsdsettings{'CC1ADDR'} =~ (/^[A-z0-9_\-\.]+[@][A-z0-9_\-.]+[A-z]{2,}$/))
	 {
	 $errormessage = 'Please enter a valid Alert2 address';
	 delete $apcupsdsettings{'CC1ADDR'};
	 goto ERROR;
	 }}

	if ($apcupsdsettings{'CC2ADDR'} ne '') {
		unless ($apcupsdsettings{'CC2ADDR'} =~ (/^[A-z0-9_\-\.]+[@][A-z0-9_\-.]+[A-z]{2,}$/))
	 {
	 $errormessage = 'Please enter a valid Alert3 address';
	 delete $apcupsdsettings{'CC2ADDR'};
	 goto ERROR;
	 }}

	if ($apcupsdsettings{'MAILSVR'} eq '')
	 {
	 $errormessage = 'Please enter valid mailserver';
	 delete $apcupsdsettings{'MAILSVR'};
	 goto ERROR;
	 }

        if ($apcupsdsettings{'BATTLEVEL'} >= 96 || $apcupsdsettings{'BATTLEVEL'} <= 4 )
        {
        $errormessage = 'Please enter % of battery remaining between 5 and 95';
	 delete $apcupsdsettings{'BATTLEVEL'};
        goto ERROR;
        }

        if ($apcupsdsettings{'BATTDELAY'} >= 301 || $apcupsdsettings{'BATTDELAY'} <= -1 )
        {
        $errormessage = 'Invalid on battery response delay, enter a value between 0 and 300';
        delete $apcupsdsettings{'BATTDELAY'};
        goto ERROR;
        }

        if ($apcupsdsettings{'RTMIN'} <= 4 )
        {
        $errormessage = 'Invalid minimum runtime, enter a value of 5 or greater';
	 delete $apcupsdsettings{'RTMIN'};
        goto ERROR;
        }

        if (length $apcupsdsettings{'UPSNAME'} > 8)
        {
        $errormessage = 'Please use 8 characters or less for UPS name';
        delete ($apcupsdsettings{'UPSNAME'});
        goto ERROR;
        }

        if ($apcupsdsettings{'ANNOY'} eq '')
        {
        $errormessage = 'Please enter Annoy Message Period<BR>Default is 300 Seconds.';
        delete ($apcupsdsettings{'ANNOY'});
        goto ERROR;
        }

ERROR:
	if ($errormessage) {
                $apcupsdsettings{'VALID'} = 'no'; }		
       else {
                $apcupsdsettings{'VALID'} = 'yes'; }

	if ($apcupsdsettings{'VALID'} eq 'yes') {
		
		&log("APCupsd service restarted.");
	
		&writehash("/var/smoothwall/apcupsd/settings", \%apcupsdsettings);
		
		system("/usr/bin/smoothwall/writeapcupsdconf.pl");
		system("smoothcom apcupsdkillpwr");
		
		my $success = message("apcupsdrestart");
		
		if (not defined $success) {
			$errormessage = $tr{'smoothd failure'}; }
	}
}

if ($apcupsdsettings{'ACTION'} eq '' )
{
	$apcupsdsettings{'ENABLE'} = 'off';
	$apcupsdsettings{'NOLOGINTYPE'} = '0';
	$apcupsdsettings{'OPMODE'} = 'testing';

if (-e "/var/smoothwall/apcupsd/settings") {
	&readhash("/var/smoothwall/apcupsd/settings", \%apcupsdsettings);
	}
}

if ($apcupsdsettings{'ACTION'} eq $tr{'restart'})
{
	&log("APCupsd service restarted.");

	my $success = message("apcupsdrestart");
		if (not defined $success) {
			$errormessage = $tr{'smoothd failure'}; }
}

if ($apcupsdsettings{'ACTION'} eq $tr{'stop'})
{
	&log("APCupsd service stopped.");

	my $success = message("apcupsdstop");
		if (not defined $success) {
			$errormessage = $tr{'smoothd failure'}; }
}

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$apcupsdsettings{'ENABLE'}} = 'CHECKED';

$selected{'OPMODE'}{'testing'} = '';
$selected{'OPMODE'}{'full'} = '';
$selected{'OPMODE'}{$apcupsdsettings{'OPMODE'}} = 'SELECTED';

$checked{'STANDALONE'}{'off'} = '';
$checked{'STANDALONE'}{'on'} = '';
$checked{'STANDALONE'}{$apcupsdsettings{'STANDALONE'}} = 'CHECKED';

$checked{'SHELLLOGIN'}{'off'} = '';
$checked{'SHELLLOGIN'}{'on'} = '';
$checked{'SHELLLOGIN'}{$apcupsdsettings{'SHELLLOGIN'}} = 'CHECKED';

$checked{'KILLPOWER'}{'off'} = '';
$checked{'KILLPOWER'}{'on'} = '';
$checked{'KILLPOWER'}{$apcupsdsettings{'KILLPOWER'}} = 'CHECKED';

$selected{'UPSMODE'}{'0'} = '';
$selected{'UPSMODE'}{'1'} = '';
$selected{'UPSMODE'}{'2'} = '';
$selected{'UPSMODE'}{'3'} = '';
$selected{'UPSMODE'}{'4'} = '';
$selected{'UPSMODE'}{'5'} = '';
$selected{'UPSMODE'}{'6'} = '';
$selected{'UPSMODE'}{'7'} = '';
$selected{'UPSMODE'}{'8'} = '';
$selected{'UPSMODE'}{'9'} = '';
$selected{'UPSMODE'}{'10'} = '';
$selected{'UPSMODE'}{'11'} = '';
$selected{'UPSMODE'}{'12'} = '';
$selected{'UPSMODE'}{'13'} = '';
$selected{'UPSMODE'}{'14'} = '';
$selected{'UPSMODE'}{'15'} = '';
$selected{'UPSMODE'}{'16'} = '';
$selected{'UPSMODE'}{'17'} = '';
$selected{'UPSMODE'}{'18'} = '';
$selected{'UPSMODE'}{$apcupsdsettings{'UPSMODE'}} = 'SELECTED';

$selected{'NOLOGINTYPE'}{'0'} = '';
$selected{'NOLOGINTYPE'}{'1'} = '';
$selected{'NOLOGINTYPE'}{'2'} = '';
$selected{'NOLOGINTYPE'}{'3'} = '';
$selected{'NOLOGINTYPE'}{$apcupsdsettings{'NOLOGINTYPE'}} = 'SELECTED';

$checked{'MSGPOWEROUT'}{'off'} = '';
$checked{'MSGPOWEROUT'}{'on'} = '';
$checked{'MSGPOWEROUT'}{$apcupsdsettings{'MSGPOWEROUT'}} = 'CHECKED';

$checked{'MSGPOWERBACK'}{'off'} = '';
$checked{'MSGPOWERBACK'}{'on'} = '';
$checked{'MSGPOWERBACK'}{$apcupsdsettings{'MSGPOWERBACK'}} = 'CHECKED';

$checked{'MSGKILLPOWER'}{'off'} = '';
$checked{'MSGKILLPOWER'}{'on'} = '';
$checked{'MSGKILLPOWER'}{$apcupsdsettings{'MSGKILLPOWER'}} = 'CHECKED';

$checked{'MSGEMERGENCY'}{'off'} = '';
$checked{'MSGEMERGENCY'}{'on'} = '';
$checked{'MSGEMERGENCY'}{$apcupsdsettings{'MSGEMERGENCY'}} = 'CHECKED';

$checked{'MSGCHANGEME'}{'off'} = '';
$checked{'MSGCHANGEME'}{'on'} = '';
$checked{'MSGCHANGEME'}{$apcupsdsettings{'MSGCHANGEME'}} = 'CHECKED';

$checked{'MSGFAILING'}{'off'} = '';
$checked{'MSGFAILING'}{'on'} = '';
$checked{'MSGFAILING'}{$apcupsdsettings{'MSGFAILING'}} = 'CHECKED';

$checked{'MSGANNOY'}{'off'} = '';
$checked{'MSGANNOY'}{'on'} = '';
$checked{'MSGANNOY'}{$apcupsdsettings{'MSGANNOY'}} = 'CHECKED';

$checked{'MSGCOMMFAILURE'}{'off'} = '';
$checked{'MSGCOMMFAILURE'}{'on'} = '';
$checked{'MSGCOMMFAILURE'}{$apcupsdsettings{'MSGCOMMFAILURE'}} = 'CHECKED';

$checked{'MSGCOMMOK'}{'off'} = '';
$checked{'MSGCOMMOK'}{'on'} = '';
$checked{'MSGCOMMOK'}{$apcupsdsettings{'MSGCOMMOK'}} = 'CHECKED';

$checked{'MSGONBATTERY'}{'off'} = '';
$checked{'MSGONBATTERY'}{'on'} = '';
$checked{'MSGONBATTERY'}{$apcupsdsettings{'MSGONBATTERY'}} = 'CHECKED';

$checked{'MSGOFFBATTERY'}{'off'} = '';
$checked{'MSGOFFBATTERY'}{'on'} = '';
$checked{'MSGOFFBATTERY'}{$apcupsdsettings{'MSGOFFBATTERY'}} = 'CHECKED';

$checked{'MSGTIMEOUT'}{'off'} = '';
$checked{'MSGTIMEOUT'}{'on'} = '';
$checked{'MSGTIMEOUT'}{$apcupsdsettings{'MSGTIMEOUT'}} = 'CHECKED';

$checked{'MSGLOADLIMIT'}{'off'} = '';
$checked{'MSGLOADLIMIT'}{'on'} = '';
$checked{'MSGLOADLIMIT'}{$apcupsdsettings{'MSGLOADLIMIT'}} = 'CHECKED';

$checked{'MSGRUNLIMIT'}{'off'} = '';
$checked{'MSGRUNLIMIT'}{'on'} = '';
$checked{'MSGRUNLIMIT'}{$apcupsdsettings{'MSGRUNLIMIT'}} = 'CHECKED';

$checked{'MSGDOSHUTDOWN'}{'off'} = '';
$checked{'MSGDOSHUTDOWN'}{'on'} = '';
$checked{'MSGDOSHUTDOWN'}{$apcupsdsettings{'MSGDOSHUTDOWN'}} = 'CHECKED';

$checked{'MSGREMOTEDOWN'}{'off'} = '';
$checked{'MSGREMOTEDOWN'}{'on'} = '';
$checked{'MSGREMOTEDOWN'}{$apcupsdsettings{'MSGREMOTEDOWN'}} = 'CHECKED';

$checked{'MSGSTARTSELFTEST'}{'off'} = '';
$checked{'MSGSTARTSELFTEST'}{'on'} = '';
$checked{'MSGSTARTSELFTEST'}{$apcupsdsettings{'MSGSTARTSELFTEST'}} = 'CHECKED';

$checked{'MSGENDSELFTEST'}{'off'} = '';
$checked{'MSGENDSELFTEST'}{'on'} = '';
$checked{'MSGENDSELFTEST'}{$apcupsdsettings{'MSGENDSELFTEST'}} = 'CHECKED';

$checked{'MSGBATTATTACH'}{'off'} = '';
$checked{'MSGBATTATTACH'}{'on'} = '';
$checked{'MSGBATTATTACH'}{$apcupsdsettings{'MSGBATTATTACH'}} = 'CHECKED';

$checked{'MSGBATTDETACH'}{'off'} = '';
$checked{'MSGBATTDETACH'}{'on'} = '';
$checked{'MSGBATTDETACH'}{$apcupsdsettings{'MSGBATTDETACH'}} = 'CHECKED';

&openpage('apcupsd', 1, '', 'services');

print <<END
<FORM METHOD='POST' action='?'>

<script type="text/javascript">
function ffoxSelectUpdate(elmt)
{
    if(!document.all) elmt.style.cssText = elmt.options[elmt.selectedIndex].style.cssText;
}

</script>
END
;

&alertbox($errormessage);

&openbox('APCupsd:');

print <<END
<TABLE style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<TR>
	<TD CLASS='base' style='width: 25%;'>$tr{'enabled'}</TD>
	<TD><INPUT TYPE='checkbox' NAME='ENABLE' $checked{'ENABLE'}{'on'}></TD>
	<TD CLASS='base' style='width: 48%;'>$tr{'UPS Type'}:</TD>
	<TD>
		<SELECT NAME='UPSMODE' style='width: 175px;'>
		<OPTION VALUE='0' $selected{'UPSMODE'}{'0'}>SmartUPS (Serial)
		<OPTION VALUE='1' $selected{'UPSMODE'}{'1'}>SmartUPS (USB)
		<OPTION VALUE='2' $selected{'UPSMODE'}{'2'}>Modbus (Serial)
		<OPTION VALUE='3' $selected{'UPSMODE'}{'3'}>Modbus (USB)
		<OPTION VALUE='4' $selected{'UPSMODE'}{'4'}>Ethernet (Slave)
		<OPTION VALUE='5' $selected{'UPSMODE'}{'5'}>PCNET (TCP/IP)
		<OPTION VALUE='6' $selected{'UPSMODE'}{'6'}>940-0020B $tr{'Cable'}
		<OPTION VALUE='7' $selected{'UPSMODE'}{'7'}>940-0020C $tr{'Cable'}
		<OPTION VALUE='8' $selected{'UPSMODE'}{'8'}>940-0023A $tr{'Cable'}
		<OPTION VALUE='9' $selected{'UPSMODE'}{'9'}>940-0024B $tr{'Cable'}
		<OPTION VALUE='10' $selected{'UPSMODE'}{'10'}>940-0024C $tr{'Cable'}
		<OPTION VALUE='11' $selected{'UPSMODE'}{'11'}>940-0024G $tr{'Cable'}
		<OPTION VALUE='12' $selected{'UPSMODE'}{'12'}>940-0095A $tr{'Cable'}
		<OPTION VALUE='13' $selected{'UPSMODE'}{'13'}>940-0095B $tr{'Cable'}
		<OPTION VALUE='14' $selected{'UPSMODE'}{'14'}>940-0095C $tr{'Cable'}
		<OPTION VALUE='15' $selected{'UPSMODE'}{'15'}>940-0119A $tr{'Cable'}
		<OPTION VALUE='16' $selected{'UPSMODE'}{'16'}>940-0127A $tr{'Cable'}
		<OPTION VALUE='17' $selected{'UPSMODE'}{'17'}>940-0128A $tr{'Cable'}
		<OPTION VALUE='18' $selected{'UPSMODE'}{'18'}>940-1524C $tr{'Cable'}
		</SELECT>
	</TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'Standalone UPS'}:</TD>
	<TD><INPUT TYPE='checkbox' NAME='STANDALONE' $checked{'STANDALONE'}{'on'}></TD>
	<TD CLASS='base'>$tr{'UPS Polling Interval (Sec)'}:</TD>
	<TD><INPUT TYPE='text' NAME='POLLTIME' style='width: 50px;' VALUE='$apcupsdsettings{'POLLTIME'}'></TD>
<TR>
	<TD CLASS='base'>$tr{'UPS Killpower on Shutdown'}:</TD>
	<TD><INPUT TYPE='checkbox' NAME='KILLPOWER' $checked{'KILLPOWER'}{'on'}></TD>
	<TD CLASS='base'>$tr{'NIS Listening Port'}:<span style='font-size:7pt;'> ($tr{'Leave blank for default'})</span></TD>
	<TD><INPUT TYPE='text' maxlength='5' NAME='NISPORT' style='width: 50px;' VALUE='$apcupsdsettings{'NISPORT'}'></TD>
</TR>
</TABLE>
END
;
&closebox()

&openbox("$tr{'UPS Configuration Information'}:");

print <<END
<TABLE style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<TR>
	<TD CLASS='base'>$tr{'Send Alerts To'}:</TD>
	<TD><INPUT TYPE='text'NAME='ALERTADDR' style='width: 220px;' VALUE='$apcupsdsettings{'ALERTADDR'}'></TD>
	<TD CLASS='base'>$tr{'UPS Serial Port'}:</TD>
	<TD><INPUT TYPE='text'NAME='UPSPORT' style='width: 150px;' VALUE='$apcupsdsettings{'UPSPORT'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'Alert Address'} 2:</TD>
	<TD><INPUT TYPE='text'NAME='CC1ADDR' style='width: 220px;' VALUE='$apcupsdsettings{'CC1ADDR'}'></TD>
	<TD CLASS='base'>$tr{'UPS Name (Max 8 Char)'}:</TD>
	<TD><INPUT TYPE='text' maxlength='8' NAME='UPSNAME' style='width: 150px;' VALUE='$apcupsdsettings{'UPSNAME'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'SMS Email Address'}:</TD>
	<TD><INPUT TYPE='text'NAME='CC2ADDR' style='width: 220px;' VALUE='$apcupsdsettings{'CC2ADDR'}'></TD>
	<TD CLASS='base'>$tr{'Master NIS or UPS IP Address'}:<BR><sup>$tr{'Append'} <span style="color:red">:&lt;$tr{'port'}&gt;</span> $tr{'if not default'} (3551)</sup></TD>
	<TD><INPUT TYPE='text'NAME='UPSIP' style='width: 150px;' VALUE='$apcupsdsettings{'UPSIP'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'Send Alerts From'}:</TD>
	<TD><INPUT TYPE='text'NAME='FROMADDR' style='width: 220px;' VALUE='$apcupsdsettings{'FROMADDR'}'></TD>
	<TD CLASS='base'>$tr{'UPS User name'} (PCNET):</TD>
	<TD><INPUT TYPE='text'NAME='UPSUSER' style='width: 150px;' VALUE='$apcupsdsettings{'UPSUSER'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'Mail Server'}:</TD>
	<TD><INPUT TYPE='text'NAME='MAILSVR' style='width: 220px;' VALUE='$apcupsdsettings{'MAILSVR'}'></TD>
	<TD CLASS='base'>$tr{'UPS Authentication Phrase'} (PCNET):</TD>
	<TD><INPUT TYPE='text'NAME='UPSAUTH' style='width: 150px;' VALUE='$apcupsdsettings{'UPSAUTH'}'></TD>
</TR>
</TABLE>
END
;

&closebox();

&openbox("$tr{'UPS On Battery Configuration'}:");

print <<END
<TABLE style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<TR>
	<TD CLASS='base' style='width: 40%;'>$tr{'Shutdown when battery capacity remains'} (%):</TD>
	<TD style='width: 15%;'><INPUT TYPE='text' style='width: 73px;' NAME='BATTLEVEL' VALUE='$apcupsdsettings{'BATTLEVEL'}'></TD>
	<TD CLASS='base' style='width: 40%;'>$tr{'Shutdown when battery runtime remains (Mins)'}:</TD>
	<TD style='width: 15%;'><INPUT TYPE='text' style='width: 73px;' NAME='RTMIN' VALUE='$apcupsdsettings{'RTMIN'}'></TD>
</TR>
<TR>
	<TD CLASS='base' style='width: 40%;'>$tr{'Wait before responding to On Battery alert (Sec)'}:</TD>
	<TD style='width: 15%;'><INPUT TYPE='text' style='width: 73px;' NAME='BATTDELAY' VALUE='$apcupsdsettings{'BATTDELAY'}'></TD>
	<TD CLASS='base' style='width: 40%;'>$tr{'Shutdown after time On Battery (Sec)'}:<span style='font-size:7pt;'> (0 $tr{'Disables'})</span></TD>
	<TD style='width: 15%;'><INPUT TYPE='text' style='width: 73px;' NAME='TO' VALUE='$apcupsdsettings{'TO'}'></TD>
</TR>
<TR>
	<TD CLASS='base' style='width: 40%;'>$tr{'Deny Shell Login when on battery'}:</TD>
	<TD style='width: 15%;'>
	<SELECT NAME='NOLOGINTYPE'>
	<OPTION VALUE='0' $selected{'NOLOGINTYPE'}{'0'}>$tr{'Never'}
	<OPTION VALUE='1' $selected{'NOLOGINTYPE'}{'1'}>$tr{'Percent'}
	<OPTION VALUE='2' $selected{'NOLOGINTYPE'}{'2'}>$tr{'Minutes'}
	<OPTION VALUE='3' $selected{'NOLOGINTYPE'}{'3'}>$tr{'Always'}
	</SELECT></TD>
	<TD style='width: 40%;' CLASS='base'>$tr{'Annoy Message Period (Sec)'}:</TD>
	<TD><INPUT TYPE='text' style='width: 73px;' NAME='ANNOY' VALUE='$apcupsdsettings{'ANNOY'}'></TD>
</TR>
</TABLE>
END
;

&closebox();

&openbox("$tr{'Event Alert Emails'}:");

print <<END
<TABLE style='width: 100%; border: none; margin-left:auto; margin-right:auto'>
<TR>
	<TD style='text-align: right;'>Powerout:</TD><TD><INPUT TYPE='checkbox' NAME='MSGPOWEROUT' $checked{'MSGPOWEROUT'}{'on'}></TD>
	<TD style='text-align: right;'>Powerback:</TD><TD><INPUT TYPE='checkbox' NAME='MSGPOWERBACK' $checked{'MSGPOWERBACK'}{'on'}></TD>
	<TD style='text-align: right;'>Killpower:</TD><TD><INPUT TYPE='checkbox' NAME='MSGKILLPOWER' $checked{'MSGKILLPOWER'}{'on'}></TD>
	<TD style='text-align: right;'>Emergency:</TD><TD><INPUT TYPE='checkbox' NAME='MSGEMERGENCY' $checked{'MSGEMERGENCY'}{'on'}></TD>
	<TD style='text-align: right;'>Changeme:</TD><TD><INPUT TYPE='checkbox' NAME='MSGCHANGEME' $checked{'MSGCHANGEME'}{'on'}></TD>
	<TD style='text-align: right;'>Failing:</TD><TD><INPUT TYPE='checkbox' NAME='MSGFAILING' $checked{'MSGFAILING'}{'on'}></TD>
	<TD style='text-align: right;'>Annoyme:</TD><TD><INPUT TYPE='checkbox' NAME='MSGANNOY' $checked{'MSGANNOY'}{'on'}></TD>
</TR>
<TR>
	<TD style='text-align: right;'>Commfailure:</TD><TD><INPUT TYPE='checkbox' NAME='MSGCOMMFAILURE' $checked{'MSGCOMMFAILURE'}{'on'}></TD>
	<TD style='text-align: right;'>Commok:</TD><TD><INPUT TYPE='checkbox' NAME='MSGCOMMOK' $checked{'MSGCOMMOK'}{'on'}></TD>
	<TD style='text-align: right;'>Onbattery:</TD><TD><INPUT TYPE='checkbox' NAME='MSGONBATTERY' $checked{'MSGONBATTERY'}{'on'}></TD>
	<TD style='text-align: right;'>Offbattery:</TD><TD><INPUT TYPE='checkbox' NAME='MSGOFFBATTERY' $checked{'MSGOFFBATTERY'}{'on'}></TD>
	<TD style='text-align: right;'>Timeout:</TD><TD><INPUT TYPE='checkbox' NAME='MSGTIMEOUT' $checked{'MSGTIMEOUT'}{'on'}></TD>
	<TD style='text-align: right;'>Loadlimit:</TD><TD><INPUT TYPE='checkbox' NAME='MSGLOADLIMIT' $checked{'MSGLOADLIMIT'}{'on'}></TD>
	<TD style='text-align: right;'>Runlimit:</TD><TD><INPUT TYPE='checkbox' NAME='MSGRUNLIMIT' $checked{'MSGRUNLIMIT'}{'on'}></TD>
</TR>
<TR>
	<TD style='text-align: right;'></TD><TD></TD>
	<TD style='text-align: right;'>Doshutdown:</TD><TD><INPUT TYPE='checkbox' NAME='MSGDOSHUTDOWN' $checked{'MSGDOSHUTDOWN'}{'on'}></TD>
	<TD style='text-align: right;'>Remotedown:</TD><TD><INPUT TYPE='checkbox' NAME='MSGREMOTEDOWN' $checked{'MSGREMOTEDOWN'}{'on'}></TD>
	<TD style='text-align: right;'>Startselftest:</TD><TD><INPUT TYPE='checkbox' NAME='MSGSTARTSELFTEST' $checked{'MSGSTARTSELFTEST'}{'on'}></TD>
	<TD style='text-align: right;'>Endselftest:</TD><TD><INPUT TYPE='checkbox' NAME='MSGENDSELFTEST' $checked{'MSGENDSELFTEST'}{'on'}></TD>
	<TD style='text-align: right;'>Battattach:</TD><TD><INPUT TYPE='checkbox' NAME='MSGBATTATTACH' $checked{'MSGBATTATTACH'}{'on'}></TD>
	<TD style='text-align: right;'>Battdetach:</TD><TD><INPUT TYPE='checkbox' NAME='MSGBATTDETACH' $checked{'MSGBATTDETACH'}{'on'}></TD>

</TR>
</TABLE>
END
;

&closebox();

&openbox("$tr{'Operation Mode'}:");

if ( $selected{'OPMODE'}{'testing'} eq 'SELECTED' ) {
	$setcolor = 'blue';
}

if ( $selected{'OPMODE'}{'full'} eq 'SELECTED' ) {
	$setcolor = 'green';
}

print <<END
<TABLE style='width: 100%; border: none;'>
<TR>
	<TD CLASS='base' colspan='2'><span style="color:blue;"><B>$tr{'Testing Mode'}</B></span> $tr{'will simulate the response to a power failure. It will not shutdown smoothwall or the UPS'}.</TD>
</TR>
<TR>		 
	<TD CLASS='base' colspan='2'><span style="color:green;"><B>$tr{'Full Operations Mode'}</B></span><B> will</B> $tr{'shutdown smoothwall in response to a power failure'}.</TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'Operational mode (DO NOT select Full Operations Mode until you know that your configuration is OK)'}:</TD>
	<TD style='width: 25%;'>
	<SELECT NAME='OPMODE' style='color: $setcolor;' onchange='ffoxSelectUpdate(this);'>
	<OPTION VALUE='testing' $selected{'OPMODE'}{'testing'} style='color: blue;'>$tr{'Testing Mode'}
	<OPTION VALUE='full' $selected{'OPMODE'}{'full'} style='color: green;'>$tr{'Full Operations Mode'}
	</SELECT></TD>
</TR>
</TABLE>
END
;

&closebox();

print <<END

<TABLE style='width: 90%; border: none; margin-left:auto; margin-right:auto'>
<TR>
	<TD style='width: 33%; text-align: center;'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'save&restart'}'></TD>
	<TD style='text-align: center;'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'restart'}'></TD>
	<TD style='width: 33%; text-align: center;'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'stop'}'></TD>
</TR>
</TABLE>
</FORM>
<BR>
END
;

&alertbox('add', 'add');

&closepage();

