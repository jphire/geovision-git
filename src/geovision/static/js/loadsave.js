jQuery(function($) {
$('#saveGraph').submit(function(e) {
	e.preventDefault();
	$.ajax('/save_view', { type: 'POST', data: 
		{ name: $('#savedGraphName').val(), data: JSON.stringify(rgraph.toJSON('graph')), csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val() },
		complete: function() { $('#saveGraphStatus').text(''); }});
	$('#saveGraphStatus').text('Saving...');
	return false;
});
});
