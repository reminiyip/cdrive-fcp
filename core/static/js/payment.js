$(document).ready(function() {
	$('#payment-page form').on('submit', function(e) {
		e.preventDefault();

		// set to loading page
		$(this).hide();

		// submit form
		$.post({
			url : $(this).attr('action'),
			data: $(this).serialize(),
			success: function(status) {
				if (status === 'OK') {
					$('#payment-success').show();

					// redirect
					setTimeout(function() {
						window.location = '/homepage';
					}, 4000);
				}
			}
		});
	});
});