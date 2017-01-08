var sensor = '<div class="hostdiv" style="{cssDiv}">\
	<div class="callfromto">{callfromto}</div>\
	<div class="callStatus">{callStatus}</div><br>\
	<div class="callDate">{callDate}</div>\
	<div class="callDuration">{callDuration}</div>\
</div>'

$( document ).ready(function() {
	document.getElementById("defaultOpen").click();
	startAgain();
});

function startAgain(){
	$("#callLogsInternal").empty();
	$("#callLogsExternal").empty();
	$("#callLogsUnknown").empty();

	$.getJSON("getCallHistory.json?limit=100").done(function(data){
		$.each(data, function(i, item){
			var tmpsensor = sensor

			callTypeColor = ""
			if (item.callStatus === "ANSWERED") {
				callTypeColor = "#030"
			} else if (item.callStatus === "NO ANSWER") {
				callTypeColor = "#321"
			} else if (item.callStatus === "BUSY") {
				callTypeColor = "#122"
			} else if (item.callStatus === "FAILED") {
				callTypeColor = "#330000"
			}
			tmpsensor = tmpsensor.replace(/\{cssDiv\}/g, "background-color: " + callTypeColor)

			tmpsensor = tmpsensor.replace(/\{callfromto\}/g, item.callFrom + ' -> ' + item.callTo)
			tmpsensor = tmpsensor.replace(/\{callDuration\}/g, item.callDuration + ' sec')
			tmpsensor = tmpsensor.replace(/\{callStatus\}/g, item.callStatus)
			tmpsensor = tmpsensor.replace(/\{callDate\}/g, item.callDate)

			if (item.callFromType === "internal" && item.callToType === "internal")
				$(tmpsensor).appendTo("#callLogsInternal");
			else if (item.callFromType === "external" || item.callToType === "external")
				$(tmpsensor).appendTo("#callLogsExternal");
			else
				$(tmpsensor).appendTo("#callLogsUnknown");
		});
	});
}

function openCity(evt, cityName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}
