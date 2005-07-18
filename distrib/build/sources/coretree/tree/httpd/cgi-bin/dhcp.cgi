#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

require '/var/smoothwall/header.pl';

my %dhcpsettings;
my %netsettings;

my $filename = "${swroot}/dhcp/staticconfig";

&showhttpheaders();

$netsettings{'GREEN_DRIVER'} = '';
$netsettings{'GREEN_ADDRESS'} = '';
$netsettings{'GREEN_NETADDRESS'} = '';
$netsettings{'GREEN_NETMASK'} = '';
&readhash("${swroot}/ethernet/settings", \%netsettings);

$dhcpsettings{'ACTION'} = '';
$dhcpsettings{'VALID'} = '';

$dhcpsettings{'ENABLE'} = 'off';
$dhcpsettings{'START_ADDR'} = '';
$dhcpsettings{'END_ADDR'} = '';
$dhcpsettings{'DNS1'} = '';
$dhcpsettings{'DNS2'} = '';
$dhcpsettings{'DOMAIN_NAME'} = '';
$dhcpsettings{'DEFAULT_LEASE_TIME'} = '';
$dhcpsettings{'MAX_LEASE_TIME'} = '';

&getcgihash(\%dhcpsettings);

my $errormessage = '';
if ($dhcpsettings{'ACTION'} eq $tr{'save'})
{ 
	if (!(&validip($dhcpsettings{'START_ADDR'})))
	{
		$errormessage = $tr{'invalid start address'};
		goto ERROR;
	}
	if (!(&validip($dhcpsettings{'END_ADDR'})))
	{
		$errormessage = $tr{'invalid end address'};
		goto ERROR;
	}
	if ($dhcpsettings{'DNS1'})
	{
		if (!(&validip($dhcpsettings{'DNS1'})))
		{
			$errormessage = $tr{'invalid primary dns'};
			goto ERROR;
		}
	}
	if ($dhcpsettings{'DNS2'})
	{
		if (!(&validip($dhcpsettings{'DNS2'})))
		{
			$errormessage = $tr{'invalid secondary dns'};
			goto ERROR;
		}
	}
	if (!($dhcpsettings{'WINS1'}) && $dhcpsettings{'WINS2'})
	{
		$errormessage = $tr{'cannot specify secondary wins without specifying primary'}; 
		goto ERROR;
	}
	if ($dhcpsettings{'WINS1'})
	{
		if (!(&validip($dhcpsettings{'WINS1'})))
		{
			$errormessage = $tr{'invalid primary wins'};
			goto ERROR;
		}
	}
	if ($dhcpsettings{'WINS2'})
	{
		if (!(&validip($dhcpsettings{'WINS2'})))
		{
			$errormessage = $tr{'invalid secondary wins'};
			goto ERROR;
		}
	}
	if (!($dhcpsettings{'DNS1'}) && $dhcpsettings{'DNS2'})
	{
		$errormessage = $tr{'cannot specify secondary dns without specifying primary'}; 
		goto ERROR;
	}
	if (!($dhcpsettings{'DEFAULT_LEASE_TIME'} =~ /^\d+$/))
	{
		$errormessage = $tr{'invalid default lease time'};
		goto ERROR;
	}
	if (!($dhcpsettings{'MAX_LEASE_TIME'} =~ /^\d+$/))
	{
		$errormessage = $tr{'invalid max lease time'};
		goto ERROR;
	}
ERROR:
	if ($errormessage) {
		$dhcpsettings{'VALID'} = 'no'; }
	else {
		$dhcpsettings{'VALID'} = 'yes'; }

	delete $dhcpsettings{'STATIC_DESC'};
	delete $dhcpsettings{'STATIC_MAC'};
	delete $dhcpsettings{'STATIC_IP'};
	&writehash("${swroot}/dhcp/settings", \%dhcpsettings);

	if ($dhcpsettings{'VALID'} eq 'yes')
	{
		open(FILE, ">/${swroot}/dhcp/dhcpd.conf") or die "Unable to write dhcpd.conf file";
		flock(FILE, 2);
		print FILE "ddns-update-style ad-hoc;\n\n";
		print FILE "subnet $netsettings{'GREEN_NETADDRESS'} netmask $netsettings{'GREEN_NETMASK'}\n";
		print FILE "{\n";
		print FILE "\toption subnet-mask $netsettings{'GREEN_NETMASK'};\n";
		print FILE "\toption domain-name \"$dhcpsettings{'DOMAIN_NAME'}\";\n";
		print FILE "\toption routers $netsettings{'GREEN_ADDRESS'};\n";
		if ($dhcpsettings{'DNS1'})
		{
			print FILE "\toption domain-name-servers ";
			print FILE "$dhcpsettings{'DNS1'}";
			if ($dhcpsettings{'DNS2'}) {
				print FILE ", $dhcpsettings{'DNS2'}"; }
			print FILE ";\n";
		}
		if ($dhcpsettings{'WINS1'})
		{
			print FILE "\toption netbios-name-servers ";
			print FILE "$dhcpsettings{'WINS1'}";
			if ($dhcpsettings{'WINS2'}) {
				print FILE ", $dhcpsettings{'WINS2'}"; }
			print FILE ";\n";
	        }
		my $defaultleasetime = $dhcpsettings{'DEFAULT_LEASE_TIME'} * 60;
		my $maxleasetime = $dhcpsettings{'MAX_LEASE_TIME'} * 60;
		print FILE "\trange dynamic-bootp $dhcpsettings{'START_ADDR'} $dhcpsettings{'END_ADDR'};\n";
		print FILE "\tdefault-lease-time $defaultleasetime;\n";
		print FILE "\tmax-lease-time $maxleasetime;\n";
		my $id = 0;
		open(RULES, "$filename") or die 'Unable to open config file.';
		while (<RULES>)
		{
			$id++;
			chomp($_);
			my @temp = split(/\,/,$_);
			print FILE "\thost $id { hardware ethernet $temp[1]; fixed-address $temp[2]; }\n";
		}
		close(RULES);
		print FILE "}\n";
		close FILE;
	
		if ($dhcpsettings{'ENABLE'} eq 'on' && $dhcpsettings{'VALID'} eq 'yes')
		{
			system ('/bin/touch', "${swroot}/dhcp/enable");
			&log($tr{'dhcp server enabled'})
		}
		else
		{
			unlink "${swroot}/dhcp/enable";
			&log($tr{'dhcp server disabled'})
		}		
		
		system '/usr/bin/setuids/restartdhcp';

		unlink "${swroot}/dhcp/uptodate";
	}
}

if ($dhcpsettings{'ACTION'} eq $tr{'add'})
{
	# Munge the MAC into something good.
	my $mac = $dhcpsettings{'STATIC_MAC'};
	$mac =~ s/[^0-9a-f]//ig;
	$mac = uc($mac);
	$mac =~ /^(..)(..)(..)(..)(..)(..)$/;
	$mac = "$1:$2:$3:$4:$5:$6";
	if (&validmac($mac)) {
		$dhcpsettings{'STATIC_MAC'} = $mac; }

	unless ($dhcpsettings{'STATIC_DESC'}) { $errormessage = $tr{'please enter a description'}; }
	if ($dhcpsettings{'STATIC_DESC'} =~ /[\,\n]/) { $errormessage = $tr{'description contains bad characters'}; }
	unless(&validmac($dhcpsettings{'STATIC_MAC'})) { $errormessage = $tr{'mac address not valid'}; }
	unless(&validip($dhcpsettings{'STATIC_IP'})) { $errormessage = $tr{'ip address not valid'}; }
	unless ($errormessage)
	{
		open(FILE, ">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$dhcpsettings{'STATIC_DESC'},$dhcpsettings{'STATIC_MAC'},$dhcpsettings{'STATIC_IP'}\n";
		close(FILE);
		delete $dhcpsettings{'STATIC_DESC'};
		delete $dhcpsettings{'STATIC_MAC'};
		delete $dhcpsettings{'STATIC_IP'};
		system ('/bin/touch', "${swroot}/dhcp/uptodate");
	}
}
if ($dhcpsettings{'ACTION'} eq $tr{'remove'} || $dhcpsettings{'ACTION'} eq $tr{'edit'})
{
	open(FILE, "$filename") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	my $count = 0;
	my $id = 0;
	my $line;
	foreach $line (@current)
	{
		$id++;
		if ($dhcpsettings{$id} eq "on") {
			$count++; }
	}
	if ($count == 0) {
		$errormessage = $tr{'nothing selected'}; }
	if ($count > 1 && $dhcpsettings{'ACTION'} eq $tr{'edit'}) {
		$errormessage = $tr{'you can only select one item to edit'}; }
	unless ($errormessage)
	{
		open(FILE, ">$filename") or die 'Unable to open config file.';
		flock FILE, 2;
 		$id = 0;
		foreach $line (@current)
		{
			$id++;
			unless ($dhcpsettings{$id} eq "on") {
				print FILE "$line"; }
			elsif ($dhcpsettings{'ACTION'} eq $tr{'edit'})
			{
				chomp($line);
				my @temp = split(/\,/,$line);
				$dhcpsettings{'STATIC_DESC'} = $temp[0];
				$dhcpsettings{'STATIC_MAC'} = $temp[1];
				$dhcpsettings{'STATIC_IP'} = $temp[2];
			}
		}
		close(FILE);
		system ('/bin/touch', "${swroot}/dhcp/uptodate");
	}
}

&readhash("${swroot}/dhcp/settings", \%dhcpsettings);

if ($dhcpsettings{'VALID'} eq '')
{
 	$dhcpsettings{'ENABLE'} = 'off';
        $dhcpsettings{'DNS1'} = $netsettings{'GREEN_ADDRESS'};
        $dhcpsettings{'DEFAULT_LEASE_TIME'} = '60';
        $dhcpsettings{'MAX_LEASE_TIME'} = '120';
}

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$dhcpsettings{'ENABLE'}} = 'CHECKED';

&openpage($tr{'dhcp configuration'}, 1, '', 'services');

&showservicessection();

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox('100%', 'LEFT', 'DHCP:');
print <<END
<TABLE WIDTH='100%'>
<TR>
	<TD WIDTH='25%' CLASS='base'>$tr{'start address'}</TD>
	<TD WIDTH='25%'><INPUT TYPE='text' NAME='START_ADDR' VALUE='$dhcpsettings{'START_ADDR'}'></TD>
	<TD WIDTH='25%' CLASS='base'>$tr{'end address'}</TD>
	<TD WIDTH='25%'><INPUT TYPE='text' NAME='END_ADDR' VALUE='$dhcpsettings{'END_ADDR'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'primary dns'}</TD>
	<TD><INPUT TYPE='text' NAME='DNS1' VALUE='$dhcpsettings{'DNS1'}'></TD>
	<TD CLASS='base'>$tr{'secondary dns'}</TD>
	<TD><INPUT TYPE='text' NAME='DNS2' VALUE='$dhcpsettings{'DNS2'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'primary wins'}</TD>
	<TD><INPUT TYPE='text' NAME='WINS1' VALUE='$dhcpsettings{'WINS1'}'></TD>
	<TD CLASS='base'>$tr{'secondary wins'}</TD>
	<TD><INPUT TYPE='text' NAME='WINS2' VALUE='$dhcpsettings{'WINS2'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'default lease time'}</TD>
	<TD><INPUT TYPE='text' NAME='DEFAULT_LEASE_TIME' VALUE='$dhcpsettings{'DEFAULT_LEASE_TIME'}'></TD>
	<TD CLASS='base'>$tr{'max lease time'}</TD>
	<TD><INPUT TYPE='text' NAME='MAX_LEASE_TIME' VALUE='$dhcpsettings{'MAX_LEASE_TIME'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'domain name suffix'}&nbsp;<IMG SRC='/ui/assets/3.5/img/blob.gif' ALT='*'></TD></TD>
	<TD><INPUT TYPE='text' NAME='DOMAIN_NAME' VALUE='$dhcpsettings{'DOMAIN_NAME'}'></TD>
	<TD CLASS='base'>$tr{'enabled'}</TD>
	<TD><INPUT TYPE='checkbox' NAME='ENABLE' $checked{'ENABLE'}{'on'}></TD>
</TR>
</TABLE>
<BR>
<IMG SRC='/ui/assets/3.5/img/blob.gif' ALT='*' VALIGN='top'>&nbsp;
<FONT CLASS='base'>$tr{'this field may be blank'}</FONT>
END
;
&closebox();

&openbox('100%', 'LEFT', $tr{'add a new static assignment'});
print <<END
<TABLE WIDTH='100%'>
<TR>
	<TD WIDTH='25%' CLASS='base'>$tr{'descriptionc'}</TD>
	<TD WIDTH='25%'><INPUT TYPE='text' NAME='STATIC_DESC' VALUE='$dhcpsettings{'STATIC_DESC'}'></TD>
	<TD WIDTH='25%' CLASS='base'>$tr{'mac addressc'}</TD>
	<TD WIDTH='25%'><INPUT TYPE='text' NAME='STATIC_MAC' VALUE='$dhcpsettings{'STATIC_MAC'}'></TD>
</TR>
<TR>
	<TD WIDTH='25%' CLASS='base'>$tr{'ip addressc'}</TD>
	<TD WIDTH='25%'><INPUT TYPE='text' NAME='STATIC_IP' VALUE='$dhcpsettings{'STATIC_IP'}'></TD>
	<TD WIDTH='50%' ALIGN='CENTER' COLSPAN='2'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'add'}'></TD>
</TR>
</TABLE>
END
;
&closebox();

&openbox('100%', 'LEFT', $tr{'current static assignments'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='30%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'description'}</B></TD>
<TD WIDTH='30%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'mac address'}</B></TD>
<TD WIDTH='30%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'ip address'}</B></TD>
<TD WIDTH='10%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'mark'}</B></TD>
</TR>
END
;

my $id = 0;
open(RULES, "$filename") or die 'Unable to open config file.';
while (<RULES>)
{
	$id++;
	chomp($_);
	my @temp = split(/\,/,$_);
	if ($id % 2) {
		print "<TR BGCOLOR='$table1colour'>\n"; }
	else {
		print "<TR BGCOLOR='$table2colour'>\n"; }
	print <<END
<TD ALIGN='CENTER'>$temp[0]</TD>
<TD ALIGN='CENTER'>$temp[1]</TD>
<TD ALIGN='CENTER'>$temp[2]</TD>
<TD ALIGN='CENTER'><INPUT TYPE='CHECKBOX' NAME='$id'></TD>
</TR>
END
;
}
close(RULES);

print <<END
</TABLE>
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='50%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'remove'}'></TD>
<TD WIDTH='50%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'edit'}'></TD>
</TR>
</TABLE>
END
;
&closebox();

&openbox('100%', 'LEFT', $tr{'note'});
if (-e "${swroot}/dhcp/uptodate") {
	print "<FONT CLASS='base'>$tr{'there are unsaved changes'}<FONT>\n"; }
print "&nbsp;\n";
&closebox();

print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='60%'>
<TR>
	<TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'save'}'></TD>
</TR>
</TABLE>
</DIV>
END
;

print "</FORM>\n";

&alertbox('add','add');

&closebigbox();

&closepage();
