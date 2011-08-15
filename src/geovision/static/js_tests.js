/* 
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */


$(document).ready(function(){
		module("Basic Unit Test");
		test("Sample test", function()
		{
			expect(2);
			equals((4/2), 2, 'Expected 2 as the result, result was: ' + (4/2));
			equals(divide(4,2), 2, 'Expected 2 as the result, result was: ' + divide(4,2));
		});

		module("moreinfo.js");
		test("Alignment test", function()
		{
			expect(1);
			var alignment;
			equals(2, 2, 'Expected 2 as the result, result was: ' + divide(4,2));
		});

		module("graphviz.js");
		test("Graph creation test", function()
		{
			expect(4);
			var rgraph = new RGraph(Config);
			var json;
			ok(rgraph.busy==false, "rgraph.busy: " + rgraph.busy);
			ok(rgraph.config.levelDistance==Config.levelDistance, "rgraph.levelDistance: " + rgraph.levelDistance);
			ok(rgraph.config.Node.alpha==Config.Node.alpha, "rgraph.config.Node.alpha: " + rgraph.config.Node.alpha);
			ok(rgraph.config.Edge.dim==Config.Edge.dim, "rgraph.config.Edge.dim: " + rgraph.config.Edge.dim);
			$.getJSON('/graphjson', query, function(json) {
				rgraph.loadJSON(prepareJSON(json), query.root || 0);
			});
			
		});

		module("events.js");
		test("Events test", function()
		{
			expect(2);
			initGraph();
			var node = rgraph.graph.getNode(rgraph.root);
			Config.Events.onMouseEnter(node);
			var cursorStyle = rgraph.canvas.getElement().style.cursor;
			equals(cursorStyle, 'pointer', 'Expected pointer as the result, result was: ' + cursorStyle);
			Config.Events.onMouseLeave(node);
			cursorStyle = rgraph.canvas.getElement().style.cursor;
			equals(cursorStyle, '', 'Expected pointer as the result, result was: ' + cursorStyle);
		});
	});