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


function init(){
    //init data
    jQuery('#loader').fadeOut();//loader fadeaway
}

function initGraph(json)
{
        var rgraph = new $jit.RGraph({
        //Where to append the visualization
        injectInto: 'infovis',
        //set canvas size
        width: 600,
        height: 600,

        //Optional: create a background canvas that plots
        //concentric circles.
        background: {
          CanvasStyles: {
            strokeStyle: '#555'
          }
        },

        //set distance for nodes on different levels
		levelDistance: 100,

        //set transformation speed
        duration: 500,
        fps: 40,

        //set transformation style
        transition: $jit.Trans.Circ,
        //Add navigation capabilities:
        //zooming by scrolling and panning.
        Navigation: {
          enable: true,
          panning: true,
          zooming: 25
        },
        
        //Set Node and Edge styles.
        Node: {
            overridable: true,
            color: '#ff0000',
            alpha: 1,
            dim: 5,
            height: 20,
            width: 90,
            autoHeight: false,
            autoWidth: false,
            lineWidth: 0.5,
            transform: true,
            align: "center",
            angularWidth: 1,
            span:1,
            type: 'circle',
            CanvasStyles: {}
        },
        
        Edge: {
          overridable: true,
          color: '#068481',
		  alpha: 1,
          lineWidth:1.0,
          dim: 10,
		  type: 'line',
		  epsilon: 7
        },

		Events : {
			enableForEdges: true,
			enable : true,
			type : 'Native', //edge event doesn't work with 'HTML'..
			onRightClick : function(node, eventInfo, e) {
				//if no node is returned then exit
				if (!node) return;
				if (node.nodeFrom) {
					// living on the edge..
					console.log(node.data.id);
					alignment(node.data.id);
					//testcode:
					//alert('Clicked on the edge ' + node.nodeFrom.name')

				} else {
					// TODO: dynamic graph refresh here..
					//rgraph.onClick(node.id);
				}
			},
			onMouseEnter: function(node, eventInfo, e) { 
				//console.log("mouse entered" + node)
				if (node.nodeFrom) {
					rgraph.canvas.getElement().style.cursor = 'pointer';
					node.data.$color = "#FDCC97"
					//rgraph.refresh()
					//alert('Hey, click on the edge:' + node.nodeFrom.name);// it's an edge
				}
			},
			onMouseLeave: function(object, eventInfo, e) {
				if(object) {
					if(object.nodeTo) {
						object.data.$color = object.data.color
					} else{
						object.data.$color = 'FF0000'
					}
				}
				rgraph.canvas.getElement().style.cursor = ''
				//rgraph.refresh()
			}
		},

		//Label styling is done via CSS!
		Label: {
			$extend: true,
			type: 'HTML',
			overridable: true
		},

        //Set tooltip configuration
        Tips: {
            enable: true,
			type: 'Native',
            width: 30,
            align: 'left',
			
            onShow: function(tip, node) {
				tip.innerHTML = "";
				if (!node) return;

				if(node.nodeFrom){
					//it's an edge
					tip.innerHTML += "<b>" + node.nodeFrom.name + " - " + node.nodeTo.name + "</b></br>";
					tip.innerHTML += "<b>" + node.data.bitscore + "</b></br>";
				}
				else {
					//it's a label
					tip.innerHTML += "<b>" + node.id + "</b></br>";
					tip.innerHTML += node.data.description + "</br>";
				}
            }
        },
        
        onBeforeCompute: function(node){
		numSubnodes = $jit.Graph.Util.getSubnodes(node).length;
		Log.write(node.name + ": " + node.data.type + ", subnodes: " + numSubnodes);
		if (numSubnodes == 1)
		{
			$.getJSON(json_base_url + '&' + node.data.type + '=' + node.name,
				function(newdata) {
					rgraph.op.sum(newdata, { type: 'replot'});
					rgraph.refresh();
				 }
			);

		}


            //Add the relation list in the right column.
            //This list is taken from the data property of each JSON node.
			$jit.id('inner-details').innerHTML = ""
            $jit.id('inner-details').innerHTML += "<b>" + node.id + "</b></br>"
			$jit.id('inner-details').innerHTML += node.data.description + "</br>"
			if(node.data.db_seq){
				//link moved from here to rightclick
			}

        },
        
        onAfterCompute: function(){
            Log.write("done");
        },
        //Add the name of the node in the correponding label
        //and a click handler to move the graph.
        //This method is called once, on label creation.
        onCreateLabel: function(domElement, node){
            domElement.innerHTML = node.name.substr(0,10);
            domElement.onclick = function(){
                rgraph.onClick(node.id);
            };
        },
        //Change some label dom properties.
        //This method is called each time a label is plotted.
        onPlaceLabel: function(domElement, node){
            var style = domElement.style;
            style.display = '';
            style.cursor = 'pointer';

            if (node._depth <= 2) {
                style.fontSize = "1.1em";
                style.color = "#ccc";
            
            } else if(node._depth == 3){
                style.fontSize = "1.1em";
                style.color = "#494949";
            
            } else {
                style.display = 'none';
            }

            var left = parseInt(style.left);
            var w = domElement.offsetWidth;
            style.left = (left - w / 2) + 'px';
        }
    });

    //load JSON data, second argument is the index of the centered node
    rgraph.loadJSON(json, 0);
    
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
    $jit.id('inner-details').innerHTML += "<b>" + rgraph.graph.getNode(rgraph.root).id + "</b></br>";
    $jit.id('inner-details').innerHTML += rgraph.graph.getNode(rgraph.root).data.description;

}
