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
  
    
    
    var json = {
id: "1.1.2.22",
name: "1.1.2.22",
children: [	{
	id: "DB1",
	name: "DB1",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: [	{
	id: "R001",
	name: "R001",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: []
	},
	{
	id: "R002",
	name: "R002",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: []
	},
]},
	{
	id: "DB1",
	name: "DB1",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: [	{
	id: "R001",
	name: "R001",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: []
	},
	{
	id: "R002",
	name: "R002",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: []
	},
]},
	{
	id: "DB2",
	name: "DB2",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: [	{
	id: "R003",
	name: "R003",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: []
	},
]},
	{
	id: "DB4",
	name: "DB4",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: [	{
	id: "R005",
	name: "R005",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: []
	},
]},
	{
	id: "DB6",
	name: "DB6",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: [	{
	id: "R004",
	name: "R004",
	data: {
		relation: "<h4>relations here..</h4>"
	},
	children: []
	},
]},
]
};
    //end
   
    //init RGraph
    var rgraph = new $jit.RGraph({
        //Where to append the visualization
        injectInto: 'infovis',
        //Optional: create a background canvas that plots
        //concentric circles.
        background: {
          CanvasStyles: {
            strokeStyle: '#555'
          }
        },
        //set distance for nodes on different levels
	levelDistance: 100,
	
        //Add navigation capabilities:
        //zooming by scrolling and panning.
        Navigation: {
          enable: true,
          panning: true,
          zooming: 10
        },
        
        //Set Node and Edge styles.
        Node: {
            span: 100,
            angularWidth:100,
            color: '#ffeeff'
        },
        
        Edge: {
          color: '#Cdffff',
          lineWidth:1.0,
          dim: 50
        },

        onBeforeCompute: function(node){
            Log.write("centering " + node.name + "...");
            //Add the relation list in the right column.
            //This list is taken from the data property of each JSON node.
            $jit.id('inner-details').innerHTML = node.data.relation;
        },
        
        onAfterCompute: function(){
            Log.write("done");
        },
        //Add the name of the node in the correponding label
        //and a click handler to move the graph.
        //This method is called once, on label creation.
        onCreateLabel: function(domElement, node){
            domElement.innerHTML = node.name;
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

            if (node._depth <= 1) {
                style.fontSize = "0.8em";
                style.color = "#ccc";
            
            } else if(node._depth == 2){
                style.fontSize = "0.7em";
                style.color = "#494949";
            
            } else {
                style.display = 'none';
            }

            var left = parseInt(style.left);
            var w = domElement.offsetWidth;
            style.left = (left - w / 2) + 'px';
        }
    });

    //load JSON data
    rgraph.loadJSON(json);
    //trigger small animation
    rgraph.graph.eachNode(function(n) {
      var pos = n.getPos();
      pos.setc(-200, -200);
    });
    rgraph.compute('end');
    rgraph.fx.animate({
      modes:['polar'],
      duration: 2000
    });
    
  
    //end
    //append information about the root relations in the right column
    $jit.id('inner-details').innerHTML = rgraph.graph.getNode(rgraph.root).data.relation;
}
