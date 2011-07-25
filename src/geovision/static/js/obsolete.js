/* old stuff that doesn't seem to be used */

		onBeforeCompute: function(node)
		{
			//This method is called only when centering a node
			//Add the relation list in the right column.
			//This list is taken from the data property of each JSON node.
			$jit.id('inner-details').innerHTML = ""
			$jit.id('inner-details').innerHTML += "<b>" + node.id + "</b><br/>"
			if(node.data.bitscore){
				$jit.id('inner-details').innerHTML += node.data.description + "<br/>"
			}
		},
	//append information about the root relations in the right column
	$jit.id('inner-details').innerHTML += "<b>" + rgraph.graph.getNode(rgraph.root).id + "</b><br/>";
	$jit.id('inner-details').innerHTML += rgraph.graph.getNode(rgraph.root).data.description;
