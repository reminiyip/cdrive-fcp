function parsePrice(priceStr) {
	return parseFloat(priceStr.split(" ")[1]);
}

function selectRewards(value, id, cart_id) {
	// save to db
	$.get({
		url: '/cart/' + cart_id + '/assign_rewards?game=' + id + '&value=' + value,
		success: function(res) {
			data = JSON.parse(res);

			// display new discount & subtotal
			$('#num-of-rewards-' + id).val(data.reward_value);
			$('#discount-value-' + id).html('HK$ ' + data.discount);
			$('#subtotal-value-' + id).html('HK$ ' + data.subtotal);
			$('#total-value').html("HK$ " + data.total);

			// adjust other game's reward quota
			allowed_rewards = parseInt(data.allowed_rewards);
			$('.rewards-wrapper select').each(function(i, e) {
				current_rewards = parseInt(e.value);
				console.log(current_rewards);

				// remove all options
				$(e).empty();

				// add appropriate numbers of options
				for (i = 0; i <= current_rewards + allowed_rewards; i++) {
					if (i != current_rewards) {
						$(e).append('<option>'+i+'</option>');
					} else {
						$(e).append('<option selected>'+i+'</option>');
					}
				}
			});
		},
	});
};
