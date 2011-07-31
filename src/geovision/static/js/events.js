Config.Events = 
{
	enableForEdges: true,
	enable : true,
	type : 'Native', //edge event doesn't work with 'HTML'..

	onClick: function(node, opt)
	{
		if(!node || node.nodeFrom)
			return;

		numSubnodes = 0;
		$jit.Graph.Util.eachAdjacency(node, function(adj) {
			if(adj.nodeFrom == node && adj.data.blast_id)
				numSubnodes++;
		});

		//if clicked a leaf-node
		if (numSubnodes <= 1)
		{
			if(busy)
				return;

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
					
					rgraph.op.sum(prepareJSON(newdata), $jit.util.merge(
						rgraph.op.userOptions, 
						{
							onMerge: colorEdges,
							onComplete: function() { 
								busy = false;
								rgraph.canvas.getElement().style.cursor = '';
						},
						}));
					$('#load').html("");
				}
			);
		}
		//the clicked node is not a leaf node
		else
		{
			if(node.collapsed) 
			{
				if(busy)
					return;

				busy = 'expanding';
				rgraph.canvas.getElement().style.cursor = 'wait';
				$('#load').html("Loading...");
				rgraph.op.expand(
					node, $jit.util.merge(
						defaultsettings.animationsettings,
						settings.animationsetting,
						{ onComplete: function() {
							colorEdges(); 
							busy = false; 
							rgraph.canvas.getElement().style.cursor = ''; 
						}}));
				$('#load').html("");
			}
			else 
			{
				if(busy)
					return;

				busy = 'contracting';
				rgraph.canvas.getElement().style.cursor = 'wait';
				$('#load').html("Contracting...");
				rgraph.op.contractForTraversal(
                    node, $jit.util.merge(
						rgraph.op.userOptions, 
						{ onComplete: function() {
								colorEdges();
								busy = false;
								rgraph.canvas.getElement().style.cursor = ''; 
								}}));
				$('#load').html("");
			}
		}
		//show clicked node's info in the right column
		$jit.id('inner-details').innerHTML = ""
		$jit.id('inner-details').innerHTML += "<b>" + node.id + "</b><br/>"
		$jit.id('inner-details').innerHTML += node.data.description + "<br/>"
		if(node.data.type == 'enzyme'){
			$.getJSON('/enzyme_data?id=' + node.id, showEnzymeData);
		}
	},
	onMouseEnter: function(node, eventInfo, e)
	{
		if(ctxMenuOpen)
			return;

		if (node.nodeTo)
		{
			if(busy)
				return;
			currentEdge = node;

			rgraph.canvas.getElement().style.cursor = 'pointer';
		}
		else if(node)
		{
			if(busy)
				return;
			currentNode = node;

			rgraph.canvas.getElement().style.cursor = 'pointer';
		}
	},
	onMouseLeave: function(object, eventInfo, e)
	{
		if(ctxMenuOpen)
			return;
		if(!object)
			return;
		currentNode = currentEdge = undefined;
		
		if(object.nodeTo)
		{
			if(busy)
				return;
			rgraph.canvas.getElement().style.cursor = '';
		}
		else if(object){
			if(busy)
				return;

			rgraph.canvas.getElement().style.cursor = '';
		}
	}
};
