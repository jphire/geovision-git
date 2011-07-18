var opened = false;

function openSearch()
{
	elem = $('#graphnavi')
        if (!opened){
            elem.find('#optiontag').hide();
            elem.animate({width: "30%"}, {complete:
			function() { $('#navicontainer').fadeIn('fast', function() { opened = true; } ); }});
	}
}
function closeSearch(e)
{
	if (opened){
		if (!e) var e = window.event;
		var tg = (window.event) ? e.srcElement : e.target;
		//if (tg.nodeName != 'DIV') return;
		var reltg = (e.relatedTarget) ? e.relatedTarget : e.toElement;
		while (reltg != tg && reltg.nodeName != 'BODY')
			reltg= reltg.parentNode
		if (reltg== tg) return;
		// Now we know that the mouse actually left the layer:
		$('#graphnavi').find('#navicontainer').hide();/*!Hide all elements*/
		$('#graphnavi').animate({width: "7px"}, {complete: function() {
                       $(this).find('#optiontag').fadeIn();
                       opened = false;
		}});
	}
}
jQuery(function($) {
/*! Function to open the graph-option-navigation and the alignment with a nice animation.
 */
	$('#filterlink').click(function() {
		if (filteropen){
			$('#filter').fadeOut();
			filteropen = false;
		}
		else{
			$('#filter').fadeIn();
			filteropen = true;
		}
	})
	$('#filterform').submit(function() {
		filter($('#bitscorefilter').val());
		return false;
	})
    $('#graphnavi').mouseenter(openSearch);
	$('#graphnavi').mouseleave(closeSearch);
    $('#graphrefresh').click(function(){
		$('#loader').fadeIn(); //loader in
    });
	$('.submitForm').live('click', function() {
		$('#ec').replaceWith('<input size="10" type="text" name="ecnumber" id="ec" value="'+$(this).attr('id')+'"/>');
		$(this).parents('form').submit();
	})
}); //jquery close

