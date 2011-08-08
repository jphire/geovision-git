/* Bitscore filtering & coloring related stuff */
var bitscoreColorMin, bitscoreColorMax;
function colorEdges(){
	var min = Math.min, max = Math.max;
	var maxScore = 0;
	var minScore = 100000;
	$jit.Graph.Util.eachNode(rgraph.graph, function(node) {
		var nodeMaxScore = 0;
		var nodeMinScore = 100000;
		$jit.Graph.Util.eachAdjacency(node, function(adj) {
			var bs = adj.data.bitscore;
			if(!bs) return;
				maxScore = max(bs, maxScore);
				minScore = min(bs, minScore);
				nodeMaxScore = max(bs, nodeMaxScore);
				nodeMinScore = min(bs, nodeMinScore);
		});
		node.data.bitscore = nodeMaxScore;
		node.data.min_bitscore = nodeMinScore;
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
	return false;
}
 /*function to filter graph by a bitscore inputted by the user*/
function filter(bitscore, masterbitscore) {
	if (isNaN(bitscore) || bitscore <= 0) { /*bitscores must make sense*/
		$('#filtererror').html("Not a valid bitscore.<br/>");
		return false;
	}
	if (false && bitscore > 0 && bitscore < masterbitscore){ /*read below ^^*/
		$('#filtererror').html("You cannot filter by bitscores lower than the bitscore you used to search the database.<br/>");
	}
	else {
		rgraph.op.deleteUntagged(bitscore);
		return false;
	}
}
/*special version of contract function used only by the filter*/
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
