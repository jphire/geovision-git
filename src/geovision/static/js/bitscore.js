/* Bitscore filtering & coloring related stuff */
/** http://mjijackson.com/2008/02/rgb-to-hsl-and-rgb-to-hsv-color-model-conversion-algorithms-in-javascript
 * Converts an HSV color value to RGB. Conversion formula
 * adapted from http://en.wikipedia.org/wiki/HSV_color_space.
 * Assumes h, s, and v are contained in the set [0, 1] and
 * returns r, g, and b in the set [0, 255].
 *
 * @param   Number  h       The hue
 * @param   Number  s       The saturation
 * @param   Number  v       The value
 * @return  Array           The RGB representation
 */
function hsvToRgb(h, s, v){
    var r, g, b;

    var i = Math.floor(h * 6);
    var f = h * 6 - i;
    var p = v * (1 - s);
    var q = v * (1 - f * s);
    var t = v * (1 - (1 - f) * s);

    switch(i % 6){
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
    }

    return [r * 255, g * 255, b * 255];
}
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
		// Use the HSV color model for interpolating between colors. Red is 0 degrees and green 120 degrees == 1/3: of a circle
		var hue = (minScore == maxScore) ? 1.0/3.0 : (1.0/3.0 * (bitscore - minScore) / (maxScore - minScore));
		var rgb = hsvToRgb(hue, 1.0, 1.0);
		return $jit.util.rgbToHex([Math.round(rgb[0]), Math.round(rgb[1]), Math.round(rgb[2])]);
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
		saveUndoState();
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
