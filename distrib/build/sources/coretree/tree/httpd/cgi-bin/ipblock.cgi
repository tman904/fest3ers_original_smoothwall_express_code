#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL

#
# (c) SmoothWall Ltd 2003

require '/var/smoothwall/header.pl';

my (%cgiparams,%checked,%selected);
my $filename = "${swroot}/ipblock/config";
my @vars;
my $var, $addr;
my $needrestart = 0;

&showhttpheaders();

$cgiparams{'ENABLED'} = 'off';
$cgiparams{'LOG'} = 'off';
&getcgihash(\%cgiparams);

if ($ENV{'QUERY_STRING'} && $cgiparams{'ACTION'} eq '')
{
	@vars = split(/\&/, $ENV{'QUERY_STRING'});
	foreach $_ (@vars)
	{
		($var, $addr) = split(/\=/);
		if ($var eq 'ip')
		{
			if (&validipormask($addr))
			{
				open(FILE,">>$filename") or die 'Unable to open config file.';
				flock FILE, 2;
				print FILE "$addr,off,DROP,on\n";
				close(FILE);
				$needrestart = 1;
			}
		}
	}
	if ($needrestart) {
		system('/usr/bin/setuids/setipblock'); }
}


my $errormessage = '';

if ($cgiparams{'ACTION'} eq $tr{'add'})
{
	unless(&validipormask($cgiparams{'SRC_IP'})) { $errormessage = $tr{'source ip bad'}; }
	open(FILE, $filename) or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);
	unless ($errormessage)
	{
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'SRC_IP'},$cgiparams{'LOG'},$cgiparams{'TARGET'},$cgiparams{'ENABLED'}\n";
		close(FILE);
		undef %cgiparams;
		&log($tr{'ip block rule added'});
		system('/usr/bin/setuids/setipblock');
	}
}
if ($cgiparams{'ACTION'} eq $tr{'remove'} || $cgiparams{'ACTION'} eq $tr{'edit'})
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
		if ($cgiparams{$id} eq "on") {
			$count++; }
	}
	if ($count == 0) {
		$errormessage = $tr{'nothing selected'}; }
	if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'}) {
		$errormessage = $tr{'you can only select one item to edit'}; }
	unless ($errormessage)
	{
		open(FILE, ">$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		$id = 0;
		foreach $line (@current)
		{
			$id++;
			unless ($cgiparams{$id} eq "on") {
				print FILE "$line"; }
			elsif ($cgiparams{'ACTION'} eq $tr{'edit'})
			{
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'SRC_IP'} = $temp[0];
				$cgiparams{'LOG'} = $temp[1];
				$cgiparams{'TARGET'} = $temp[2];
				$cgiparams{'ENABLED'} = $temp[3];
			}
		}
		close(FILE);
		system('/usr/bin/setuids/setipblock');
		&log($tr{'ip block rule removed'});
	}
}
if ($cgiparams{'ACTION'} eq '')
{
	$cgiparams{'TARGET'} = 'DROP';
	$cgiparams{'ENABLED'} = 'on';
}

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';  
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

$checked{'LOG'}{'off'} = '';
$checked{'LOG'}{'on'} = '';  
$checked{'LOG'}{$cgiparams{'LOG'}} = 'CHECKED';

$checked{'TARGET'}{'DROP'} = '';
$checked{'TARGET'}{'REJECT'} = '';
$checked{'TARGET'}{$cgiparams{'TARGET'}} = 'CHECKED';

&openpage($tr{'ip block configuration'}, 1, '', 'networking');

&shownetworkingsection();

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox('100%', 'LEFT', $tr{'add a new rule'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='20%' CLASS='base'><FONT COLOR='$colourred'>$tr{'source ip or networkc'}</FONT></TD>
<TD WIDTH='20%'><INPUT TYPE='TEXT' NAME='SRC_IP' VALUE='$cgiparams{'SRC_IP'}' SIZE='15'></TD>
<TD WIDTH='20%' CLASS='base'>
<INPUT TYPE='radio' NAME='TARGET' VALUE='DROP' $checked{'TARGET'}{'DROP'}>$tr{'drop packet'}
</TD>
<TD WIDTH='20%' CLASS='base'>
<INPUT TYPE='radio' NAME='TARGET' VALUE='REJECT' $checked{'TARGET'}{'REJECT'}>$tr{'reject packet'}
</TD>
<TD WIDTH='20%' CLASS='base'>
$tr{'logc'}<INPUT TYPE='checkbox' NAME='LOG' $checked{'LOG'}{'on'}>
</TD>
</TR>
</TABLE>
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='50%' CLASS='base' ALIGN='CENTER'>$tr{'enabled'}<INPUT TYPE='CHECKBOX' NAME='ENABLED' $checked{'ENABLED'}{'on'}></TD>
<TD WIDTH='50%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'add'}'></TD>
</TR>
</TABLE>
END
;
&closebox();

&openbox('100%', 'LEFT', $tr{'current rules'});
print <<END
<TABLE WIDTH='100%' CELLSPACING='1'>
<TR>
<TD WIDTH='30%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'source ip'}</B></TD>
<TD WIDTH='20%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'action'}</B></TD>
<TD WIDTH='20%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'log'}</B></TD>
<TD WIDTH='15%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'enabledtitle'}</B></TD>
<TD WIDTH='15%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'mark'}</B></TD>
END
;

my $id = 0;
open(RULES, "$filename") or die 'Unable to open config file.';
while (<RULES>)
{
	my ($protocol, $loggif, $enabledgif);
	$id++;
	chomp($_);
	my @temp = split(/\,/,$_);
	if ($id % 2) {
		$colour = $table1colour; }
	else {
		$colour = $table2colour; }

	if ($temp[1] eq 'on') { $loggif = 'on.gif'; }
		else { $loggif = 'off.gif'; }
	if ($temp[3] eq 'on') { $enabledgif = 'on.gif'; }
		else { $enabledgif = 'off.gif'; }

	print <<END
<TR BGCOLOR='$colour'>
<TD ALIGN='CENTER'>$temp[0]</TD>
<TD ALIGN='CENTER'>$temp[2]</TD>
<TD ALIGN='CENTER'><IMG SRC='/ui/assets/3.5/img/$loggif'></TD>
<TD ALIGN='CENTER'><IMG SRC='/ui/assets/3.5/img/$enabledgif'></TD>
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

&alertbox('add', 'add');

&closebox();

&closebigbox();

&closepage($errormessage);

