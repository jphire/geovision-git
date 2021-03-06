/** prepareJSON(jitJSON json) - prepare a JIT graph in JSON 'graph' form for display
 * @param json the json to be used for the graph
 * @return the 'graphified' json */
function prepareJSON(json)
{
	for (i in json)
	{
		var node = json[i];
		var data = node.data;
		if(data.type == "enzyme")
			data.$color = '#0000FF';
		else if (data.type == "dbentry")
			data.$color = '#00FF00';
		for(var adj in node.adjacencies)
		{
				// setting adj.$direction is required for making arrow tips point to the correct direction
				// Firefox actually gets them correct completely by accident without this line.
				node.adjacencies[adj].data.$direction = node.adjacencies[adj].nodeTo;
		}
	}
	return json;
}
/** setBusy(null|string msg) - Set animation busy status
 * If msg is a string, add a loading bar with the specified message and prevent all other operations
 * If msg is null, disable busy state
 * @param msg message to be shown
 */
function setBusy(msg)
{
	if(msg)
	{
		$('#load').html(msg + '...');
		rgraph.canvas.getElement().style.cursor = 'wait';
		busy = msg;
	}
	else
	{
		$('#load').html('');
		rgraph.canvas.getElement().style.cursor = '';
		busy = false;
	}
}
/** clean up the graph by removing leftover stuff
 * (e.g. edges with $alpha 0.0) that JIT tends to leave when deleting nodes.
 */
function cleanupGraph()
{
	rgraph.graph.eachNode(function(n) {
		if(n.data.$alpha < 0.01)
			rgraph.graph.removeNode(n.id);
	});
}
/**
 * expand the graph at the specified node
 * @param node JitNode from which the graph needs to expand
 */
function fetchJSON(node)
{

			setBusy('Expanding');
			var offset = [];
			node.eachAdjacency(function(adj) {
				offset.push(adj.nodeTo.id);
			});
			var args = $jit.util.merge(query, { read: '', dbentry: '', enzyme: '', depth: 1, offset: offset});
			args[node.data.type] = node.id;
			$.getJSON('/graphjson', args,
				function(newdata)
				{
					if(newdata.error_message)
					{
						console.log('Server error while loading JSON', newdata.error_message);
						setBusy(false);
						return;
					}
					else
					{
						node.data.hidden_nodes_count = newdata[0].data.hidden_nodes_count;
						rgraph.op.sum(prepareJSON(newdata), rgraph.op.userOptions);
					}
				});
}

/**
 * This function creates the graph according to the JSON data.
 */
function initGraph()
{
	$.getJSON('/graphjson', query, function(json) {
		jQuery('#loader').fadeOut();
		if(!json || json.error_message)
		{
			if(json)
				$("#navierror").text(json.error_message);
			openSearch();
			return;
		}
		initContextMenu();
		$('#infovis').disableSelection();

		rgraph = new RGraph(Config);
		rgraph.loadJSON(prepareJSON(json), query.root || 0);
		$jit.Graph.Util.computeLevels(rgraph.graph, rgraph.root, 0);
		delete query.view_id;
		delete query.root;

		colorEdges();
		rgraph.refresh();
		rgraph.op.userOptions = settings.animationsettings;
		rgraph.op.tagParents = tagParents;
		rgraph.op.tagSubgraph = tagSubgraph;
		rgraph.op.tagSubnodes = tagSubnodes;
		rgraph.op.deleteUntagged = deleteUntagged;
	});
}


