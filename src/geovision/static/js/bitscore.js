/* Bitscore filtering & coloring related stuff */
var bitscoreColorMin, bitscoreColorMax;
function colorEdges(){

	maxScore = 0;
	minScore = 100000;
	$jit.Graph.Util.eachNode(rgraph.graph, function(node) {
		var nodeMaxScore = 0;
		$jit.Graph.Util.eachAdjacency(node, function(adj) {
			var bs = adj.data.bitscore;
			if(!bs) return;
			if(bs > maxScore)
				maxScore = bs;
			if(bs < minScore)
				minScore = bs;
			if(bs > nodeMaxScore)
				nodeMaxScore = bs;
		});
		if(node.data.type == 'enzyme')
			node.data.bitscore = nodeMaxScore;
	});
	if(bitscoreColorMin)
	{
		minScore = bitscoreColorMin;
		maxScore = bitscoreColorMax;
	}
	function color(bitscore)
	{
		if(bitscoreColorMin)
		{
			if(bitscore > bitscoreColorMax)
				return '#00ff00';
			if(bitscore < bitscoreColorMin)
				return '#ff0000';
		}
		grncol = (minScore == maxScore) ? 255 : Math.floor((1.0 * (bitscore - minScore) / (maxScore - minScore)) * 255);
		return $jit.util.rgbToHex([255 - grncol, grncol, 0]);
	}
	$jit.Graph.Util.eachNode(rgraph.graph, function(node) {
		$jit.Graph.Util.eachAdjacency(node, function(adj) {
			adj.data.$color = color(adj.data.bitscore);
		});
		if(node.data.type == 'enzyme')
			node.data.color = color(node.data.bitscore);
	});
}
 /*function to filter graph by a bitscore inputted by the user*/
function filter(bitscore, masterbitscore) {
	if (!(bitscore > 0)) { /*bitscores must make sense*/
		$('#filtererror').html("Not a valid bitscore.<br/>");
	}
	if (bitscore > 0 && bitscore < masterbitscore){
		$('#filtererror').html("You cannot filter by bitscores lower than the bitscore you used to search the database.<br/>");
	}
	else {
		$('#load').html("Filtering...");

		rgraph.op.filterContract(rgraph.graph.getNode(rgraph.root), {type: "replot"});

		rgraph.graph.getNode(rgraph.root).eachAdjacency(function helper(edge){
			var target;
			if (edge.nodeTo._depth > edge.nodeFrom._depth) {
				target = edge.nodeTo;
			}
			else {
				target = edge.nodeFrom;
			}
			if (typeof(edge.data.bitscore) == "undefined" || edge.data.bitscore >= bitscore || target.traversalTag){
				var node = edge.nodeTo;
				node.ignore = false;
				node.setData('alpha', node.Node.alpha, "current");
				node.eachAdjacency(function(edgenow){
					if (edgenow.nodeTo._depth > edgenow.nodeFrom._depth && edgenow.nodeTo != edge.nodeTo){
						helper(edgenow);
					}
				})
			}
		})
		rgraph.op.viz.refresh();

		$('#load').html("");
		$('#filtererror').html("");
		return;
	}
}
function filterContract(node, opt) {
	var viz = this.viz;
	opt = $jit.util.merge(this.options, viz.config, opt || {}, {
		'modes': ['node-property:alpha:span', 'linear']
	});
	node.collapsed = true;
	(function subn(n) {
		n.eachSubnode(function(ch) {
			ch.ignore = true;
			ch.setData('alpha', 0, opt.type == 'animate'? 'end' : 'current');
			subn(ch);
		});
	})(node);
	if(opt.type == 'animate') {
		viz.compute('end');
		(function subn(n) {
			n.eachSubnode(function(ch) {
				ch.setPos(node.getPos('end'), 'end');
				subn(ch);
			});
		})(node);
		viz.fx.animate(opt);
	}
	else if(opt.type == 'replot') {
		viz.refresh();
	}
}
