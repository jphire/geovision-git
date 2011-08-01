Config.Events = 
{
	enableForEdges: true,
	enable : true,
	type : 'Native', //edge event doesn't work with 'HTML'..

	onClick: function(node, opt)
	{
		if(!node || node.nodeFrom)
			return;
		if(currentEdge != undefined){
			
			rgraph.config.Events.onMouseLeave(currentEdge);
		}
		if(currentNode != undefined){
			
			rgraph.config.Events.onMouseLeave(currentNode);
		}

		//if clicked an unopened node
		if (!node.data.opened)
		{
			if(busy)
				return;
			node.data.opened = true;
			fetchJSON(node);
		}
		else
		{
			fetchJSON(node, true);
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
