/**
 * Modified version of the original contract function for removing unnecessary
 * nodes while traversing the graph.
 * TODO: NOT USED
 */
function contractForTraversal(node, opt) {
	console.log("contractForTraversal");
	var viz = this.viz;
	if(node.collapsed || !node.anySubnode($jit.util.lambda(true))) return;
	opt = $jit.util.merge(this.options, viz.config, opt || {}, {
		'modes': ['node-property:alpha:span', 'linear']
	});
	node.collapsed = true;
	(function subn(n) {
		n.eachSubnode(function(ch) {
			if (!ch.traversalTag) {
				ch.ignore = true;
				ch.setData('alpha', 0, opt.type == 'animate'? 'end' : 'current');
				subn(ch);
			}   
		});
	})(node);
	if(opt.type == 'animate') {
		viz.compute('end');
		(function subn(n) {
			n.eachSubnode(function(ch) {
				if (!ch.traversalTag) {
					ch.setPos(node.getPos('end'), 'end');
					subn(ch);
				}
			});
		})(node);
		viz.fx.animate(opt);
	} 
	else if(opt.type == 'replot') {
		viz.refresh();
	}
}

function deleteByBitscore(bitscoreLimit) {

}

/** Function for deleting nodes from the graph.
 * If bitscoreLimit is not defined, all untagged nodes except root will be deleted.
 * If bitscoreLimit is defined, all untagged nodes (except root) without connections 
 * over that bitscore will be deleted. It will also preserve a path to root from each
 * remaining node (since many operations would break if graph became disconnected).
 *
 * Function will also clean all edges to (and from) the deleted nodes from the graph, 
 * and update data.bitscore field for remaining nodes.
 *
 * Will also untag all nodes once finished.
 */
function deleteUntagged(bitscoreLimit) {
	var nodesArray = [];
	rgraph.graph.eachBFS(rgraph.root, function(n) { nodesArray.push(n) });
	// Add nodes to end of array and pop from there to get reverse-BFS order
	while (nodesArray.length > 1) {
		var node = nodesArray.pop();
		if (!node.traversalTag && (!bitscoreLimit || node.data.bitscore < bitscoreLimit)) {
			rgraph.op.removeNode(
				node.id, 
				$jit.util.merge(rgraph.op.userOptions, {
					onComplete: function() { cleanupGraph(); colorEdges(); updateBitscores();},
					onAfterPlotNode: function(n) { n.traversalTag = false; }
			}));
		}
		else {
			tagParents(node);
		}
	}
}

/** Function for updating data.bitscore field for all nodes in the graph.
 * Should be used after deleting edges from the graph if relevant values are not otherwise updated.
 */
function updateBitscores() {
	rgraph.graph.eachNode(function(node) {
		var bitscore = 0;
		node.eachAdjacency(function(edge) {
			console.log(edge);
			if (edge.data.bitscore > bitscore) {
				bitscore = edge.data.bitscore;
			}
		});
		node.data.bitscore = bitscore;
	});
}

/** TODO: UNUSED? */
function addTemporaryTags()
{
	rgraph.graph.eachNode(function(n) {
		if(n.traversalTag === true)
			tagParents(n, 'temp');
	});
}

/** Function for checking if node has a tagged path to the root node.
 * Assumes the node has a path to root.
 */
function checkRootTagpath(node) {
	var parentNodes = node.getParents();
	if (parentNodes.length == 0) {
		if (node.id === rgraph.root) return true;
		else return false;
	}
	for (var i = 0; i < parentNodes.length; i++) {
		pnode = parentNodes[i]
		if (!pnode.traversalTag) continue;
		if (checkRootTagpath(pnode)) return true;
	}
	return false;
}

/** Function for tagging a node. If node has no tagged path to root, a path will also be tagged
 * since otherwise deletion could result in disconnected graph.
 */
function tagNode(node, value) {
	if (!checkRootTagpath(node)) tagParents(node);
	node.traversalTag = value ? value : true;
	rgraph.refresh()
}

/** Function for tagging a path from node to root.
 * Builds path by tagging the parent with the best (bitscore) connection to current node.
 * Responsibility for updating the visualization is left to user, this function does
 * not call refresh() or any animating function.
 */
function tagParents(node, value) {
	var currentNode = node;
	var parents = node.getParents();
	while (parents.length > 0) {
		var bestParent = parents[0];
		var bestBitscore = currentNode.getAdjacency(parents[0].id).data.bitscore;
		for (var i = 1; i < parents.length; i++) {
			var tempBitscore = currentNode.getAdjacency(parents[i].id).data.bitscore;
			if (tempBitscore > bestBitscore) {
				bestParent = parents[i];
				bestBitscore = tempBitscore;
			}
		}
		bestParent.traversalTag = value ? value : true;
		currentNode = bestParent;
		parents = currentNode.getParents();
	}
	node.traversalTag = true;
}

/** Tags the subnodes of the node*/
function tagSubnodes(node) {
	if (!checkRootTagpath(node)) tagParents(node);
	node.eachSubnode(function(child) {
		child.traversalTag = true;
		console.log("Child " + child.id + " tagged");
	});
	node.traversalTag = true;
	rgraph.refresh()
}

/** Tags the subgraph of the node*/
function tagSubgraph(node) {
	if (!checkRootTagpath(node)) tagParents(node);
	node.eachSubgraph(function(child) {
		child.traversalTag = true;
		console.log("Child " + child.id + " tagged");
	});
	node.traversalTag = true;
	rgraph.refresh()
}

/** Untags a node.
 * Since many operations rely on all nodes having a path to root, also untags all
 * tagged nodes without a tagged path to root after untagging this node.
 */
function untagNode(node) {
	node.traversalTag = false;
	(function subn(n) {
		n.eachSubnode(function(ch) {
			ch.traversalTag = checkRootTagpath(ch);
			subn(ch);
		});
	})(node);
	rgraph.refresh()
}

/** Untags a subgraph */
function untagSubgraph(node) {
	node.eachSubgraph(function(sn) {
		sn.traversalTag = false;
	});
	rgraph.refresh()
}

