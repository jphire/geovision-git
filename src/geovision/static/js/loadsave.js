jQuery(function($) {
/* Performed when the 'Save' button is pressed
 * Export the graph as JIT 'graph' style JSON annotated with the root node and the original query
 * Also add the saved graph immediately to the search bar
 */
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

/* performed when the 'Undo' button is clicked */
$('#undo').click(function(e) {
	e.preventDefault();
	doUndo();
});

/* performed when the 'Save settings' or 'Restore defaults' buttons are pressed.
 * Instead of normally POSTing the form, use AJAX to prevent page loading and having the current graph disappear.
 */
$('#settingsform, #defaultsettingsForm').submit(function(e) {
	console.log(e);
	e.preventDefault();
	console.log($(this).serialize());
	$.post('/savesettings', $(this).serialize(), function (data) {
		$('#settingmessage').html(data);
		console.log(data);
	});
	return false;
});
});

/**Adds the views name and load-, delete-, and export-buttons to the left navigation with their css-styles.
 * @param id the id of the saved view in question
 * @param name the name of the view*/
function addSavedViewToList(id, name)
{
	$('#savedViews').append('<div class="view">View name: <strong>'+ name +'</strong><br/><a class="load" href="/graphrefresh?open_view=' + id + '">Load</a> -' +
		' <a class="load" href="/save_view?delete=' + id + '">Delete</a> -' +
		' <a class="load" href="/export_view?type=json&id=' + id + '">Export as JSON</a>' +
		'</span><br/>');
}

var MAX_UNDO = 20; /* Maximum number of undo states. This could be made user configurable */
var undoStates = [];

/**Deep copies and saves the new state of the graph into undoStates.
 *If there are too many states, shifts the array. Also removes the undo-buttons disabled attribute if it has one.*/
function saveUndoState()
{
	// $.extend is used to deep copy the array because JIT doesn't >:|
	undoStates.push({ graph: $.extend(true, [], rgraph.toJSON('graph')), root: rgraph.root.id});
	if(undoStates.length > MAX_UNDO)
		undoStates.shift();
	$('#undo').removeAttr('disabled');
}

/**If there are saved states to use for undoing, morphs the graph into the last state recorded.
 * If there are no states, sets the undo-button to disabled.*/
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
