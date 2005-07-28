#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use IO::Socket;
require '/var/smoothwall/header.pl';
require '/var/smoothwall/updatelists.pl';

&showhttpheaders();

my (%uploadsettings,$errormessage);
&getcgihash(\%uploadsettings);

&openpage($tr{'updates'}, 1, '', 'maintenance');

&openbigbox('100%', 'LEFT');

if ($uploadsettings{'ACTION'} eq "upload")
{
	my @list;
	my $return = &downloadlist();
	if ($return =~ m/^HTTP\/\d+\.\d+ 200/)
	{
		unless (open(LIST, ">${swroot}/patches/available"))
		{
	                $errormessage = $tr{'could not open available updates file'};
      	 	        goto ERROR;
        	}
		flock LIST, 2;
	        my @this = split(/----START LIST----\n/,$return);
		print LIST $this[1];
		close(LIST);
		@list = split(/\n/,$this[1]);
	} 
	else
	{
		unless(open(LIST, "${swroot}/patches/available"))
		{
			$errormessage = $tr{'could not open available updates list'};
			goto ERROR;
		}
		@list = <LIST>;
		close(LIST);
		$errormessage = $tr{'could not download the available updates list'};
	}
	unless (mkdir("/var/patches/$$",0700))
	{
		$errormessage = $tr{'could not create directory'};
		goto ERROR;
	}
	unless (open(FH, ">/var/patches/$$/patch.tar.gz"))
	{
		$errormessage = $tr{'could not open update for writing'};
		goto ERROR;
	}
	flock fH, 2;
	print FH $uploadsettings{'FH'};
	close(FH);
	my $md5sum;
	chomp($md5sum = `/usr/bin/md5sum /var/patches/$$/patch.tar.gz`);
	my $found = 0;
	my ($id,$md5,$title,$description,$date,$url);
	foreach (@list)
	{
		chomp();
		($id,$md5,$title,$description,$date,$url) = split(/\|/,$_);
		if ($md5sum =~ m/^$md5\s/)
		{
			$found = 1;
			last;
		}
	}
	unless ($found == 1)
	{
		$errormessage = $tr{'this is not an authorised update'};
		goto ERROR;
	}
	unless (system("cd /var/patches/$$ && /bin/tar xvfz patch.tar.gz > /dev/null") == 0)
	{
		$errormessage = $tr{'this is not a valid archive'};
		goto ERROR;
	}
	unless (open(INFO, "/var/patches/$$/information"))
	{
		$errormessage = $tr{'could not open update information file'};
		goto ERROR;
	}
	my $info = <INFO>;
	close(INFO);
	open(INS, "${swroot}/patches/installed") or $errormessage = $tr{'could not open installed updates file'};
	while (<INS>)
	{
		my @temp = split(/\|/,$_);
		if($info =~ m/^$temp[0]/)
		{
			$errormessage = $tr{'this update is already installed'};
			goto ERROR;
		}
	}
	chdir("/var/patches/$$");
	unless (system("/usr/bin/setuids/installpackage $$ > /dev/null") == 0)
	{
		$errormessage = $tr{'package failed to install'};
		goto ERROR;
	}
	unless (open(IS, ">>${swroot}/patches/installed")) {
 		$errormessage = $tr{'update installed but'}; }
	flock IS, 2;
	my @time = gmtime();
	chomp($info);
	$time[4] = $time[4] + 1;
	$time[5] = $time[5] + 1900;
	if ($time[3] < 10) { $time[3] = "0$time[3]"; }
	if ($time[4] < 10) { $time[4] = "0$time[4]"; }
	print IS "$info|$time[5]-$time[4]-$time[3]\n";
	close(IS);
	&log("$tr{'the following update was successfully installedc'} $title"); 
}
elsif ($uploadsettings{'ACTION'} eq $tr{'refresh update list'})
{
	my $return = &downloadlist();
	if ($return =~ m/^HTTP\/\d+\.\d+ 200/)
	{
                unless(open(LIST, ">${swroot}/patches/available"))
		{
                        $errormessage = $tr{'could not open available updates file'};
                        goto ERROR;
                }
		flock LIST, 2;
                my @this = split(/----START LIST----\n/,$return);
                print LIST $this[1];
                close(LIST);
		&log($tr{'successfully refreshed updates list'});
        } 
	else {
                $errormessage = $tr{'could not download the available updates list'}; }
}

ERROR:

open(AV, "${swroot}/patches/available") or $errormessage = $tr{'could not open the available updates file'};
my @av = <AV>;
close(AV);

&alertbox($errormessage);

&openbox($tr{'installed updates'});

print qq|<TABLE WIDTH='100%' BORDER='0' CELLPADDING='2 CELLSPACING='0'>
<TR>
<TD WIDTH='5%' ALIGN='CENTER'><B>$tr{'id'}</B></TD>
<TD WIDTH='30%' ALIGN='CENTER'><B>$tr{'title'}</B></TD>
<TD WIDTH='35%' ALIGN='CENTER'><B>$tr{'description'}</B></TD>
<TD WIDTH='15%' ALIGN='CENTER'><B>$tr{'released'}</B></TD>
<TD WIDTH='15%' ALIGN='CENTER'><B>$tr{'installed'}</B></TD>
</TR>
|;

open (PF, "${swroot}/patches/installed") or $errormessage = $tr{'could not open installed updates file'};
while (<PF>)
{
	next if $_ =~ m/^#/;
	my @temp = split(/\|/,$_);
	@av = grep(!/^$temp[0]/, @av);
	print "<TR><TD VALIGN='TOP'>" . join("</TD><TD VALIGN='TOP'>",@temp) . "</TD></TR>";
}
close(PF);

print qq|</TABLE>|;

&closebox();

&openbox($tr{'available updates'});

if ($av[0] ne "")
{
	print $tr{'there are updates available'};

	print qq|<TABLE WIDTH='100%' BORDER='0' CELLPADDING='2 CELLSPACING='0'>
<TR>
<TD WIDTH='5%' ALIGN='CENTER'><B>$tr{'id'}</B></TD>
<TD WIDTH='30%' ALIGN='CENTER'><B>$tr{'title'}</B></TD>
<TD WIDTH='50%' ALIGN='CENTER'><B>$tr{'description'}</B></TD>
<TD WIDTH='15%' ALIGN='CENTER'><B>$tr{'released'}</B></TD>
</TR>
|;
	foreach (@av)
	{
		my @temp = split(/\|/,$_);
		print "<TR><TD VALIGN='TOP'>$temp[0]</TD><TD VALIGN='TOP'>$temp[2]</TD><TD VALIGN='TOP'>$temp[3]</TD><TD VALIGN='TOP'>$temp[4]</TD><TD VALIGN='TOP'><A HREF='$temp[5]' TARGET='_new'>$tr{'info'}</A></TD></TR>";
	}
	print "</TABLE>";
} 
else {
	print $tr{'all updates installed'}; }

&closebox();

&openbox($tr{'install new update'});

print qq|
$tr{'to install an update'}
<P>
<TABLE>
<TR>
<FORM METHOD='post' ACTION='/cgi-bin/updates.cgi' ENCTYPE='multipart/form-data'>
<TD ALIGN='right' CLASS='base'><B>$tr{'upload update file'}</B></TD>
<TD><INPUT TYPE="file" NAME="FH"> <INPUT TYPE='submit' NAME='ACTION' VALUE='upload'</TD>
</FORM>
</TR>
</TABLE>|;

&closebox();

print qq|
<P>
<DIV ALIGN='CENTER'>
<FORM ACTION='/cgi-bin/updates.cgi' METHOD='POST'>
<INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'refresh update list'}'>
</FORM></DIV>
|;

&alertbox('add','add');

&closebigbox();

&closepage();
