function simpleMonitor(url, callback)
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

        self.xmlHttpReq.open('GET', url, true);
        self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        self.xmlHttpReq.onreadystatechange = function() {
                if ( self.xmlHttpReq && self.xmlHttpReq.readyState == 4) {
                        callback(self.xmlHttpReq.responseText);
                }
        }

        //document.getElementById('status').style.display = "inline";

        self.xmlHttpReq.send( null );
}
