/**
 * This file includes qunit tests for all javascript code not in external libraries.
 */

$(document).ready(function(){

		module("moreinfo.js");
		asyncTest("Alignment test", function()
		{
			expect(1);
			initGraph();
			setTimeout(function(){
				alignmentfunction(26092180, 'A1A835', 'GDQ9FB102FUTYO');
				ok($('span.alignmentpart')[0].innerHTML != '', "Alignmentfunction has data: " + ($('span.alignmentpart')[0].innerHTML!=''));
				ok(closealign.innerHTML=="Close", "Alignmentfunction has close button:" + (closealign.innerHTML=="Close"));
				start();
			}, 1000);

			setTimeout(function(){
				closealignment(closealign);
				raises(closealignment(closealign), "must raise error to pass");
				start();
			}, 1000);
			
			start();
		});

		module("graphviz.js");
		 /* Asynchronous testing required when using ajax!*/
		asyncTest("Graph creation and initial query result test", function()
		{
			expect(8);
			initGraph();
//			$.getJSON('/graphjson', query, function(json) {
//					rgraph.loadJSON(prepareJSON(json), query.root || 0);
//			});
			setTimeout(function(){
				ok(rgraph.busy==false, "rgraph.busy: " + rgraph.busy);
				ok(rgraph.config.levelDistance==Config.levelDistance, "rgraph.levelDistance: " + rgraph.config.levelDistance);
				ok(rgraph.config.Node.alpha==Config.Node.alpha, "rgraph.config.Node.alpha: " + rgraph.config.Node.alpha);
				ok(rgraph.config.Edge.dim==Config.Edge.dim, "rgraph.config.Edge.dim: " + rgraph.config.Edge.dim);
				ok(rgraph.json.length == 5, "rgraph.json.length was: " + rgraph.json.length);
				ok(rgraph.root=="R1", "rgraph.root was: " + rgraph.root);
				start();
			}, 1000);

			setTimeout(function(){
				setBusy(true);
				ok(busy==true, "setBusy works: " + (busy==true));
				setBusy(false);
				start();
			}, 1000);

			setTimeout(function(){
				cleanupGraph();
				var works = true;
				rgraph.graph.eachNode(function(n) {
					if(n.data.$alpha<0.01)
						works = false;
				});
				ok(works, "cleanupGraph works: " + works);
				start();
			}, 1000);
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
				Config.Events.onMouseLeave(node);
				ok(rgraph.canvas.getElement().style.cursor=='', 'cursorStyle was empty: ' + (rgraph.canvas.getElement().style.cursor==''));
				ok(currentNode==undefined, 'currentNode was undefined: ' + (currentNode==undefined));
				start();
			}, 1000);

			
			setTimeout(function(){
				var node = rgraph.graph.getNode(rgraph.root);
				Config.Events.onClick(node);		
				ok(('DB5' in rgraph.graph.nodes), 'DB5 was in the graph: ' + ('DB5' in rgraph.graph.nodes));
				start();
			}, 1000);
		});
	});