#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my (%cgiparams, %checked, %selected);
my $filename = "${swroot}/xtaccess/config";

&showhttpheaders();

$cgiparams{'ENABLED'} = 'off';
&getcgihash(\%cgiparams);

my $errormessage = '';

if ($cgiparams{'ACTION'} eq $tr{'add'})
{
	unless($cgiparams{'PROTOCOL'} =~ /^(tcp|udp)$/) { $errormessage = $tr{'invalid input'}; }
	unless(&validipormask($cgiparams{'EXT'}))
	{
		if ($cgiparams{'EXT'} ne '') {
			$errormessage = $tr{'source is bad'}; }
		else {
			$cgiparams{'EXT'} = '0.0.0.0/0'; }
	}
	unless(&validport($cgiparams{'DEST_PORT'})) { $errormessage = $tr{'destination port numbers'}; }
	open(FILE, $filename) or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);
	unless ($errormessage)
	{
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'PROTOCOL'},$cgiparams{'EXT'},$cgiparams{'DEST_PORT'},$cgiparams{'ENABLED'}\n";
		close(FILE);
		undef %cgiparams;
		&log($tr{'external access rule added'});
		system('/usr/bin/setuids/setxtaccess');
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
		my $id = 0;
		foreach $line (@current)
		{
			$id++;
			unless ($cgiparams{$id} eq "on") {
				print FILE "$line"; }
			elsif ($cgiparams{'ACTION'} eq $tr{'edit'})
			{
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'PROTOCOL'} = $temp[0];
				$cgiparams{'EXT'} = $temp[1];
				$cgiparams{'DEST_PORT'} = $temp[2];
				$cgiparams{'ENABLED'} = $temp[3];
			}
		}
		close(FILE);
		system('/usr/bin/setuids/setxtaccess');
		&log($tr{'external access rule removed'});
	}
}
if ($cgiparams{'ACTION'} eq '')
{
	$cgiparams{'PROTOCOL'} = 'tcp';
	$cgiparams{'ENABLED'} = 'on';
}

$selected{'PROTOCOL'}{'udp'} = '';
$selected{'PROTOCOL'}{'tcp'} = '';
$selected{'PROTOCOL'}{$cgiparams{'PROTOCOL'}} = 'SELECTED';

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';  
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&openpage($tr{'external access configuration'}, 1, '', 'networking');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print <<END
<!-- 
<CENTER>
<TABLE BORDER='0' CELLPADDING='0' CELLSPACING='0'>
<TR><TD VALIGN='top' ALIGN='CENTER'>
<A HREF='http://www.smoothwall.co.uk/'><IMG
 SRC='/ui/assets/3.5/img/inlinepromo.smoothhost.png' BORDER='0'
 ALT='Visit smoothwall.co.uk for enhanced commercial SmoothWall products'></A>
</TD></TR>
</TABLE>
</CENTER>
 -->
END
;

print "<FORM METHOD='POST'>\n";

&openbox($tr{'add a new rule'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD>
<SELECT NAME='PROTOCOL'>
<OPTION VALUE='udp' $selected{'PROTOCOL'}{'udp'}>UDP
<OPTION VALUE='tcp' $selected{'PROTOCOL'}{'tcp'}>TCP
</SELECT>
</TD>
<TD CLASS='base'><FONT COLOR='$colourred'>$tr{'sourcec'}</FONT></TD>
<TD><INPUT TYPE='TEXT' NAME='EXT' VALUE='$cgiparams{'EXT'}' SIZE='32'></TD>
<TD CLASS='base'><FONT COLOR='$colourred'>$tr{'destination portc'}</FONT></TD>
<TD><INPUT TYPE='TEXT' NAME='DEST_PORT' VALUE='$cgiparams{'DEST_PORT'}' SIZE='5'></TD>
</TR>
</TABLE>
<TABLE WIDTH='100%'>
<TR>
<TD CLASS='base' WIDTH='50%' ALIGN='CENTER'>$tr{'enabled'}<INPUT TYPE='CHECKBOX' NAME='ENABLED' $checked{'ENABLED'}{'on'}></TD>
<TD WIDTH='50%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'add'}'></TD>
</TR>
</TABLE>
END
;
&closebox();

&openbox($tr{'current rules'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='10%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'protocol'}</B></TD>
<TD WIDTH='40%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'source'}</B></TD>
<TD WIDTH='30%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'destination port'}</B></TD>
<TD WIDTH='10%' CLASS='boldbase' ALIGN='CENTER'><B>$tr{'enabledtitle'}</B></TD>
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
	my $protocol = '';
	my $gif = '';
	if ($temp[0] eq 'udp') {
		$protocol = 'UDP'; }
	else {
		$protocol = 'TCP' }
	if ($id % 2) {
		print "<TR BGCOLOR='$table1colour'>\n"; }
	else {
              	print "<TR BGCOLOR='$table2colour'>\n"; }
	if ($temp[3] eq 'on') { $gif = 'on.gif'; }
		else { $gif = 'off.gif'; }
	if ($temp[1] eq '0.0.0.0/0') {
		$temp[1] = $tr{'all'}; }
print <<END
<TD ALIGN='CENTER'>$protocol</TD>
<TD ALIGN='CENTER'>$temp[1]</TD>
<TD ALIGN='CENTER'>$temp[2]</TD>
<TD ALIGN='CENTER'><IMG SRC='/ui/assets/3.5/img/$gif'></TD>
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

&alertbox('add','add');

&closebigbox();

&closepage();

