$( document ).ready(function() {

  $(function () {
  	$('[data-toggle="tooltip"]').tooltip()
  });
  
  var $btns = $('.btn').click(function() {
    if (this.id == 'all') {
      $('#external > div').fadeIn(450);
      console.log("show all");
    } else {
      var $el = $('.' + this.id).fadeIn(450);
      $('#external > div').not($el).hide();
      console.log("rm some");
    }
    $btns.removeClass('active');
    $(this).addClass('active');
  })

});

function addContact(){
	senddata = {
		"method": "new",
		"cnt_name": $("#cnt_name").val(),
		"cnt_number": $("#cnt_number").val()
	}
	console.log(senddata)
	$.post("contacts.html", senddata, function(data){
		console.log(data);
		if (data.error == false)
			location.reload();
	});
}
function delContact(number){
	senddata = {
		"method": "del",
		"cnt_number": number
	}
	console.log(senddata)
	if (confirm('Are you sure you want to delete this number?')) {
		$.post("contacts.html", senddata, function(data){
			console.log(data);
			if (data.error == false)
				location.reload();
		});
	}
}

function addBlockedContact(){
	senddata = {
		"method": "new",
		"blcnt_number": $("#blcnt_number").val()
	}
	console.log(senddata)
	$.post("blockedcontacts.html", senddata, function(data){
		console.log(data);
		location.reload();
	});
}
