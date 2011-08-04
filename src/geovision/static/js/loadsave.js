jQuery(function($) {
$('#saveGraph').submit(function(e) {
	e.preventDefault();
	var name = $('#savedGraphName').val();
	$.post('/save_view', { name: name, 
			graph: JSON.stringify(rgraph.toJSON('graph')), 
			query: JSON.stringify($jit.util.merge(query, {'root': rgraph.root.id})), 
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val() },
		function(data) { $('#saveGraphStatus').text(''); addSavedViewToList(data, name); });
	$('#saveGraphStatus').text('Saving...');
	return false;
});
});

function addSavedViewToList(id, name)
{
	$('#savedViews').append('<a href="/graphrefresh?open_view=' + id + '">' + name + '</a>' + 
		' <a href="/save_view?delete=' + id + '">Delete</a>' +
		' <a href="/export_view?type=json&id=' + id + '">Export as JSON</a>' +
		'<br/>');
}
