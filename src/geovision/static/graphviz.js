var labelType, useGradients, nativeTextSupport, animate;

(function() {
  var ua = navigator.userAgent,
	  iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
	  typeOfCanvas = typeof HTMLCanvasElement,
	  nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
	  textSupport = nativeCanvasSupport 
		&& (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
  //I'm setting this based on the fact that ExCanvas provides text support for IE
  //and that as of today iPhone/iPad current text support is lame
  labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
  nativeTextSupport = labelType == 'Native';
  useGradients = nativeCanvasSupport;
  animate = !(iStuff || !nativeCanvasSupport);
})();

var Log = {
  elem: false,
  write: function(text){
	if (!this.elem) 
		this.elem = document.getElementById('log');
	this.elem.innerHTML = text;
	this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
  }
};

function dot(u, v)
{
	return u.x * v.x + u.y * v.y;
}
function add(u, v)
{
	return {'x': u.x + v.x, 'y': u.y + v.y}

}
function sub(u, v)
{
	return {'x': u.x - v.x, 'y': u.y - v.y}
}
function mul(k, v)
{
	return {'x': k * v.x, 'y': k * v.y};
}

dotLineLength = function( x, y, x0, y0, x1, y1, o ){
	function lineLength( x, y, x0, y0 ){
		return Math.sqrt( ( x -= x0 ) * x + ( y -= y0 ) * y );
	}
	if( o && !( o = function( x, y, x0, y0, x1, y1 ){
		if( !( x1 - x0 ) ) return { x: x0, y: y };
		else if( !( y1 - y0 ) ) return { x: x, y: y0 };
		var left, tg = -1 / ( ( y1 - y0 ) / ( x1 - x0 ) );
		return { x: left = ( x1 * ( x * tg - y + y0 ) + x0 * ( x * - tg + y - y1 ) ) / ( tg * ( x1 - x0 ) + y0 - y1 ), y: tg * left - tg * x + y };
	}( x, y, x0, y0, x1, y1 ), o.x >= Math.min( x0, x1 ) && o.x <= Math.max( x0, x1 ) && o.y >= Math.min( y0, y1 ) && o.y <= Math.max( y0, y1 ) ) ){
		var l1 = lineLength( x, y, x0, y0 ), l2 = lineLength( x, y, x1, y1 );
		return l1 > l2 ? l2 : l1;
	}
	else {
		var a = y0 - y1, b = x1 - x0, c = x0 * y1 - y0 * x1;
		return Math.abs( a * x + b * y + c ) / Math.sqrt( a * a + b * b );
	}
};

$jit.RGraph.Plot.EdgeTypes.implement({  
	'customArrow':{
	    'render': function(adj, canvas) {
            var from = adj.nodeFrom.pos.getc(true),
                to = adj.nodeTo.pos.getc(true),
                dim = adj.getData('dim'),
                direction = adj.data.$direction,
                inv = (direction && direction.length>1 && direction[0] != adj.nodeFrom.id);
            this.edgeHelper.arrow.render(from, to, dim, inv, canvas);
        },
        'contains': function(adj, pos) {
            var from = adj.nodeFrom.pos.getc(true),
		        to = adj.nodeTo.pos.getc(true);
            var lineWidth = adj.getData('epsilon');
            var d = lineWidth/2;
            var minX = Math.min(from.x, to.x) - d, maxX = Math.max(from.x, to.x) + d;
            var minY = Math.min(from.y, to.y) - d, maxY = Math.max(from.y, to.y) + d;
            if(pos.x < minX || pos.x > maxX || pos.y < minY || pos.y > maxY)
	            return false;
        return dotLineLength(pos.x, pos.y, from.x, from.y, to.x, to.y, false) < lineWidth;
	    }
    }
});  

function init(){
	//init data
	jQuery('#loader').fadeOut();//loader fadeaway
}

function prepareJSON(json)
{
	for (i in json)
	{
//		if(json[i].data.type == "enzyme")
//			json[i].data.$color = '#0000FF';
	}
	return json;
}

var rgraph;
var busy = false;
function initGraph(json)
{
	if(json.error_message)
	{
		document.getElementById("error").innerHTML = json.error_message;
		openSearch();
		return;
	}

	$('#infovis').disableSelection();

	rgraph = new $jit.RGraph({
		//Where to append the visualization
		injectInto: 'infovis',
		//set canvas size
		width: 600,
		height: 600,

		//Optional: create a background canvas that plots
		//concentric circles.
		background: { CanvasStyles: { strokeStyle: '#555' } },

		//set distance for nodes on different levels
		levelDistance: 100,

		//set transformation speed
		duration: 500,
		fps: 40,

		//set transformation style
		transition: $jit.Trans.Circ,

		//Add navigation capabilities:
		//zooming by scrolling and panning.
		Navigation:
		{
		  enable: true,
		  panning: true,
		  zooming: 25
		},
		
		//Set Node and Edge styles.
		Node:
		{
			overridable: true,
			color: '#ff0000',
			alpha: 0.6,
			dim: 5.0,
			lineWidth: 0.5,
			angularWidth: 1,
			span:1,
			type: 'circle',
			CanvasStyles: {}
		},
		
		Edge:
		{
			overridable: true,
			color: '#888800',
			alpha: 0.6,
			lineWidth:1.5,
			type: 'customArrow',
			epsilon: 5.0,
			dim: 10,
		},

		Events:
		{
			enableForEdges: true,
			enable : true,
			type : 'Native', //edge event doesn't work with 'HTML'..

			onRightClick : function(node, eventInfo, e)
			{
				if (node.nodeFrom)
				{
					alignmentfunction(node.data.id);
				}
                else 
                {
                    node.traversalTag = true;
                    console.log(node.traversalTag);
                }
			},

			onClick: function(node, opt)
			{
				if(!node || node.nodeFrom)
					return;

				if(busy)
					return;
				numSubnodes = $jit.Graph.Util.getSubnodes(node).length;
				if (numSubnodes == 1)
				{
					busy = 'expanding';
					$.getJSON(json_base_url + '&depth=1&' + node.data.type + '=' + node.name,
						function(newdata)
						{
							rgraph.op.sum(prepareJSON(newdata), { type: 'fade:con', fps:30, duration: 500, hideLabels: false, onMerge: colorEdges, onComplete: function() { busy = false;}})
						}
					);
				}
				else
				{
					if(node.collapsed) 
                    {
                        busy = 'expanding';
                        rgraph.op.expand(node, 
                                { type: 'animate', 
                                duration: 1000, 
                                hideLabels: true, 
                                transition: $jit.Trans.Quart.easeOut, 
                                onComplete: function() {colorEdges(); busy = false}});
                    }
                    else 
                    {
                        busy = 'contracting';
                        rgraph.op.contract(node, 
                                { type: 'animate', 
                                duration: 1000, 
                                hideLabels: true, 
                                transition: $jit.Trans.Quart.easeOut, 
                                onComplete: function() {colorEdges(); busy = false}});
    				}
				}
			},

			onMouseEnter: function(node, eventInfo, e)
			{ 
				if (node.nodeTo)
				{
					rgraph.canvas.getElement().style.cursor = 'pointer';
					node.data.$lineWidth = node.getData('epsilon');
					
					if(busy)
						return;
					rgraph.fx.animate(
					{
						modes: ['edge-property:lineWidth'],
						duration: 500
					});
				}
				else if(node)
				{
					rgraph.canvas.getElement().style.cursor = 'pointer';
					node.data.$dim = node.getData('dim') + 3;
					
					if(busy)
						return;
					rgraph.fx.animate(
					{
						modes: ['node-property:dim'],
						duration: 500
					});

				}
			},
			onMouseLeave: function(object, eventInfo, e)
			{
				//rgraph.config.Tips.type = 'HTML';
				if(!object) return;
				if(object.nodeTo)
				{
					rgraph.canvas.getElement().style.cursor = '';
					
					object.data.$lineWidth = rgraph.config.Edge.lineWidth;
					
					if(busy)
						return;
					rgraph.fx.animate(
					{
						modes: ['edge-property:lineWidth'],
						duration: 1
					});

				}
				else if(object){
					
					rgraph.canvas.getElement().style.cursor = '';
					object.data.$dim = rgraph.config.Node.dim;
					
					if(busy)
						return;
					rgraph.fx.animate(
					{
						modes: ['edge-property:dim'],
						duration: 1
					});

				}
			}
		},
		//Label styling is done via CSS!
		Label:
		{
			$extend: true,
			type: 'HTML',
			overridable: true
		},

		//Set tooltip configuration
		Tips:
		{
			enable: true,
			type: 'Native',
			width: 30,
			align: 'left',
			
			onShow: function(tip, node)
			{
				tip.innerHTML = "";
				if (!node) return;

				if(node.nodeFrom)
				{
					if(node.data.bitscore)
					{
						//it's an edge
						tip.innerHTML += "bitscore: " + node.data.bitscore + "<br/>";
						tip.innerHTML += "e-value: " + node.data.error_value + "<br/>";
					}
					else
						tip.innerHTML = 'enzyme edge';
				}
				else if(node.data.type != 'enzyme')
				{
					//it's a read or db entry
					tip.innerHTML += "<b>" + node.id + "</b><br/>";
					tip.innerHTML += node.data.description + "<br/>";
				}
				else
				{
					tip.innerHTML = "<b>" + node.id + "</b>";
				}
			}
		},
		onBeforeCompute: function(node)
		{
			//Add the relation list in the right column.
			//This list is taken from the data property of each JSON node.
			$jit.id('inner-details').innerHTML = ""
			$jit.id('inner-details').innerHTML += "<b>" + node.id + "</b><br/>"
			if(node.data.bitscore){
				$jit.id('inner-details').innerHTML += node.data.description + "<br/>"
			}
		},
		
		onAfterCompute: function() {},

		//Add the name of the node in the correponding label
		//and a click handler to move the graph.
		//This method is called once, on label creation.
		onCreateLabel: function(domElement, node)
		{
			if(node.name)
				domElement.innerHTML = node.name.substr(0, 10);
			domElement.onclick = function() { rgraph.config.Events.onClick(node); };
		},
		//Change some label dom properties.
		//This method is called each time a label is plotted.
		onPlaceLabel: function(domElement, node)
		{
			var style = domElement.style;
			style.display = '';
			style.cursor = 'pointer';

			var left = parseInt(style.left);
			var w = domElement.offsetWidth;
			style.left = (left - w / 2) + 'px';

			return;

			if (node._depth <= 2) {
				style.fontSize = "1.1em";
				style.color = "#ccc";
			
			} else if(node._depth == 3){
				style.fontSize = "1.1em";
				style.color = "#494949";
			
			} else {
				style.display = 'none';
			}
		}		
	});

	//load JSON data, second argument is the index of the centered node
	rgraph.loadJSON(prepareJSON(json), 0);
	//trigger small animation

	rgraph.graph.eachNode(function(n) {
	  var pos = n.getPos();
	  pos.setc(-200, -200);
	});
	rgraph.compute('end');
	rgraph.fx.animate({
	  modes:['polar'],
	  duration: 1000
	});
	//end
	//append information about the root relations in the right column
	$jit.id('inner-details').innerHTML += "<b>" + rgraph.graph.getNode(rgraph.root).id + "</b><br/>";
	$jit.id('inner-details').innerHTML += rgraph.graph.getNode(rgraph.root).data.description;
	rgraph.refresh();
	colorEdges();
    rgraph.op.contract = contractForTraversal;
}

var alignmentopen = false;
function alignmentfunction(thisid) {
	if (alignmentopen) {
		closealignment();
	}
	if (alignmentopen == false){
		$.getJSON('/show_alignment', {id: thisid}, function (data) {
			if(data == null){
				return false;
			}
			alignmentopen = true;
/*			var part1 = $('<nobr>' + data.readseq + '</nobr>');
			var part2 = $('<nobr>' + data.dbseq + '</nobr>');  */
			var part1 = $('<nobr>');
			var part2 = $('<nobr>');
			for ( i = 0; i < data.readseq.length; i++){
				if (i % 95 == 0 && i>0){
					part1.append('<br/>');
					part1.appendTo($('#alignment'));
					part1 = $('<nobr>');
					part2.appendTo($('#alignment'));
					part2 = $('<nobr>');
					$('<br/><br/>').appendTo($('#alignment'));
				}
				if (data.readseq.charAt(i) === data.dbseq.charAt(i)){
					part1 = part1.append(data.readseq.charAt(i));
					part2 = part2.append(data.dbseq.charAt(i));
				}
				else {
					part1 = part1.append('<span class=\'aligndifference\'>' + data.readseq.charAt(i) + '</span>');
					part2 = part2.append('<span class=\'aligndifference\'>' + data.dbseq.charAt(i) + '</span>');
				}
			}
	/*		part1 = part1.append('</nobr>');
			part2 = part2.append('</nobr>');
			part1.css('display', 'none');
			part2.css('display', 'none'); */
			part1.appendTo($('#alignment'));
			$('<br/>').appendTo($('#alignment'));
			part2.appendTo($('#alignment'));
			$('#alignment').slideDown(300, function() { part1.fadeIn(); part2.fadeIn();
								var close = $('<div id = "closealign">Close</div>');
								$('#alignment').before(close);
								$('#alignment').css('margin-bottom', '10px');
			});
		});
		return false;
	}
	else {
		return false;
	}
}
$('#closealign').live('click', function() {
	closealignment();
});
function closealignment () {
	if (alignmentopen == true){
		alignmentopen = false;
		$('#alignment').find('*').remove();/*!Hide all elements*/
		$('#closealign').remove();
		$('#alignment').css('margin-bottom', '0px');
		$('#alignment').slideUp();
	}
}

function formatHex(num)
{
	str = num.toString(16);
	if(str.length == 1)
		str = "0" + str;
	return str;
}

function colorEdges(){
	maxScore = 0;
	minScore = 100000;
	$jit.Graph.Util.eachNode(rgraph.graph, function(node) {
		$jit.Graph.Util.eachAdjacency(node, function(adj) {
			if(adj.data.bitscore > maxScore)
				maxScore = adj.data.bitscore;
			if(adj.data.bitscore < minScore)
				minScore = adj.data.bitscore;
		});
	});
	$jit.Graph.Util.eachNode(rgraph.graph, function(node) {
		$jit.Graph.Util.eachAdjacency(node, function(adj) {
			if(adj.data.bitscore) // XXX - is a blast
			{
				grncol = Math.floor((1.0 * (adj.data.bitscore - minScore) / (maxScore - minScore)) * 255);
				col = "#" + formatHex(255 - grncol) + formatHex(grncol) + "00";
				adj.data.$color = col;
				adj.data.color = col;
			}
			else
			{
				adj.data.$color = '#0000ff';
				adj.data.color = '#0000ff';
			}
		});
	});
}

/*
 * Modified version of the original contract function for removing unnecessary
 * nodes while traversing the graph.
 */

function contractForTraversal(node, opt) {
    console.log("contractForTraversal");
  var viz = this.viz;
  if(node.collapsed || !node.anySubnode($jit.util.lambda(true))) return;
  opt = $jit.util.merge(this.options, viz.config, opt || {}, {
    'modes': ['node-property:alpha:span', 'linear']
  });
  node.collapsed = true;
  (function subn(n) {
    n.eachSubnode(function(ch) {
        if (!ch.traversalTag) 
        {
            ch.ignore = true;
            ch.setData('alpha', 0, opt.type == 'animate'? 'end' : 'current');
            subn(ch);
      }
    });
  })(node);
  if(opt.type == 'animate') {
    viz.compute('end');
    if(viz.rotated) {
      viz.rotate(viz.rotated, 'none', {
        'property':'end'
      });
    }
    (function subn(n) {
      n.eachSubnode(function(ch) {
        if (!ch.traversalTag) 
        {
            ch.setPos(node.getPos('end'), 'end');
            subn(ch);
        }
      });
    })(node);
    viz.fx.animate(opt);
  } else if(opt.type == 'replot'){
    viz.refresh();
  }
}

