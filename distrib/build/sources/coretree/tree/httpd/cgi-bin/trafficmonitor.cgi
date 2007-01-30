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

var titles = new Array();
titles[ 'inc' ] = "I<br/>n<br/>c<br/>o<br/>m<br/>i<br/>n<br/>g";
titles[ 'out' ] = "O<br/>u<br/>t<br/>g<br/>o<br/>i<br/>n<br/>g";


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
		var tinterface = matches[2];
		var direction = matches[1];	
		var value     = matches[3];

		if (!document.getElementById('graph_' + tinterface ) ){
			create_graph( tinterface );
		}

		update_graph( tinterface, direction, value );
	
	}
	the_timeout = setTimeout( "xmlhttpPost()", 1000 );
}

function update_graph( tinterface, direction, value)
{
	var max_height = $ubermax;

	if ( value >= max_height ){
		max_height = value;
	}

	var total_height = 0;

	for ( var i = 0 ; i < ($history-1) ; i++ ){
		if ( parseInt(interfaces[ tinterface ][ direction ][ i ]) > max_height ){
			max_height = interfaces[ tinterface ][ direction ][ i ];
			total_height += interfaces[tinterface][direction][i];
		}
	}
	
	max_height++;

	max_height = rationalise( max_height );

	var height = Math.floor( ( value / max_height ) * $ubermax );
	total_height += height;

//	var dbg = document.getElementById('dbg');
//	dbg.innerHTML += "mx: " + max_height + " : hx: " + height + " : rx: " + value + "<br/>";
	
	for ( var i = 0 ; i < ($history-1) ; i++ ){
		interfaces[ tinterface ][ direction ][ i ] = interfaces[ tinterface ][ direction ][ i + 1 ];
		var nheight = Math.floor((interfaces[ tinterface ][ direction ][ i ]/max_height)*60);
		document.getElementById('u_' + tinterface + '_' + direction + '_' + i ).style.height = nheight + 'px';
		document.getElementById('l_' + tinterface + '_' + direction + '_' + i ).style.height = Math.floor(nheight/2) + 'px';
	}
	document.getElementById('u_' + tinterface + '_' + direction + '_' + i ).style.height = height + 'px';
	document.getElementById('l_' + tinterface + '_' + direction + '_' + i ).style.height = Math.floor(height/2) + 'px';

	document.getElementById('title_' + tinterface + '_' + direction ).innerHTML = rates[ max_height ]  + " ";
	interfaces[tinterface][direction][($history-1)] = value;


	if ( total_height == 0 ){
		document.getElementById('graph_' + tinterface).style.display = 'none';
	} else {
		document.getElementById('graph_' + tinterface).style.display = 'inline';
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

function create_graph(tinterface)
{
	var directions = new Array( "inc", "out" );
	var colours    = new Array( "#ff9900", "#ffcc66" );
	var graph_html = "";	

	for ( var j = 0; j < directions.length ; j++ ){
		var direction = directions[j];
		graph_html += "<div><table style='width: 100%; height: 100px; border: 1px solid #c0c0c0; border-collapse: collapse; background-color: #f0f0ff; margin-bottom: 3px;'><tr style='height: 70px;'><td style='vertical-align: top; font-size: 8px; width: 10px; text-align: center; vertical-align: middle; background-color: #e0e0ef;' rowspan='2'>" + titles[ direction ] + "</td><td style='vertical-align: top; font-size: 8px; width: 50px; text-align: right; border-right: 1px dashed #909090;' id='title_" + tinterface + "_" + direction + "' rowspan='2'></td>";
	
		for ( var i = 0; i < $history ; i++ ){
			graph_html += "<td style='width: 5px; margin: 0px;padding: 0px; vertical-align: bottom;  background-image: url(/ui/img/dasher.png); background-repeat: repeat;'><div id='u_" + tinterface + "_" + direction + "_" + i + "' style='background-color: " + colours[j] + "; height: 33px; margin: 0px; width: 6px; padding: 0px; font-size: 1px;'></div></td>";
		}

		graph_html += "<td></td></tr><tr style='height: 30px;'>";

		for ( var i = 0; i < $history ; i++ ){
			graph_html += "<td style='border-top: 1px solid #909090;  width: 5px; margin: 0px;padding: 0px; padding-top: 1px; vertical-align: top;'><div id='l_" + tinterface + "_" + direction + "_" + i + "' style=\\\"background-image: url('/ui/img/fader" + direction + ".jpg'); background-repeat: repeat-x; background-position: top left; height: 11px; margin: 0px; width: 6px; padding: 0px; font-size: 1px;\\\"></div></td>";
		}

		graph_html += "<td></td></tr></table></div>";
	}

	document.getElementById('content').innerHTML += "<div style='width: 60%; margin-left: auto; margin-right: auto;'><div id='graph_" + tinterface + "'><div style='border: 1px solid #c0c0c0; margin-bottom: 3px;'><div style='background-color: #d0d0d0; text-align: center; width: 100%;'>" + tinterface + "</div><div style='padding: 5px;'>" + graph_html + "</div></div></div></div>";
	interfaces[ tinterface ] = new Array();
	interfaces[ tinterface ]["inc"] = new Array();
	interfaces[ tinterface ]["out"] = new Array();
	for ( var i = 0 ; i < $history ; i++ ){
		interfaces[tinterface]["inc"][ i ] = 0;
		interfaces[tinterface]["out"][ i ] = 0;
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

