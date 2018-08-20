$(function() {
	$('.stars').each(function() {
		let ua = $(this).html();
		ua = parseInt(ua).toFixed(1);
		$(this).text(ua);
	});
	$('.book_box_button').hide();
	$('.book_box').on('mouseenter', function() {
		$(this).find('.book_box_button').fadeIn(800);
		$('.book_box').on('mouseleave', function() {
			$(this).find('.book_box_button').fadeOut();
		});
	});
});