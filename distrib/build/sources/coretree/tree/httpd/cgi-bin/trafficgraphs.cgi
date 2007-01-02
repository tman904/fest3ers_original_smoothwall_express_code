#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

&showhttpheaders();

my $history = 60;
my $oururl = "/cgi-bin/trafficstats.cgi";
my $ubermax = 40;

my $script = qq {
<script language="Javascript">

var interfaces = new Array();
var rates = new Array();
rates[ 10      ] = "10 bps";
rates[ 100     ] = "100 bps";
rates[ 1000    ] = "1 kbps";
rates[ 10000   ] = "10 kbps";
rates[ 100000  ] = "100 kbps";
rates[ 1000000    ] = "1 Mbps";
rates[ 10000000   ] = "10 Mbps";
rates[ 100000000  ] = "100 Mbps";
rates[ 1000000000 ] = "1 Gbps";

function xmlhttpPost()
{
	var xmlHttpReq = false;
    	var self = this;


    	if (window.XMLHttpRequest) {
		// Mozilla/Safari
        	self.xmlHttpReq = new XMLHttpRequest();
    	} else if (window.ActiveXObject) {
    		// IE
        	self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
    	}

    	self.xmlHttpReq.open('GET', "$oururl", true);
	self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	self.xmlHttpReq.onreadystatechange = function() {
	        if ( self.xmlHttpReq && self.xmlHttpReq.readyState == 4) {
        		updatepage(self.xmlHttpReq.responseText);
		}
    	}

	document.getElementById('status').style.display = "inline";

    	self.xmlHttpReq.send( null );
}

function updatepage(str){
	document.getElementById('status').style.display = "none";

	/* determine the interfaces we're supposed to be dealing with, wherever they may be */

	var rows = str.split( '\\n' );
	
	var detail_finder = new RegExp( /cur_(.{3})_rate_([^=]*)=(.*)/ );
	for ( var i = 0; i < rows.length ; i++ ){
		if ( !rows[i] ){ continue; }
		var matches = detail_finder.exec( rows[i] );
		var interface = matches[2];
		var direction = matches[1];	
		var value     = matches[3];

		if (!document.getElementById('graph_' + interface ) ){
			create_graph( interface );
		}

		update_graph( interface, direction, value );
	
	}
	the_timeout = setTimeout( "xmlhttpPost();", 1000 );
}

function update_graph(interface, direction, value)
{
	var max_height = $ubermax;

	if ( value >= max_height ){
		max_height = value;
	}

	var total_height = 0;

	for ( var i = 0 ; i < ($history-1) ; i++ ){
		if ( parseInt(interfaces[ interface ][ direction ][ i ]) > max_height ){
			max_height = interfaces[ interface ][ direction ][ i ];
			total_height += interfaces[interface][direction][i];
		}
	}
	
	max_height++;

	max_height = rationalise( max_height );

	var height = Math.floor( ( value / max_height ) * $ubermax );
	total_height += height;

//	var dbg = document.getElementById('dbg');
//	dbg.innerHTML += "mx: " + max_height + " : hx: " + height + " : rx: " + value + "<br/>";
	
	for ( var i = 0 ; i < ($history-1) ; i++ ){
		interfaces[ interface ][ direction ][ i ] = interfaces[ interface ][ direction ][ i + 1 ];
		var nheight = Math.floor((interfaces[ interface ][ direction ][ i ]/max_height)*60);
		document.getElementById('u_' + interface + '_' + direction + '_' + i ).style.height = nheight + 'px';
		document.getElementById('l_' + interface + '_' + direction + '_' + i ).style.height = Math.floor(nheight/2) + 'px';
	}
	document.getElementById('u_' + interface + '_' + direction + '_' + i ).style.height = height + 'px';
	document.getElementById('l_' + interface + '_' + direction + '_' + i ).style.height = Math.floor(height/2) + 'px';

	document.getElementById('title_' + interface + '_' + direction ).innerHTML = rates[ max_height ]  + " ";
	interfaces[interface][direction][($history-1)] = value;


	if ( total_height == 0 ){
		document.getElementById('graph_' + interface).style.display = 'none';
	} else {
		document.getElementById('graph_' + interface).style.display = 'inline';
	}
}

function maxit( v1, v2 )
{
	if ( v1 > v2 ){
		return v1;
	} else {
		return v2;
	}
}

function rationalise( value )
{
	for ( var v = 10; v < 100000000 ; v *= 10 ){
		if ( maxit( value, v ) == v ){
			return v;
		}
	}
}

function create_graph(interface)
{
	var directions = new Array( "inc", "out" );
	var colours    = new Array( "#c0c0ff", "red" );
	var graph_html = "";	

	for ( var j = 0; j < directions.length ; j++ ){
		var direction = directions[j];
		graph_html += "<div><table style='width: 100%; height: 100px; border: 1px solid #c0c0c0; border-collapse: collapse; background-color: #f0f0ff; margin-bottom: 3px;'><tr style='height: 70px;'><td style='vertical-align: top; font-size: 8px; width: 10px; text-align: right;' rowspan='2'>" + direction + "</td><td style='vertical-align: top; font-size: 8px; width: 50px; text-align: right; border-right: 1px dashed #909090;' id='title_" + interface + "_" + direction + "' rowspan='2'></td>";
	
		for ( var i = 0; i < $history ; i++ ){
			graph_html += "<td style='width: 5px; margin: 0px;padding: 0px; vertical-align: bottom;'><div id='u_" + interface + "_" + direction + "_" + i + "' style='background-color: " + colours[j] + "; height: 33px; margin: 0px; width: 6px; padding: 0px; font-size: 1px;'></div></td>";
		}

		graph_html += "<td></td></tr><tr style='height: 30px;'>";

		for ( var i = 0; i < $history ; i++ ){
			graph_html += "<td style='border-top: 1px solid #909090;  width: 5px; margin: 0px;padding: 0px; padding-top: 1px; vertical-align: top;'><div id='l_" + interface + "_" + direction + "_" + i + "' style=\\\"background-image: url('/ui/img/fader.jpg'); background-repeat: repeat-x; background-position: top left; height: 11px; margin: 0px; width: 6px; padding: 0px; font-size: 1px;\\\"></div></td>";
		}

		graph_html += "<td></td></tr></table></div>";
	}

	document.getElementById('content').innerHTML += "<div style='width: 60%; margin-left: auto; margin-right: auto;'><div id='graph_" + interface + "'><div style='border: 1px solid #c0c0c0; margin-bottom: 3px;'><div style='background-color: #d0d0d0; text-align: center; width: 100%;'>" + interface + "</div><div style='padding: 5px;'>" + graph_html + "</div></div></div></div>";
	interfaces[ interface ] = new Array();
	interfaces[ interface ]["inc"] = new Array();
	interfaces[ interface ]["out"] = new Array();
	for ( var i = 0 ; i < $history ; i++ ){
		interfaces[interface]["inc"][ i ] = 0;
		interfaces[interface]["out"][ i ] = 0;
	}
}


</script>
};

# display the page ...

&openpage($tr{'network traffic graphs'}, 1, $script, 'about your smoothie');
&openbigbox('100%', 'LEFT');
print qq{
	<div style='width: 100%; text-align: right;'><span id='status' style='background-color: #fef1b5; display: none;'>Updating</span>&nbsp;</div>
	<div id='content' style='width: 100%; overflow: auto; vertical-align: bottom; border-bottom: solid 1px #c0c0c0; overflow-x: hidden;'></div>
	<script>xmlhttpPost();</script>
};

&closebigbox();
&closepage();
exit;



sub realtime_graphs 
{

	# construct the bar graphs accordingly.

	my %interfaces;

	open INPUT, "</var/log/quicktrafficstats";
	while ( my $line = <INPUT> ){
		next if ( not $line =~ /^cur_/ );
		my ( $rule, $interface, $value ) = ( $line =~ /(.*)_([^_]*)=([\d\.]+)$/i );
		print STDERR "looking to $rule, $interface, $value\n";
		$interfaces{ $interface }{ $rule } = $value;
	}

	print	"<div style='width: 100%; text-align: right;'><span id='status' style='background-color: #fef1b5; display: none;'>Updating</span>&nbsp;</div>\n";
	print qq { 
	<div id='main_content'>
	<style>  
		.s0{ display: none; } 
		.s1{ opacity: 0.10 ; -moz-opacity: 0.10 ; -khtml-opacity:0.10 ; filter:alpha(opacity=10)} 
		.s2{ opacity: 0.15 ; -moz-opacity: 0.15 ; -khtml-opacity:0.15 ; filter:alpha(opacity=15)} 
		.s3{ opacity: 0.20 ; -moz-opacity: 0.20 ; -khtml-opacity:0.20 ; filter:alpha(opacity=20)} 
		.s4{ opacity: 0.25 ; -moz-opacity: 0.25 ; -khtml-opacity:0.25 ; filter:alpha(opacity=25)} 
		.s5{ opacity: 0.30 ; -moz-opacity: 0.30 ; -khtml-opacity:0.30 ; filter:alpha(opacity=30)} 
		.s6{ opacity: 0.35 ; -moz-opacity: 0.35 ; -khtml-opacity:0.35 ; filter:alpha(opacity=35)} 
		.s7{ opacity: 0.40 ; -moz-opacity: 0.40 ; -khtml-opacity:0.40 ; filter:alpha(opacity=40)} 
		.s8{ opacity: 0.45 ; -moz-opacity: 0.45 ; -khtml-opacity:0.45 ; filter:alpha(opacity=45)} 
		.s9{ opacity: 0.50 ; -moz-opacity: 0.50 ; -khtml-opacity:0.50 ; filter:alpha(opacity=50)} 
		.s10{ opacity: 0.55 ; -moz-opacity: 0.55 ; -khtml-opacity:0.55 ; filter:alpha(opacity=55)} 
		.s11{ opacity: 0.60 ; -moz-opacity: 0.60 ; -khtml-opacity:0.60 ; filter:alpha(opacity=60)} 
		.s12{ opacity: 0.65 ; -moz-opacity: 0.65 ; -khtml-opacity:0.65 ; filter:alpha(opacity=65)} 
		.s13{ opacity: 0.70 ; -moz-opacity: 0.70 ; -khtml-opacity:0.70 ; filter:alpha(opacity=70)} 
		.s14{ opacity: 0.75 ; -moz-opacity: 0.75 ; -khtml-opacity:0.75 ; filter:alpha(opacity=75)} 
		.s15{ opacity: 0.80 ; -moz-opacity: 0.80 ; -khtml-opacity:0.80 ; filter:alpha(opacity=80)} 
		.s16{ opacity: 0.85 ; -moz-opacity: 0.85 ; -khtml-opacity:0.85 ; filter:alpha(opacity=85)} 
		.s17{ opacity: 0.90 ; -moz-opacity: 0.90 ; -khtml-opacity:0.90 ; filter:alpha(opacity=90)} 
		.s18{ opacity: 0.95 ; -moz-opacity: 0.95 ; -khtml-opacity:0.95 ; filter:alpha(opacity=95)} 
		.s19{ } 
	</style>
		<div style='width: 90%; margin-left: auto; margin-right: auto;'>
	};
	my @rules;

	foreach my $interface ( @devices ){
		my $iftitle = $interface;
		print qq{
		<table id='${interface}_container' style='width: 90%; border-collapse: collapse; border: 0px; margin-left: auto; margin-right: auto;'>
		<tr style='background-color: #C3D1E5;'>
			<td style="background-image: url('/themes/default/squaretopleft.jpg'); background-position: top left; background-repeat: no-repeat; text-align: left; vertical-align: middle;">&nbsp;<strong>$iftitle</strong></td>
			<td style="width: 40%; background-image: url('/themes/default/squaretopright.jpg'); background-position: top right; background-repeat: no-repeat; text-align: left; vertical-align: middle;">&nbsp;</td>
		</tr>
		<tr>
			<td colspan='2' style='background-image: url( "/themes/default/squarebackdrop.jpg" ); background-position: top left; background-repeat: no-repeat; vertical-align: top;' ><br/><table style='width: 95%; margin-left: auto; margin-right: auto; border: 0px; border-collapse: collapse;'>
		};

		foreach my $section ( keys %{$interfaces{$interface}} ){
			my $colour = $table1colour;
			my $title  = $section;
		
			if ( $section eq "cur_inc_rate" ){
				$title  = "Incoming";
				$colour = "#4D71A3";
			} elsif ( $section = "cur_out_rate" ){
				$title  = "Outgoing";
				$colour = "#4F8E83";
			}

			print qq{
			<tr>
				<td style='width: 15%;' rowspan='2' style='vertical-align: top;'>$title</td>
				<td style='width: 400px; background-color: $table2colour; font-size: 6pt; padding: 0px;'  id='${section}_${interface}_scale' >
				<table style='width: 100%; border: 0px; border-collapse: collapse;'>
				<tr>
				<td style='height: 8px; overlow: hiddent; font-size: 6pt; color: #303030; width: 25%; background-colour: #efefef; border-right: 1px solid #505050; text-align: right;' id='${section}_${interface}_scale_1'>25%</td>
				<td style='height: 8px; overlow: hiddent; font-size: 6pt; color: #303030; width: 25%; background-colour: #dfdfdf; border-right: 1px solid #505050; text-align: right;' id='${section}_${interface}_scale_2'>50%</td>
				<td style='height: 8px; overlow: hiddent; font-size: 6pt; color: #303030; width: 25%; background-colour: #cfcfcf; border-right: 1px solid #505050; text-align: right;' id='${section}_${interface}_scale_3'>75%</td>
				<td style='height: 8px; overlow: hiddent; font-size: 6pt; color: #303030; width: 25%; background-colour: #bfbfbf; border-right: 1px solid #505050; text-align: right;' id='${section}_${interface}_scale_4'>100%<td>
				</tr>
				</table>
				</td>
				<td style='width: 2%;' rowspan='2' style='vertical-align: top;'>&nbsp;</td>
				<td rowspan='2' id='${section}_${interface}_rate'></td>
			</tr>
			<tr>
				<td style='width: 400px; background-color: $table2colour; padding: 0px;'>
				<div style='width: 0px; border: 0px; background-color: $colour;' id='${section}_$interface'>&nbsp;</div>	
				</td>
			</tr>
			<tr style='height: 5px;'><td colspan='3'></td></tr>
			};
			push @rules, "${section}_${interface}";
		}

		print qq{
			</table>
		</td>
	</tr>
	<tr><td colspan='2'></td></tr>
	</table>
		};
	}

	print "</div><script>";
	show_script( \@rules );
	print "</script>";
	print "</div>";
	print "<script> monitor(); fader(); </script>\n";
}

sub show_script
{
	my ( $rules ) = @_;

	print qq {
var interfaces 	= new Array();
var old 	= new Array();
var cur 	= new Array();
var iftotals 	= new Array();
var ifclass 	= new Array();
var ofclass 	= new Array();
var ifnames 	= new Array();
var scale       = new Array();
var oscale      = new Array();
var scalef      = new Array();
	};

	for ( my $i = 0 ; $i < scalar( @$rules ) ; $i++ ){
		print "interfaces[$i] = '$rules->[$i]';\n";
		print "cur['$rules->[$i]'] = 0;\n";
		print "old['$rules->[$i]'] = 0;\n";
		print "scale['$rules->[$i]'] = 0;\n";
		print "oscale['$rules->[$i]'] = 0;\n";
		print "scalef['$rules->[$i]'] = 0;\n";
	}

	my $i = 0;
	foreach my $interface ( @devices ){
		print "iftotals['$interface'] = 0\n";
		print "ifclass['$interface'] = 19\n";
		print "ofclass['$interface'] = 19\n";
		print "ifnames[ $i ] = '$interface'\n;";
		$i++;
	}

	print qq {
var dbg = document.getElementById('dbg');

function xmlhttpPost()
{
	var xmlHttpReq = false;
    	var self = this;


    	if (window.XMLHttpRequest) {
		// Mozilla/Safari
        	self.xmlHttpReq = new XMLHttpRequest();
    	} else if (window.ActiveXObject) {
    		// IE
        	self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
    	}

    	self.xmlHttpReq.open('GET', "$oururl", true);
	self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	self.xmlHttpReq.onreadystatechange = function() {
	        if ( self.xmlHttpReq && self.xmlHttpReq.readyState == 4) {
        		updatepage(self.xmlHttpReq.responseText);
		}
    	}

	document.getElementById('status').style.display = "inline";

    	self.xmlHttpReq.send( null );
}

var splitter = /(.*)_([^_]*)=([\\d\\.]+)\$/i;

function updatepage(str){
	document.getElementById('status').style.display = "none";
	
	var rows = str.split( '\\n' );
	
	for ( var i = 0; i < ifnames.length ; i++ ){
		iftotals[ ifnames[i] ] = 0;
	}

	dbg.innerHTML = "";

	for ( var i = 0; i < rows.length ; i++ ){
		if ( rows[ i ] != "" ){
			var results = splitter.exec(rows[i]);	
			var id = results[ 1 ] + '_' + results[2];
			if ( !document.getElementById( id + '_rate' ) ){
				continue;
			}
			var divider = 0;;
			var rate = 0;
			var s1; var s2; var s3; var s4;
			if ( results[ 3 ] > (1024*1024*100) ){
				/* GBps Scale */
				divider = (400 / ( 1024 * 1024 * 1024 )) * results[ 3 ];
				rate = parseInt( results[3] / (1024*1024) );
				rate += " Mbps";
				s1 = '250M'; s2 = '500M'; s3 = '750M'; s4 = '1G'; 

			} else if ( results[ 3 ] > (1024*1024*10) ){
				/* 100 MBps */
				divider = (400 / ( 1024 * 1024 * 100 )) * results[ 3 ];
				rate = parseInt( results[3] / (1024*1024) );
				rate += " Mbps";
				s1 = '25M'; s2 = '50M'; s3 = '75M'; s4 = '100M'; 

			} else if ( results[ 3 ] > (1024*1024) ){
				/* 10 MBps */
				divider = (400 / ( 1024 * 1024 * 10 )) * results[ 3 ];
				rate = parseInt( results[3] / (1024*1024) );
				rate += " Mbps";
				s1 = '2.5M'; s2 = '5M'; s3 = '7.5M'; s4 = '10M'; 

			} else if ( results[ 3 ] > (1024) ){
				/* 1 MBps */
				divider = (400 / ( 1024 * 1024 )) * results[ 3 ];
				rate = parseInt( results[3] / 1024 );
				rate += " Kbps";
				s1 = '256K'; s2 = '512K'; s3 = '768K'; s4 = '1M';

			} else if ( results[ 3 ] > (1024) ) {
				/* KBps */
				divider = (400 / ( 1024 * 512 )) * results[ 3 ];
				rate = parseInt( results[3] );// / 1024 );
				rate += " Kbps";
				s1 = '128K'; s2 = '256K'; s3 = '384K'; s4 = '512K';

			} else {
				s1 = '&nbsp;'; s2 = '&nbsp;'; s3 = '&nbsp;'; s4 = '&nbsp;'; 
			}


			scale[ id ] = s4;
			old[ id ] = cur[ id ];
			cur[ id ] = parseInt( divider );
			document.getElementById( id ).style.width = cur[ id ] + 'px';
			document.getElementById( id + '_rate' ).innerHTML = rate;
			document.getElementById( id + '_scale_1' ).innerHTML = s1;
			document.getElementById( id + '_scale_2' ).innerHTML = s2;
			document.getElementById( id + '_scale_3' ).innerHTML = s3;
			document.getElementById( id + '_scale_4' ).innerHTML = s4;
		
			iftotals[ results[ 2 ] ] += parseInt( results[ 3 ] );

			if ( scale[ id ] != oscale[ id ] ){
				oscale[ id ] = scale[ id ];
				scalef[ id ] = 20;
			}
		}

	}
			

	setTimeout( "xmlhttpPost()", 1000 );
}

function monitor()
{
dbg.innerHTML += "hello dolly<br/>";
	xmlhttpPost();
}

function fader()
{
	var jump = 3;

	for ( var i = 0; i < interfaces.length ; i++ ){
		var element  = document.getElementById( interfaces[i] );

		var id = interfaces[i];
		if ( element ){
                        var direction =  ( old[ id ] - cur[ id ] );

			var jdis = parseInt( direction / jump );
			if ( jdis < 0 ){ jdis *= -1; }

                        if ( direction < -jump ){
                                if ( old[ id ] < cur[ id ] ){
                                        old[ id ] = ( old[ id ] + jdis );
                                        if ( element ){
                                                element.style.width = old[ id ] + "px";
                                        }
                                }
                        } else if ( direction > jump ){
                                if ( old[ id ] > cur[ id ] ){
                                        old[ id ] = ( old[ id ] - jdis );
                                        if ( element ){
                                                element.style.width = old[ id ] + "px";
                                        }
                                }
                        }
		}
	}


	for ( var i = 0; i < ifnames.length ; i++ ){
		if ( iftotals[ ifnames[i] ] == 0 ){
			ifclass[ ifnames[i] ] --; 
		} else {
			ifclass[ ifnames[i] ] ++; 
		}

		if ( ifclass[ ifnames[i] ] > 19 ){
			ifclass[ifnames[i]] = 19;
		} else if ( ifclass[ifnames[i]] < 0 ){
			ifclass[ifnames[i]] = 0;
		}

		if ( ofclass[ ifnames[ i ] ] != ifclass[ ifnames[ i ] ] ){
			document.getElementById( ifnames[i] + '_container' ).className = "s" + ifclass[ifnames[i]];
			ofclass[ ifnames[ i ] ] = ifclass[ ifnames[ i ] ];
		}
	}

	for ( var i = 0; i < interfaces.length ; i++ ){
		var id = interfaces[i];
		var v = scalef[id];
		if ( scalef[ id ] > 0 ){
			scalef[id]--;
			document.getElementById( id + '_scale').style.background = 'rgb(' + (195+(v*2)) + ',' + (209+(v*2)) + ',' + (229+(v*2)) +')';
		} else if ( scalef[ id ] == 0 ){
			scalef[id]--;
			document.getElementById( id + '_scale').style.background = 'rgb(195,209,229)';
		}
			
	}



	setTimeout( fader, 60 );



}




	};
}
