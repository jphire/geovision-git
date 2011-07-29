function prepareJSON(json)
{
	for (i in json)
	{
		var data = json[i].data;
		if(data.type == "enzyme")
			data.$color = '#0000FF';
		else if (data.type == "dbentry")
			data.$color = '#00FF00';
		for(adj in data.adjacencies)
				data.adjacencies[adj].data.$direction = data.adjacenction[adj].nodeTo;
	}
	return json;
}
function fetchJSON(node)
{

			busy = 'expanding';
			rgraph.canvas.getElement().style.cursor = 'wait';
			$('#load').html("Loading...");
			$.getJSON(json_base_url + '&depth=1&' + node.data.type + '=' + node.name,
				function(newdata)
				{
					graph = rgraph.construct(newdata)
					//UPDATE HIDDEN NODE INFO IN ALREADY EXISTING NODES
					var graphNode = graph.getNode(node.id);
					
					if(graphNode){
						var graphNodeData = graphNode.data;
						node.data.hidden_nodes_count = graphNodeData['hidden_nodes_count'];
					}
					
					var settings = $jit.util.merge(
						rgraph.op.userOptions,
						{
						///////// remove these when everything works
							type: 'fade:con',
							transition: $jit.Trans.linear,
							duration: 60,
							fps: 40,
						/////////
							onMerge: colorEdges,
							onComplete: function() { 
								busy = false;
								rgraph.canvas.getElement().style.cursor = '';
						}});
					rgraph.op.sum(prepareJSON(newdata), settings);
					$('#load').html("");
				});
}

function initGraph(json)
{
	jQuery('#loader').fadeOut();
	if(!json || json.error_message)
	{
		if(json)
			$("#error").text(json.error_message);
		openSearch();
		return;
	}
	initContextMenu();
	$('#infovis').disableSelection();

	rgraph = new RGraph(Config);
	rgraph.loadJSON(prepareJSON(json), 0);


	colorEdges();
	rgraph.refresh();
	rgraph.op.userOptions = $jit.util.merge(
		{ type: 'fade:seq'},
		((typeof settings != "undefined" && typeof settings.animationsettings != "undefined" && settings.animationsettings) || {}));

    rgraph.op.contractForTraversal = contractForTraversal;
	rgraph.op.filterContract = filterContract;
	rgraph.op.tagParents = tagParents;
	rgraph.op.tagSubgraph = tagSubgraph;
	rgraph.op.tagSubnodes = tagSubnodes;
	rgraph.centerToNode = centerToNode;
}


