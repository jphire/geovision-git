/* config.js - Initializes all globals and the config dict. Sets default
 * values for settings. Detailed explanation of all the configurations available
 * e.g. for animations can be found at the JIT documents page
 * http://thejit.org/static/v20/Docs/.
 */

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
settings.animationsettings.onComplete = function() { setBusy(false); };
settings.animationsettings.onMerge = colorEdges;

//set initial number of concentric circles
var max_level = 6;

var Config = 
{
		//Where to append the visualization
		injectInto: 'infovis',
		
		//set canvas size
		width: settings.settings.canvaswidth,
		height:settings.settings.canvasheight,
		//Optional: create a background canvas that plots
		//concentric circles.
		background: { numberOfCircles: max_level, CanvasStyles: { strokeStyle: '#555' } },
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
			angularWidth: 20,
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
			dim: 10,
		}
};
jQuery(function($) {
	/*setting stuff in css to the preferred size*/
	$('#infovis').css('height', parseInt(settings.settings.canvasheight));
	$('#infovis').css('width', parseInt(settings.settings.canvaswidth));
	$('#center-container').css('width', parseInt(settings.settings.canvaswidth));
	$('#center-container').css('height', parseInt(settings.settings.canvasheight));
	$('#right-container').css('height', parseInt(settings.settings.canvasheight));
	$('#container').css('width', parseInt(settings.settings.canvaswidth)+400);
	$('#container').css('height', parseInt(settings.settings.canvasheight));
	$('#deleteUntagged').click(function(e) { e.preventDefault(); saveUndoState(); rgraph.op.deleteUntagged(); });
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
