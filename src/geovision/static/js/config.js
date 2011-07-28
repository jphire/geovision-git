/* config.js - Initialize all globals and the config dict */

// Copied from JIT example code. Probably not necessary
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

var rgraph;
var RGraph = $jit.RGraph;
var busy = false;
var settings = {
			canvaswidth: "{{ settings.settings.canvaswidth }}",
			canvasheight: "{{ settings.settings.canvasheight }}"
};

//function getUrlVars()
//{
//    var vars = [], hash;
//    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
//
//    for(var i = 0; i < hashes.length; i++)
//    {
//        hash = hashes[i].split('=');
//        vars.push(hash[0]);
//        vars[hash[0]] = hash[1];
//    }
//
//    return vars;
//}
//
//var hash = getUrlVars();

var Config = 
{
		//Where to append the visualization
		injectInto: 'infovis',
		//set canvas size

		width: settings.canvaswidth,
		height: settings.canvasheight,
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
//			lineWidth: 0.5,
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
		//	lineWidth_hover: 5.0,
			dim: 10,
		//	dim_hover: 15
		}
};
