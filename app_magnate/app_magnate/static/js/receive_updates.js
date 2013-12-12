
if (window.refreshIntervalId != undefined) {
    clearInterval(window.refreshIntervalId);
    window.refreshIntervalId = undefined;
}
window.refreshPeriodMs = 2000;
var last_ts = 0;

window.refreshIntervalId = setInterval( function() {

    $.getJSON("/dash/updates/?strictlyafter=" + last_ts, function(data) {

	if (last_ts != 0) { // Do nothing the first time. 
	    if (data.badges.length > 0) {
	        for (var i=0; i<data.badges.length; i++) {
	            alert("You've unlocked a new badge: "+data.badges[i].name);
	        }
	        $("#user_badges").load("/dash/user_badges/");
            }
	}
	last_ts = data.last_ts
    });
}, window.refreshPeriodMs );
