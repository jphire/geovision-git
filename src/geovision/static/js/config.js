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
var defaultsettings = {
		animationsettings:
			{duration: 1000,
			transition: 'linear',
			subtype: 'EaseIn',
			type:"fade:con"},
		settings:
			{canvaswidth: 600,
			canvasheight: 600}
};
settings = $jit.util.merge(defaultsettings, settings);
var numericFields = {settings: ['canvaswidth', 'canvasheight'], animationsettings: ['duration']}

for (var key1 in numericFields)
{
	for (var i in numericFields[key1])
	{
		var key2 = numericFields[key1][i];
		var num = parseInt(settings[key1][key2]);
		settings[key1][key2] = isNaN(num) ? defaultsettings[key1][key2] : num;
	}
}
settings.animationsettings.transitionname = settings.animationsettings.transition;
var type = $jit.Trans[settings.animationsettings.transition];
if(!type)
	type = $jit.Trans[defaultsettings.animationsettings.transition]; 
var subtype = type[settings.animationsettings.subtype];
if(subtype)
	type = subtype;
settings.animationsettings.transition = type;
var Config = 
{
		//Where to append the visualization
		injectInto: 'infovis',
		//set canvas size
		width: settings.settings.canvaswidth,
		height:settings.settings.canvasheight,
		//Optional: create a background canvas that plots
		//concentric circles.
		background: { CanvasStyles: { strokeStyle: '#555' } },
		//set distance for nodes on different levels
		levelDistance: 100,
		//set transformation speed
		duration: settings.animationsettings.duration,
		fps: 40,
		//set transformation style
		transition: settings.animationsettings.transition,
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
jQuery(function($) {
	/*setting stuff in css to the prefered size*/
	$('#infovis').css('height', parseInt(settings.settings.canvasheight));
	$('#infovis').css('width', parseInt(settings.settings.canvaswidth));
	$('#center-container').css('width', parseInt(settings.settings.canvaswidth));
	$('#center-container').css('height', parseInt(settings.settings.canvasheight));
	$('#right-container').css('height', parseInt(settings.settings.canvasheight));
	$('#container').css('width', parseInt(settings.settings.canvaswidth)+400);
	$('#container').css('height', parseInt(settings.settings.canvasheight));
	$('#deleteUntagged').click(function(e) { e.preventDefault(); rgraph.op.deleteUntagged(); });
	$('#canvas_x').val(settings.settings.canvaswidth);
	$('#canvas_y').val(settings.settings.canvasheight);
	if (settings.animationsettings.type == 'replot'){
		$('#animations_off').attr('checked', 'checked');
	}
	$('#duration').val(settings.animationsettings.duration);
	if (settings.animationsettings.transitionname != undefined){
		$('#animationtype').val(settings.animationsettings.transitionname);
	}
	$('#animationsubtype').val(settings.animationsettings.subtype);
});

