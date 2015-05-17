$(document).on('ready', function(){
	console.log("DOM loaded");

	$('#the_submit').on('submit', function(e){
		e.preventDefault();
		console.log("CLICK");
		var fn = $("#firstName").val();
		var sn = $("#surname").val();
		var formData = {"fn": fn, "sn": sn};

		$.ajax({
			url: '/ufc/fighter/query/',
			data: formData,
			method: 'POST',
			type: 'JSON',
			success: function(status, jqXHR, error){
				console.log(jqXHR);
			}
		}).done(function(data){
			console.log("ajax done");
		}).fail(function(error){
			console.log("error: "+error)
		})


	});
})