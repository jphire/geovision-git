var labelType, useGradients, nativeTextSupport, animate;
var rgraph;

var RGraph = $jit.RGraph;

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

RGraph.Plot.NodeTypes.implement({
    'customCircle': {
      'render': function(node, canvas){
          var pos = node.pos.getc(),
              radius = node.getData('dim');
          var ctx = canvas.getCtx();
          ctx.beginPath();
          ctx.arc(pos.x, pos.y, radius, 0, Math.PI * 2, true);
          ctx.closePath();
          ctx.fill();

          if(node.traversalTag)
          {
	          ctx.fillStyle = '#ffffff';
	          ctx.beginPath();
	          ctx.arc(pos.x, pos.y, radius/2, 0, Math.PI * 2, true);
	          ctx.closePath();
	          ctx.fill();
          }


        },
        'contains': function(node, pos){
          if(node.ignore)
              return false;
          var npos = node.pos.getc(true),
              radius = node.getData('dim');
          var diffx = npos.x - pos.x,
              diffy = npos.y - pos.y,
              diff = diffx * diffx + diffy * diffy;
          return diff <= radius * radius;
        }
    }
});

RGraph.Plot.EdgeTypes.implement({  
	'customArrow':{
	    'render': function(adj, canvas) {
            var from = adj.nodeFrom.pos.getc(),
                to = adj.nodeTo.pos.getc(),
                dim = adj.getData('dim'),
                direction = adj.data.$direction,
//                swap = (direction && direction.length>1 && direction[0] != adj.nodeFrom.id);
                swap = false; // XXX - may cause bugs

            var ctx = canvas.getCtx();
            Complex = $jit.Complex;
            // invert edge direction
            if (swap) {
              var tmp = from;
              from = to;
              to = tmp;
            }
            var vect = new Complex(to.x - from.x, to.y - from.y);
	    var norm = vect.norm();
            to.$add(vect.scale(-adj.nodeTo.getData("dim") / norm));
            from.$add(vect.$scale(adj.nodeFrom.getData("dim") / norm));
            vect = new Complex(to.x - from.x, to.y - from.y);

            vect.$scale(dim / vect.norm());
            var intermediatePoint = new Complex(to.x - vect.x, to.y - vect.y),
                normal = new Complex(-vect.y / 2, vect.x / 2),
                v1 = intermediatePoint.add(normal), 
                vM = intermediatePoint.clone();
                v2 = intermediatePoint.$add(normal.$scale(-1));
            
            ctx.beginPath();
	    if(from.x != from.x) return;
            ctx.moveTo(from.x, from.y);
            ctx.lineTo(vM.x, vM.y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(v1.x, v1.y);
            ctx.lineTo(v2.x, v2.y);
            ctx.lineTo(to.x, to.y);
            ctx.closePath();
            ctx.fill();

        },
        'contains': function(adj, pos) {
            var from = adj.nodeFrom.pos.getc(),
		        to = adj.nodeTo.pos.getc();
            var lineWidth = adj.getData('epsilon');
            var d = lineWidth/2;

            var vect = new Complex(to.x - from.x, to.y - from.y);
	    var norm = vect.norm();
            to.$add(vect.scale(-adj.nodeTo.getData("dim") / norm));
            from.$add(vect.$scale(adj.nodeFrom.getData("dim") / norm));

            var minX = Math.min(from.x, to.x) - d, maxX = Math.max(from.x, to.x) + d;
            var minY = Math.min(from.y, to.y) - d, maxY = Math.max(from.y, to.y) + d;
            if(pos.x < minX || pos.x > maxX || pos.y < minY || pos.y > maxY)
	            return false;
        return dotLineLength(pos.x, pos.y, from.x, from.y, to.x, to.y, false) < lineWidth;
	    }
    }
});  

var currentNode;
var currentEdge;
var ctxMenuOpen;
var overLabel;

function hideCtxMenu()
{
	if(!ctxMenuOpen) return;
	ctxMenuOpen = false;
	busy = false;
	if(currentNode) rgraph.config.Events.onMouseLeave(currentNode)
	if(currentEdge) rgraph.config.Events.onMouseLeave(currentEdge); // XXX does this work completely?
	currentEdge = currentNode = false;
	rgraph.config.Navigation.panning = true;
	rgraph.config.Tips.enable = true;
//	rgraph.events.pressed = undefined;
}

function init(){
	//init data
	jQuery('#loader').fadeOut();//loader fadeaway

	$('#infovis').contextMenu('nodeMenu', {
		'shadow': false,
		'bindings': {
			'close': function() { },
			'e_align': function() { alignmentfunction(currentEdge.data.id); },
			'n_tag': function() { 
				if (currentNode.traversalTag != true) {
					tagNode(currentNode);
				}
				else {
					untagNode(currentNode);
				}
			},
			'n_tagparents': function() { rgraph.op.tagParents(currentNode)},
			'n_tagsubnodes': function() { rgraph.op.tagSubnodes(currentNode)},
			'n_tagsubgraph': function() { rgraph.op.tagSubgraph(currentNode)},
			'n_untagsubgraph': function() { untagSubgraph(currentNode)},
			'n_tagpath': function() { console.log(checkRootTagpath(currentNode))},
			'n_en_names': function() { showEnzymeData(currentNode); },
			'n_en_brendalink': function() { window.open('http://www.brenda-enzymes.org/php/result_flat.php4?ecno=' + currentNode.id); },
			'n_en_kegglink': function() { window.open('http://www.genome.jp/dbget-bin/www_bget?ec:' + currentNode.id); },
			'n_db_uni_link': function() { window.open('http://www.uniprot.org/uniprot/' + currentNode.id); },
			'n_db_frn_link': function() { window.open('http://www.ncrna.org/frnadb/detail.html?i_name=' + currentNode.id); }

		},
		'onContextMenu': function(event)
		{
			return currentNode || currentEdge;
		},
		'onShowMenu': function(evt, menu)
		{
			ctxMenuOpen = true;
			rgraph.config.Navigation.panning = false;
			rgraph.config.Tips.enable = false;
			rgraph.tips.hide();

			if(!currentEdge || !currentEdge.data.bitscore ) 
				$('li[id^=e_]', menu).remove();
			if(!currentNode)
				$('li[id^=n_]', menu).remove();
			else
			{
				if(currentNode.data.type != 'enzyme')
					$('li[id^=n_en_]', menu).remove();
				if(currentNode.data.type != 'dbentry')
					$('li[id^=n_db_]', menu).remove();
				else
				{
					if(currentNode.data.source != 'uniprot')
						$('li[id^=n_db_uni]', menu).remove();
					if(currentNode.data.source != 'frnadb')
						$('li[id^=n_db_frn]', menu).remove();
				}
			}
			return menu;
		},
		'onHideMenu': hideCtxMenu
	});
		
}

function prepareJSON(json)
{
	for (i in json)
	{
		var data = json[i].data;
		if(data.type == "enzyme")
			data.$color = '#0000FF';
		else if (data.type == "dbentry")
			data.$color = '#00FF00';
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

	rgraph = new RGraph({
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
		  panning: 'avoid nodes',
		  zooming: 25
		},
		
		//Set Node and Edge styles.
		Node:
		{
			overridable: true,
			color: '#ff0000',
			alpha: 0.6,
			dim: 7.0,
			lineWidth: 0.5,
			angularWidth: 1,
			span:1,
			type: 'customCircle',
			CanvasStyles: {}
		},
		
		Edge:
		{
			overridable: true,
			color: '#888800',
			alpha: 0.6,
			type: 'customArrow',

			lineWidth:1.5,
			lineWidth_hover: 5.0,
			dim: 10,
			dim_hover: 15
		},

		Events:
		{
			enableForEdges: true,
			enable : true,
			type : 'Native', //edge event doesn't work with 'HTML'..

			onClick: function(node, opt)
			{
				if(!node || node.nodeFrom)
					return;

				if(busy)
					return;
				
				numSubnodes = 0;
				$jit.Graph.Util.eachAdjacency(node, function(adj) {
					if(adj.nodeFrom == node && adj.data.bitscore)
						numSubnodes++;
				});

				if (numSubnodes <= 1)
				{
					busy = 'expanding';
					rgraph.canvas.getElement().style.cursor = 'wait';
					$('#load').html("Loading...");
					$.getJSON(json_base_url + '&depth=1&' + node.data.type + '=' + node.name,
						function(newdata)
						{
							rgraph.op.sum(prepareJSON(newdata), { type: 'fade:con', fps:30, duration: 500, hideLabels: false, onMerge: colorEdges, onComplete: function() { busy = false;rgraph.canvas.getElement().style.cursor = '';}})
							$('#load').html("");
						}
					);
				}
				else
				{
					if(node.collapsed) 
                    {
                        busy = 'expanding';
						rgraph.canvas.getElement().style.cursor = 'wait';
						$('#load').html("Loading...");
                        rgraph.op.expand(node, 
                                { type: 'animate', 
                                duration: 1000, 
                                hideLabels: true, 
                                transition: $jit.Trans.Quart.easeOut, 
                                onComplete: function() {colorEdges(); busy = false; rgraph.canvas.getElement().style.cursor = '';}});
						$('#load').html("");
                    }
                    else 
                    {
                        busy = 'contracting';
						rgraph.canvas.getElement().style.cursor = 'wait';
						$('#load').html("Contracting...");
                        rgraph.op.contractForTraversal(node, 
                                { type: 'animate',
                                duration: 1000, 
                                hideLabels: true, 
                                transition: $jit.Trans.Quart.easeOut, 
                                onComplete: function() {colorEdges(); busy = false;rgraph.canvas.getElement().style.cursor = '';}});
						$('#load').html("");
    				}
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
					node.data.$lineWidth = node.getData('lineWidth_hover');
					node.data.$dim = node.getData('dim_hover');

					rgraph.fx.animate(
					{
						modes: ['edge-property:lineWidth'],
						duration: 1
					});
				}
				else if(node)
				{
					if(busy)
						return;
					currentNode = node;

					rgraph.canvas.getElement().style.cursor = 'pointer';
					node.data.$dim = rgraph.config.Node.dim + 3;

					rgraph.fx.animate(
					{
						modes: ['node-property:dim'],
						duration: 1
					});

				}
			},
			onMouseLeave: function(object, eventInfo, e)
			{
				if(ctxMenuOpen)
					return;
				if(busy)
					return;
				currentNode = currentEdge = undefined;
				if(!object) return;
				if(object.nodeTo)
				{
					rgraph.canvas.getElement().style.cursor = '';
					object.data.$lineWidth = rgraph.config.Edge.lineWidth;
					object.data.$dim = rgraph.config.Edge.dim;

					rgraph.fx.animate(
					{
						modes: ['edge-property:lineWidth'],
						duration: 1
					});

				}
				else if(object){
					if(busy)
						return;
					rgraph.canvas.getElement().style.cursor = '';
					object.data.$dim = rgraph.config.Node.dim;

					rgraph.fx.animate(
					{
						modes: ['node-property:dim'],
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
			overridable: true,
		},

		//Set tooltip configuration
		Tips:
		{
			enable: true,
			type: 'Native',
			align: 'left',
			
			onShow: function(tip, node)
			{
				if(ctxMenuOpen)
					return false;
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
					tip.innerHTML = tip.innerHTML + "<br/>" + node.data.name;
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
			if(node.name && node.name.substr)
				domElement.innerHTML = node.name.substr(0, 10);
			domElement.onclick = function() { rgraph.config.Events.onClick(node); };
			//domElement.onmouseover = function() { rgraph.config.Events.onMouseEnter(node); };
			//domElement.onmouseout = function() { rgraph.config.Events.onMouseLeave(node); };
//			domElement.onmouseover = function() { overLabel = true; if(!ctxMenuOpen) currentNode = node; };
//			domElement.onmouseout = function() { overLabel = false; if(!ctxMenuOpen) currentNode = null; };
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
    rgraph.op.contractForTraversal = contractForTraversal;
	rgraph.op.filterContract = filterContract;
	rgraph.op.tagParents = tagParents;
	rgraph.op.tagSubgraph = tagSubgraph;
	rgraph.op.tagSubnodes = tagSubnodes;
}

var alignmentopen = false;
/*Function for showing the alignment of the read and the db-entry*/
function alignmentfunction(thisid) {
	if (alignmentopen) {
		closealignment();
	}
	if (alignmentopen == false){
		$.getJSON('/show_alignment', {id: thisid}, function (data) { /*get the json with the data*/
			if(data == null){
				return false;
			}
			alignmentopen = true;
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
					part1 = part1.append('<span>' + data.readseq.charAt(i) + '</span>');
					part2 = part2.append('<span>' + data.dbseq.charAt(i) + '</span>');
				}
				else {
					part1 = part1.append('<span class=\'aligndifference\'>' + data.readseq.charAt(i) + '</span>');
					part2 = part2.append('<span class=\'aligndifference\'>' + data.dbseq.charAt(i) + '</span>');
				}
			}
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
/*when the close button appears, it's se to work*/
$('#closealign').live('click', function() {
	closealignment();
});
/*Function to close the div-element showing the alignment*/
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
			var bs = adj.data.bitscore;
			if(!bs) return;
			if(bs > maxScore)
				maxScore = bs;
			if(bs < minScore)
				minScore = bs;
		});
	});
	$jit.Graph.Util.eachNode(rgraph.graph, function(node) {
		$jit.Graph.Util.eachAdjacency(node, function(adj) {
			if(adj.data.bitscore) // XXX - is a blast
			{
				grncol = (minScore == maxScore) ? 255 : Math.floor((1.0 * (adj.data.bitscore - minScore) / (maxScore - minScore)) * 255);
				col = "#" + formatHex(255 - grncol) + formatHex(grncol) + "00";
				adj.data.$color = col;
				//adj.data.color = col;
			}
			else
			{
				adj.data.$color = '#0000ff';
				//adj.data.color = '#0000ff';
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
			if (!ch.traversalTag) {
				ch.ignore = true;
				ch.setData('alpha', 0, opt.type == 'animate'? 'end' : 'current');
				subn(ch);
			}   
		});
	})(node);
	if(opt.type == 'animate') {
		viz.compute('end');
		if(viz.rotated) {
			viz.rotate(viz.rotated, 'none', { 'property':'end' });
		}
		(function subn(n) {
			n.eachSubnode(function(ch) {
				if (!ch.traversalTag) {
					ch.setPos(node.getPos('end'), 'end');
					subn(ch);
				}
			});
		})(node);
		viz.fx.animate(opt);
	} 
	else if(opt.type == 'replot') {
		viz.refresh();
	}
}

/*
 * Function for checking if node has a tagged path to the root node.
 */
function checkRootTagpath(node) {
	var parentNodes = node.getParents();
	if (!node.traversalTag) return false;
	if (parentNodes.length == 0) return true;
	for (var i = 0; i < parentNodes.length; i++) {
		pnode = parentNodes[i]
		if (pnode.traversalTag != true) continue;
		if (checkRootTagpath(pnode)) return true;
	}
	return false;
}

function tagNode(node) {
	if (!checkRootTagpath(node)) tagParents(node);
	node.traversalTag = true;
}

function tagParents(node) {
	var parents = node.getParents();
	while (parents.length > 0) {
		parents[0].traversalTag = true;
		console.log("Parent " + parents[0].id + " tagged");
		parents = parents[0].getParents();
	}
	node.traversalTag = true;
}

function tagSubnodes(node) {
	if (!checkRootTagpath(node)) tagParents(node);
	node.eachSubnode(function(child) {
		child.traversalTag = true;
		console.log("Child " + child.id + " tagged");
	});
	node.traversalTag = true;
}

function tagSubgraph(node) {
	if (!checkRootTagpath(node)) tagParents(node);
	node.eachSubgraph(function(child) {
		child.traversalTag = true;
		console.log("Child " + child.id + " tagged");
	});
	node.traversalTag = true;
}

/* Function to list all names, reactions and pathways related to an enzyme in the right container */
function showEnzymeData (node){
	ec = node.id;

	var html = '<br/>';
	if(node.data.reactions)
	{
		html += '<strong>Reactions of ' + ec + '</strong><br/>';
		html += $.map(node.data.reactions, function(reac){
			return 'R' + reac.id + ': ' + reac.name + ' <a target="_blank" href="http://www.genome.jp/dbget-bin/www_bget?r' + reac.id + '">[KEGG]</a><br/>'; }).join('');
	}
	if(node.data.pathways)
	{
		html += '<strong>Pathways of ' + ec + '</strong><br/>';
		html += $.map(node.data.pathways, function(pw){
			return pw.id + ': ' + pw.name + ' <a target="_blank" href="http://www.genome.jp/dbget-bin/www_bget?pathway:' + pw.id + '">[KEGG]</a><br/>'; }).join('');
	}

	names = node.data.names;

	html += '<strong>Other names of ' + ec + ':</strong><br/>';
	for (name in names){
		html = html + names[name] + '<br/>';
	}
	$('#names').html(html); /*#names is replaced fully when this is called for a new node*/
	return;
 }

function untagNode(node) {
	node.traversalTag = false;
	(function subn(n) {
		n.eachSubnode(function(ch) {
			ch.traversalTag = checkRootTagpath(ch);
			subn(ch);
		});
	})(node);
}

function untagSubgraph(node) {
	node.eachSubgraph(function(sn) {
		sn.traversalTag = false;
	});
}

 /*function to filter graph by a bitscore inputted by the user*/
function filter(bitscore) {
	if (!(bitscore > 0)) { /*bitscores must make sence*/
		$('#filtererror').html("Not a valid bitscore.");
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
		//	if (!ch.traversalTag) {
				ch.ignore = true;
				ch.setData('alpha', 0, opt.type == 'animate'? 'end' : 'current');
				subn(ch);
		//	}
		});
	})(node);
	if(opt.type == 'animate') {
		viz.compute('end');
		if(viz.rotated) {
			viz.rotate(viz.rotated, 'none', { 'property':'end' });
		}
		(function subn(n) {
			n.eachSubnode(function(ch) {
		//		if (!ch.traversalTag) {
					ch.setPos(node.getPos('end'), 'end');
					subn(ch);
		//		}
			});
		})(node);
		viz.fx.animate(opt);
	}
	else if(opt.type == 'replot') {
		viz.refresh();
	}
}
