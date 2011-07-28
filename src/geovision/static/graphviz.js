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
		((typeof settings != "undefined" && settings.animationsettings) || {}));

    rgraph.op.contractForTraversal = contractForTraversal;
	rgraph.op.filterContract = filterContract;
	rgraph.op.tagParents = tagParents;
	rgraph.op.tagSubgraph = tagSubgraph;
	rgraph.op.tagSubnodes = tagSubnodes;
	rgraph.centerToNode = centerToNode;
}


