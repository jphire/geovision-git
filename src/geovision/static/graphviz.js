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
				node.adjacencies[adj].data.$direction = node.adjacencies[adj].nodeTo;
		}
	}
	return json;
}

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
		return newdata;
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
		delete query.view_id;
		delete query.root;

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


