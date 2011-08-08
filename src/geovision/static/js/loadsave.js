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
	$('#savedViews').append('View name: '+ name +'<br/>\t<a class="load" href="/graphrefresh?open_view=' + id + '">Load</a>  ' +
		' <a class="load" href="/save_view?delete=' + id + '">Delete</a>  ' +
		' <a class="load" href="/export_view?type=json&id=' + id + '">Export as JSON</a>' +
		'<br/>');
}

var MAX_UNDO = 10;
var undoStates = [];
function saveUndoState()
{
	undoStates.push(rgraph.toJSON('graph'));
	if(undoStates.length > MAX_UNDO)
		undoStates.shift();
}
function doUndo()
{
	if(undoStates.length == 0)
		return;
	var oldState = undoStates.pop();
	rgraph.op.morph(oldState, rgraph.op.userOptions);
}
