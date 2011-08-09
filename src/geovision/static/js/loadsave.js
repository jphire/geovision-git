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
$('#undo').click(function(e) {
	e.preventDefault();
	doUndo();
});
});

function addSavedViewToList(id, name)
{
	$('#savedViews').append('<div class="view">View name: <strong>'+ name +'</strong><br/><a class="load" href="/graphrefresh?open_view=' + id + '">Load</a> -' +
		' <a class="load" href="/save_view?delete=' + id + '">Delete</a> -' +
		' <a class="load" href="/export_view?type=json&id=' + id + '">Export as JSON</a>' +
		'</span><br/>');
}

var MAX_UNDO = 20;
var undoStates = [];
function saveUndoState()
{
	// $.extend is used to deep copy the array because JIT doesn't >:|
	undoStates.push({ graph: $.extend(true, [], rgraph.toJSON('graph')), root: rgraph.root.id});
	if(undoStates.length > MAX_UNDO)
		undoStates.shift();
	$('#undo').removeAttr('disabled');
}

function doUndo()
{
	if(undoStates.length == 0)
		return;
	var oldState = undoStates.pop();
	rgraph.op.morph(oldState.graph, $jit.util.merge(rgraph.op.userOptions, 
		{ id: oldState.root, onComplete: function() { /* cleanupGraph(); */colorEdges(); }}));
	if(undoStates.length == 0)
		$('#undo').attr('disabled', 'disabled');
}
