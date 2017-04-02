function parsePrice(priceStr) {
	return parseFloat(priceStr.split(" ")[1]);
}

function selectRewards(value, gamePrice, id, cart_id) {

	var prevSubtotal = parsePrice($("#subtotal-value-" + id).html());

	var discount = parseFloat(gamePrice * (value * 0.1)).toFixed(2);
	var subtotal = (gamePrice - discount).toFixed(2)
	$("#discount-value-" + id).html("HK$ " + discount);
	$("#subtotal-value-" + id).html("HK$ " + subtotal);

	var prevTotal = parsePrice($("#total-value").html());
	var total = parseFloat(parseFloat(prevTotal) - parseFloat(prevSubtotal) + parseFloat(subtotal)).toFixed(2);

	$("#total-value").html("HK$ " + total);

	// save to db
	$.get({
		url : '/cart/' + cart_id + '/assign_rewards/' + id + '/' + value + '/',
		success: function(value) {
			
		}
	});
};
