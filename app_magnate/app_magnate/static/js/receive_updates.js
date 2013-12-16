
if (window.refreshIntervalId != undefined) {
    clearInterval(window.refreshIntervalId);
    window.refreshIntervalId = undefined;
}
window.refreshPeriodMs = 2000;
var last_ts = 0;

function receive_updates() {
   

    $.getJSON("/dash/updates/?strictlyafter=" + last_ts, function(data) {
	console.log("received json " + data.badges.length + " "  + last_ts);
	if (last_ts != 0) { // Do nothing the first time. 
	    if (data.badges.length > 0) {
	        for (var i=0; i<data.badges.length; i++) {
                    console.log("unlocked badge " + data.badges[i].name);
	            alert("You've unlocked a new badge: "+data.badges[i].name);
	        }
	        $("#user_badges").load("/dash/user_badges/");
            }
	}
	last_ts = data.last_ts
    });
}

// Call right away to initialize. So that if something happens, we can detect that this is new. 
// (Better solutions are possible, but this is still better than nothing. Otherwise if the user e.g. likes something within the first second, before the first timer event, he/she won't see the badges for that, if any, until page refresh.)
receive_updates();


window.refreshIntervalId = setInterval(receive_updates, window.refreshPeriodMs );
