/**
 * This file includes qunit tests for all javascript code not in external libraries.
 */

$(document).ready(function(){

		module("moreinfo.js");
		asyncTest("Alignment test", function()
		{
			expect(3);
			initGraph();
			alignmentfunction(26092180, 'A1A835', 'GDQ9FB102FUTYO');
			setTimeout(function(){
				ok($(alignment)[0].innerText.search(/Alignment for edge/i)!=-1, "Alignment for edge has data: " + ($(alignment)[0].innerText.search(/Alignment for edge/i)!=-1));
				ok($('span.alignmentpart')[0].innerHTML != '', "Alignmentfunction has data: " + ($('span.alignmentpart')[0].innerHTML!=''));
				ok(closealign[1].innerHTML=="Close", "Alignmentfunction has a close button:" + (closealign[1].innerHTML=="Close"));
				start();
			}, 2000);

		});

		module("graphviz.js");
		 /* Asynchronous testing required when using ajax!*/
		asyncTest("Graph creation and initial query result test", function()
		{
			expect(9);
			initGraph();
			setTimeout(function(){
				ok(rgraph.busy==false, "rgraph.busy: " + rgraph.busy);
				ok(rgraph.config.levelDistance==Config.levelDistance, "rgraph.levelDistance: " + rgraph.config.levelDistance);
				ok(rgraph.config.Node.alpha==Config.Node.alpha, "rgraph.config.Node.alpha: " + rgraph.config.Node.alpha);
				ok(rgraph.config.Edge.dim==Config.Edge.dim, "rgraph.config.Edge.dim: " + rgraph.config.Edge.dim);
				ok(rgraph.json.length == 2, "rgraph.json.length was: " + rgraph.json.length);
				ok(rgraph.root=="Q57DS4", "rgraph.root was: " + rgraph.root);
				start();
			}, 3000);

			setTimeout(function(){
				setBusy(true);
				ok(busy==true, "setBusy works: " + (busy==true));
				setBusy(false);
				start();
			}, 3000);

			setTimeout(function(){
				cleanupGraph();
				var works = true;
				rgraph.graph.eachNode(function(n) {
					if(n.data.$alpha<0.01)
						works = false;
				});
				ok(works, "cleanupGraph works: " + works);
				start();
			}, 3000);

			setTimeout(function(){
				var node = rgraph.graph.getNode('gi|185679843|gb|ABLU01135391.1|');
				fetchJSON(node);
				ok(('A8LMA2' in rgraph.graph.nodes), "fetchJSON works: " + ('A8LMA2' in rgraph.graph.nodes));
				start();
			}, 3000);

		});

		module("events.js");
		asyncTest("Events test", function()
		{
			expect(5);
			initGraph();

			setTimeout(function(){
				var node = rgraph.graph.getNode(rgraph.root);
				rgraph.events.config.onMouseEnter(node);
				ok((rgraph.canvas.getElement().style.cursor=='pointer'), 'cursorStyle was pointer: ' + (rgraph.canvas.getElement().style.cursor=='pointer'));
				ok(currentNode!=undefined, 'currentNode was not undefined: ' + (currentNode!=undefined));
				start();
			}, 1000);
			
			setTimeout(function(){
				node = rgraph.graph.getNode(rgraph.root);
				rgraph.events.config.onMouseLeave(node);
				ok(rgraph.canvas.getElement().style.cursor=='', 'cursorStyle was empty: ' + (rgraph.canvas.getElement().style.cursor==''));
				ok(currentNode==undefined, 'currentNode was undefined: ' + (currentNode==undefined));
				start();
			}, 1000);
			
			setTimeout(function(){
				var node = rgraph.graph.getNode(rgraph.root);
				rgraph.events.config.onClick(node);
				ok(('gi|185679843|gb|ABLU01135391.1|' in rgraph.graph.nodes), '\'gi|185679843|gb|ABLU01135391.1|\' was in the graph: ' + ('DB5' in rgraph.graph.nodes));
				start();
			}, 1000);
		});

		module("bitscore.js");
		asyncTest("Graph coloring and filtering test", function()
		{
			expect(2);
			initGraph();

			colorEdges();
			var works = true;
			rgraph.graph.eachNode(function(node) {
				node.eachAdjacency(function(adj) {
					if(adj.data.type=='enzyme'){
						if(!node.data.color) works = false;
					}
				});
			});
			
			setTimeout(function(){
				ok(works, "colorEdges works: " + works);
				start();
			}, 1000);

			setTimeout(function(){
				ok(filter(-1)==false, "Filter(-1) returned false: " + (filter(-1)==false));
				start();
			}, 1000);
		});

		module("navigation.js");
		asyncTest("Graph traversal and tagging test", function()
		{
			expect(5);
			initGraph();
			var node = rgraph.graph.getNode('Q57DS4')
			setTimeout(function(){
				tagNode(node);
				ok(node.traversalTag==true, "tagNode works: " + (node.traversalTag==true));
				ok(checkRootTagpath(node)==true, "checkRootTagpath test 1: " + (checkRootTagpath(node)==true));
				ok(checkRootTagpath(rgraph.graph.getNode('gi|185679843|gb|ABLU01135391.1|'))==false, "checkRootTagpath test 2: " + (checkRootTagpath(rgraph.graph.getNode('gi|185679843|gb|ABLU01135391.1|'))==false));
				start();
			}, 2000);

			setTimeout(function(){
				untagNode(node);
				ok(node.traversalTag==false, "untagNode works: " + (node.traversalTag==false));
				start();
			}, 2000);

			setTimeout(function(){
				var node = rgraph.graph.getNode('gi|185679843|gb|ABLU01135391.1|')
				tagParents(node);
				ok(checkRootTagpath(node)==true, "tagParents: " + (checkRootTagpath(rgraph.graph.getNode('gi|185679843|gb|ABLU01135391.1|'))==true));
				start();
			}, 2000);
		});
	});