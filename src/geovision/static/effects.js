var opened = false;
var settingsopen = false;
var helpopen = false;
var samplesopen = false;

function openSearch()
{
	var elem = $('#graphnavi')
        if (!opened){
            elem.find('#optiontag').hide();
            elem.animate({width: "25%"}, {complete:
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
/*! Functions to open the graph-option-navigation and the alignment and other items with a nice animations.*/

	$('#sampleslink').click(function() {
		if (!samplesopen){
			$('#samples').slideDown();
			samplesopen = true;
		}
		else{
			$('#samples').slideUp();
			samplesopen = false;
		}
	})
	$('#settingslink').click(function() {
		if (!settingsopen){
			$('#settings').slideDown();
			settingsopen = true;
		}
		else{
			$('#settings').slideUp();
			settingsopen = false;
		}
	})
	$('#helplink').click(function() {
		if (!helpopen){
			$('#help').slideDown();
			helpopen = true;
		}
		else{
			$('#help').slideUp();
			helpopen = false;
		}
	})
	$('#filterform').submit(function(e) {
		e.preventDefault();
		filter(parseFloat($('#bitscorefilter').val()), parseFloat($('#masterbitscorefilter').val()));
		return false;
	})
	$('#colorform').submit(function(){
		$('#colorErrorMsg').text('');
		if($('#colortypeDynamic').attr('checked'))
			setBitscoreColoring();
		else
		{
			var min = parseFloat($('#colorMin').val()), max = parseFloat($('#colorMax').val());
			if(min > 0 && max > min)
				setBitscoreColoring(min, max);
			else
				$('#colorErrorMsg').text('Enter valid numbers');
		}
		return false;
	});

	$('#colortypeCustom').click(function(n){
		$('#colorMin, #colorMax').removeAttr('disabled');
	});
	$('#colortypeDynamic').click(function(n){
		$('#colorErrorMsg').text('');
		$('#colorMin, #colorMax').attr('disabled', 'disabled');
	});

    $('#graphnavi').mouseenter(openSearch);
	$('#graphnavi').mouseleave(closeSearch);
    $('#graphrefresh').click(function(){
		$('#loader').fadeIn(); //loader in
    });
	$('.submitForm').live('click', function() {
		console.log();
		$('#ec').val($(this).text());
		$(this).parents('form').submit();
	})
}); //jquery close

function setBitscoreColoring(min, max)
{
	if(!min)
		bitscoreColorMin = bitscoreColorMax = null;
	else
	{
		bitscoreColorMin = min;
		bitscoreColorMax = max;
	}
	colorEdges();
	rgraph.refresh();
}
