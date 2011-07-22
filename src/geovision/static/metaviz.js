var fd;

function init(json)
{
	for(i in json)
	{
		json[i].name = json[i].data.name;
	}
	fd = new $jit.ForceDirected({
		//id of the visualization container	
		injectInto: "infovis",
		width: 600,
		height: 600,
		//Enable zooming and panning	
		//by scrolling and DnD	
		Navigation: {	
			enable: true,	
			//Enable panning events only if we're dragging the empty	
			//canvas (and not a node).	
			panning: 'avoid nodes',	
			zooming: 10 //zoom speed. higher is more sensible	
		},	
		// Change node and edge styles such as	
		// color and width.	
		// These properties are also set per node	
		// with dollar prefixed data-properties in the	
		// JSON structure.	
		Node: {	
			overridable: true	
		},	
		Edge: {	
			overridable: true,	
			color: '#23A4FF',	
			lineWidth: 0.4	
		},	
		//Native canvas text styling	
		Label: {	
			type: 'HTML',
			size: 16,	
			style: 'bold'	
		},	
		//Add Tips	
		Tips: {	
			enable: false,	
			onShow: function(tip, node) {	
			}	
		},	
		// Add node events	
		Events: {	
			enable: true,	
			type: 'Native',	
			onMouseEnter: function() {	
			},	
			onMouseLeave: function() {	
			},	
			onClick: function(node) {	
			}	
		},	
	
		//Number of iterations for the FD algorithm	
		iterations: 200,	
		//Edge length	
		levelDistance: 130,	
	
		onCreateLabel: function(domElement, node){	
			domElement.innerHTML = node.name;	
			var style = domElement.style;	
			style.fontSize = "0.8em";	
			style.color = "#ff0000";	
		},	
	
		onPlaceLabel: function(domElement, node){	
			var style = domElement.style;	
			var left = parseInt(style.left);	
			var top = parseInt(style.top);	
			var w = domElement.offsetWidth;	
			style.left = (left - w / 2) + 'px';	
			style.top = (top + 10) + 'px';	
			style.display = '';	
		}	
	});	

	fd.loadJSON(json);	
	// compute positions incrementally and animate.	
	fd.computeIncremental({	
		iter: 40,	
		property: 'end',	
		onComplete: function(){	
			fd.animate({	
				modes: ['linear'],	
				transition: $jit.Trans.Elastic.easeOut,	
				duration: 2500	
			});	
		}	
	});	
}
