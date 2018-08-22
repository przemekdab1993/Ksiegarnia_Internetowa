function hide_book_box() 
{
	$('.book_box_button').hide();
	$('.book_box').on('mouseenter', function() {
		$(this).find('.book_box_button').fadeIn(500);
		$('.book_box').on('mouseleave', function() {
			$(this).find('.book_box_button').fadeOut(200);
		});
	});
}


$(function() {
	$('.stars').each(function() {
		let ua = $(this).text();
		ua = parseFloat(ua);
		$(this).text(ua.toFixed(1));
	});
	hide_book_box();
	
	$('.button_sort').not('#b_sort0').not('#b_sort1').on('click', function() {
		$('.button_sort').removeClass('button_sort_clicked');
		$(this).addClass('button_sort_clicked');
		$('.book_box').hide();
		let sort_by = $(this).text().toLowerCase();
		$('.book_box .type').each(function() {
			let type = $(this).text();
			if (type == sort_by)
			{
				$(this).parent().fadeIn(800);
			}
		});
	});
	$('#b_sort0').on('click', function() {
		$('.button_sort').removeClass('button_sort_clicked');
		$(this).addClass('button_sort_clicked');
		
		var $sort = $('.book_box').sort(function (a, b) {
			let contentA = parseInt( $(a).data('sort'));
			let contentB = parseInt( $(b).data('sort'));
			return (contentA < contentB);
		});
		$('#books_container').html($sort);
		$('.book_box').hide().fadeIn(800);
		hide_book_box();
	});
	$('#b_sort1').on('click', function() {
		$('.button_sort').removeClass('button_sort_clicked');
		$(this).addClass('button_sort_clicked');
		
		var $sort = $('.book_box').sort(function (a, b) {
			let contentA = parseInt( $(a).find('.stars').text());
			let contentB = parseInt( $(b).find('.stars').text());
			return (contentA < contentB);
		});
		$('#books_container').html($sort);
		$('.book_box').hide().fadeIn(800);
		hide_book_box();
	});
	$('#button_info').on('submit', function() {
		
	});
});