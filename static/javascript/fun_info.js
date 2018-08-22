$(function() {
	var check = $('.grand_book').length;
	if (check < 1)
	{	
		$('.main_container').text("Przepraszamy ale strona nie otrzymała danych z serwera. Proszę spróbować innym razem.");
	}
	
	var stars = $('#i-stars').text();
	stars = parseFloat(stars);
	let buf = '<span class="i-text">Ocena: ' + stars.toString() + '</span>';
	for (let i = 0; i < stars; i++)
	{
		buf += '&Delta;';
	}	
	$('#i-stars').html(buf);
});