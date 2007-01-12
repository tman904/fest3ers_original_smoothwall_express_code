function MM_preloadImages() {
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
    var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
    if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_swapImgRestore() {
  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}

function MM_findObj(n, d) {
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
    d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document); return x;
}

function MM_swapImage() {
  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}

function displayHelp(url) {
	window.open("/cgi-bin/help.cgi?"+url,"disposableHelpWindow","resizable=yes,status=no,scrollbars=yes,width=300,height=400");
}

/* Validation functions and related options */

function _disable(field)
{
	if ( document.getElementById(field) ){
		document.getElementById(field).disabled = true;
	}
}

function _enable(field)
{
	if ( document.getElementById(field) ){
		document.getElementById(field).disabled = false;
	}
}

function _error(field)
{
	if ( document.getElementById(field) ){
		document.getElementById(field).style.backgroundColor = '#FFdddd';
	}
}

function _ok(field)
{
	if ( document.getElementById(field) ){
		document.getElementById(field).style.backgroundColor = 'white';
	}
}
	

function portlist( selectf, inputf, enabledon, allowblank )
{
	var selectval = document.getElementById(selectf).value;
	var inputval  = document.getElementById(inputf).value;

	if ( selectval == enabledon ){
		_enable(inputf);
		validport(inputf,allowblank);
	} else {
		_ok(inputf);
		_disable(inputf);
	}
}

function validport(field,allowblank)
{
	var inputval = document.getElementById(field).value;
	/* check it for validity */
	var errored = !/^[\d:]+$/.test(inputval);
	if(!errored) {
		errored = (inputval < 1 || inputval > 0xFFFF);
	}
	if( inputval == "" && allowblank == true){
		errored = 0;
	}

	if ( errored ){
		_error(field);
	} else {
		_ok(field);
	}
}

function validip(field)
{
	var address = document.getElementById(field).value;
	var numbers = address.split( "." );
	var valid = true;

	if ( numbers.length != 4 ){
		valid = false;
	}
		
	for ( var number = 0 ; number < 4 ; number++ ){			
		if ( ! numbers[ number ] ){
			valid = false;
			break;
		}		
		
		for ( var character = 0 ; character < numbers[ number ].length ; character++ ){
			if ( 
				( numbers[ number ].charAt( character ) < '0' ) ||
				( numbers[ number ].charAt( character ) > '9' ) ){
				valid = false;
				break;
			}
		}
		
		if (( numbers[ number ] < 0 ) || ( numbers[ number ] > 255 )){
			valid = false;
		}
	}

	if ( valid ){
		_ok(field);
	} else {
		_error(field);
	}
}


