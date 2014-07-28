function createCookie(name, value, days) {
    var expires;

    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    } else {
        expires = "";
    }
    document.cookie = escape(name) + "=" + escape(value) + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = escape(name) + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return unescape(c.substring(nameEQ.length, c.length));
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name, "", -1);
}




//console.log("loading file receive_updates.js, window.refreshIntervalId=" + window.refreshIntervalId + ", last_ts=" + last_ts);
if (window.refreshIntervalId != undefined) {
    //    console.log("UNregistering timer to receive updates");
    clearInterval(window.refreshIntervalId);
    window.refreshIntervalId = undefined;
}
window.refreshPeriodMs = 120000;
var last_ts = 0;
saved_last_ts = readCookie("last_ts");
if (saved_last_ts) {
    last_ts = parseInt(saved_last_ts, 10);
    //    console.log("restored from cookies, last_ts = " + last_ts);
}

function receive_updates() {
   
    //    console.log("calling receive_updates, last_ts=" + last_ts);
    $.ajax({
	    cache: false,
	    url: "/dash/updates/?strictlyafter=" + last_ts, 
	    dataType: "json",
	    success: function(data) {
	// console.log("received json " + data.badges.length + " "  + last_ts);
	if (last_ts != 0) { // Do nothing the first time. 
	    if (data.badges.length > 0) {
	        for (var i=0; i<data.badges.length; i++) {
		    //                    console.log("unlocked badge " + data.badges[i].name);
	            alert("You've unlocked a new badge: "+data.badges[i].name);
	        }
	        $("#user_badges").load("/dash/user_badges/");
            }
	}
	last_ts = data.last_ts;
	createCookie("last_ts", ""+last_ts, '');
	//	console.log("saved cookie last_ts=" + last_ts);
	//	console.log("done calling receive updates, new last_ts = " + last_ts);
	    }});

}

       // The initial call to find out which badges we have. Will be done with ?strictlyafter=0
       // Important that it is not cached! Setting cache: false above. Otherwise messageboxes get replayed, etc.
receive_updates();

window.refreshIntervalId = setInterval(receive_updates, window.refreshPeriodMs );
//console.log("registered timer to receive updates, id=" + window.refreshIntervalId);