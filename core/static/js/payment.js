$(document).ready(function() {
	$('#payment-page form').on('submit', function(e) {
		e.preventDefault();

		var errorUrl = $(this).attr('error-url');
		var successUrl = $(this).attr('success-url');

		// set to loading page
		$(this).hide();

		// submit form
		$.post({
			url : $(this).attr('action'),
			data: $(this).serialize(),
			success: function(res) {
				if (res === 'OK') {
					$('#payment-success').show();

					// redirect
					setTimeout(function() {
						window.location = successUrl;
					}, 4000);
				} else {
					$('#payment-page form').show();
					$('#payment-error').show();

					errorMsg = JSON.parse(res);
					$.each(errorMsg, function(errorKey, msg) {
						$('#payment-error .message').append('<p>' + msg + '</p>');
					});
				}
			}
		});
	});
});