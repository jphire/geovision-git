/* prepareJSON(jitJSON json) - prepare a JIT graph in JSON 'graph' form for display */ 
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
/* setBusy(null|string msg) - Set animation busy status
 * If msg is a string, add a loading bar with the specified message and prevent all other operations
 * If msg is null, disable busy state
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
/* cleanupGraph() - clean up the graph by removing leftover stuff
 * (e.g. edges with $alpha 0.0) that JIT tends to leave when deleting nodes.
 */
function cleanupGraph()
{
	var toDelete = [];
	rgraph.graph.eachNode(function(n) {
		n.eachAdjacency(function(adj) {				
			if(adj.data.$alpha < 0.01)
			{
				delete rgraph.graph.edges[adj.nodeFrom.id][adj.nodeTo.id];
				delete rgraph.graph.edges[adj.nodeTo.id][adj.nodeFrom.id];
			}
		});
	});
}
/* fetchJSON(JitNode node) - expand the graph at the specified node */
function fetchJSON(node)
{

			setBusy('Expanding');
			var args = $jit.util.merge(query, { read: '', dbentry: '', enzyme: '', depth: 1, offset: node.data.min_bitscore});
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
			delete query.view_id
			delete query.root

			colorEdges();
			rgraph.refresh();
			rgraph.op.userOptions = settings.animationsettings;

			rgraph.op.filterContract = filterContract;
			rgraph.op.tagParents = tagParents;
			rgraph.op.tagSubgraph = tagSubgraph;
			rgraph.op.tagSubnodes = tagSubnodes;
			rgraph.op.deleteUntagged = deleteUntagged;
		});
}


