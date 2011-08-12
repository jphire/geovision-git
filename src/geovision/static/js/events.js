/* Event configurations for nodes and edges is implemented here. onClick event is
 * triggered when a node or an edge is clicked. 
 *
 * When node is is clicked, a new database query is made to fetch new adjacencies for 
 * the clicked node. fetchJSON also calls JIT graph.op.sum to sum the graphs and animate
 * the transition.
 *
 * For enzymes additional data is fetched using enzyme_data function in
 * [project root]/src/geovision/viz/views.py and shown with showEnzymeData in moreinfo.js.
 *
 * If an edge is clicked, nothing happens. The right-click functionality is implemented in 
 * contextmenu.js. 
 *
 * The onMouseEnter and onMouseLeave events change the mouse pointer style as well 
 * as some other values related to all events.
 */

Config.Events = 
{
	enableForEdges: true,
	enable : true,
	type : 'Native', //edge event doesn't work with 'HTML'

	onClick: function(node, opt){
		if(!node || node.nodeFrom)
			return;
		if(currentEdge != undefined){
			rgraph.config.Events.onMouseLeave(currentEdge);
		}
		if(currentNode != undefined){
			rgraph.config.Events.onMouseLeave(currentNode);
		}
		saveUndoState();

		// Fetch new adjacencies for the clicked node, sum and animate
		fetchJSON(node, true);

		var changed_max = false;
		if(node._depth >= max_level){
			max_level = node._depth + 2;
			changed_max = true;
		}

		// Increase the number of concentric circles if needed
		if(changed_max){
			$jit.Graph.Util.computeLevels(rgraph.graph, rgraph.root, 0);
			rgraph.canvas.canvases[1].opt.numberOfCircles = max_level;
			rgraph.canvas.canvases[1].plot();
			changed_max = false;
		}


		if(node.data.type == 'enzyme'){
			$.getJSON('/enzyme_data', { id: node.id }, showEnzymeData);
		}
		else{
			var html = '';
			var source = node.data.source || node.data.sample;
			html += "<b>" + node.id + "<br/>(" + source + ")</b><br/>";
			html += node.data.description + "<br/>";
			if(node.data.source == 'uniprot'){
				html += node.data.sub_db + "<br/>";
				html += node.data.entry_name + "<br/>";
				html += node.data.os_field + "<br/>";
				html += node.data.other_info + "<br/>";
			}

			$('#names').html(html);
		}
	},
	onMouseEnter: function(node, eventInfo, e) {
		if(ctxMenuOpen || busy)
			return;

		rgraph.canvas.getElement().style.cursor = 'pointer';

		if (node.nodeTo)
			currentEdge = node;
		else
			currentNode = node;
	},
	onMouseLeave: function(object, eventInfo, e) {
		if(ctxMenuOpen || !object || busy)
			return;
		currentNode = currentEdge = undefined;
		rgraph.canvas.getElement().style.cursor = '';
	}
};
