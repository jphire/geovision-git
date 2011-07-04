var opened = false;

function openSearch()
{
	elem = $('#graphnavi')
        if (!opened){
            opened = true;
            elem.find('#optiontag').hide();
            elem.animate({width: "30%"}, {complete:
		function() { elem.find('*').not('#optiontag').fadeIn(); }});
	}
}
function closeSearch()
{
	if (opened){
		$('#graphnavi').find('*').hide();/*!Hide all elements*/
		$('#graphnavi').animate({width: "7px"}, {complete: function() {
                       $(this).find('#optiontag').fadeIn();
                       opened = false;
		}});
	}
}
jQuery(function($) {
/*! Function to open the graph-option-navigation and the alignment with a nice animation.
 */
    $('#graphnavi').mouseenter(openSearch);
    $('#close').click(closeSearch);
    $('#graphrefresh').click(function(){
		$('#loader').fadeIn(); //loader in
    });
	$('.submitForm').live('click', function() {
		$('#ec').replaceWith('<input size="10" type="text" name="ecnumber" id="ec" value="'+$(this).attr('id')+'"/>');
		$(this).parents('form').submit();
	})
}); //jquery close

