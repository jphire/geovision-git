/** Bitscore filtering & coloring related stuff */
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

/** Calculates colors for all adges and nodes in the graph and add that information
 * in the nodes and edges. Color can be accessed through node.data.$color.
 */
function colorEdges(){
	
	var min = Math.min, max = Math.max;
	var maxScore = 0;
	var minScore = 100000;
	rgraph.graph.eachNode(function(node) {
		var nodeMaxScore = 0;
		node.eachAdjacency(function(adj) {
			var bs = adj.data.bitscore;
			if(!bs) return;
				maxScore = max(bs, maxScore);
				minScore = min(bs, minScore);
				nodeMaxScore = max(bs, nodeMaxScore);
		});
		node.data.bitscore = nodeMaxScore;
	});
	if(bitscoreColorMin)
	{
		minScore = bitscoreColorMin;
		maxScore = bitscoreColorMax;
	}
	/** Calculates colors based on the bitscore given as argument. Returns the
	 * color in hexadecimal format.
	 * @param bitscore the birscore to be used for calculations
	 * @return a color
	 */
	function color(bitscore){
		
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
	rgraph.graph.eachNode(function(node) {
		node.eachAdjacency(function(adj) {
			adj.data.$color = color(adj.data.bitscore);
		});
		if(node.data.type == 'enzyme')
			node.data.color = color(node.data.bitscore);
	});
	return false;
}
/** Function to filter graph based on a bitscore given by the user.
 * @param bitscore the bitscore to be used for filtering
 */
function filter(bitscore) {
	if (isNaN(bitscore) || bitscore <= 0) { /*bitscores must make sense*/
		$('#filtererror').html("Not a valid bitscore.<br/>");
		return false;
	}
	saveUndoState();
	rgraph.op.deleteUntagged(bitscore);
	return true;
}
