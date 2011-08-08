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

		saveUndoState();
		fetchJSON(node, true);
		//show clicked node's info in the right column
		/*
		$jit.id('inner-details').innerHTML = ""
		$jit.id('inner-details').innerHTML += "<b>" + node.id + "</b><br/>"
		$jit.id('inner-details').innerHTML += node.data.description + "<br/>"
		*/
		if(node.data.type == 'enzyme'){
			$.getJSON('/enzyme_data', { id: node.id }, showEnzymeData);
		}
	},
	onMouseEnter: function(node, eventInfo, e)
	{
		if(ctxMenuOpen || busy)
			return;

		rgraph.canvas.getElement().style.cursor = 'pointer';

		if (node.nodeTo)
			currentEdge = node;
		else
			currentNode = node;
	},
	onMouseLeave: function(object, eventInfo, e)
	{
		if(ctxMenuOpen || !object || busy)
			return;
		currentNode = currentEdge = undefined;
		rgraph.canvas.getElement().style.cursor = '';
	}
};
