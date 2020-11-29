$(document).ready(function() {


$('ul').on('click', '.shopping-item-delete', function(event) {
	$(this).parent().parent().remove();  
	console.log('remove button pressed');
});


$('ul').on('click', '.shopping-item-toggle', function(event) {

	$(this).parent().parent().find('.shopping-item').toggleClass('shopping-item__checked');
	
	console.log('toggle button pressed');
});



$('#js-shopping-list-form').submit(function(event) {
	console.log('add item button pressed');

	txt = $('#shopping-list-entry').val();



	$('ul').append(
		$('<li>').append([
			$('<span>').attr('class', 'shopping-item').append(txt),
			$('<div>').attr('class', 'shopping-item-controls').append([
          		$('<button>').attr('class', 'shopping-item-toggle').append(
            		$('<span>').attr('class', 'button-label').append('check')),
                 $('<button>').attr('class', 'shopping-item-delete').append(
            		$('<span>').attr('class', 'button-label').append('delete'))])]
			));


	console.log(txt);
	event.preventDefault(); //Prevent page refresh

});



//$('li').css('background-color', 'steelblue'); 



});