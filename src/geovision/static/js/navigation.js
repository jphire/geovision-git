/*
 * Modified version of the original contract function for removing unnecessary
 * nodes while traversing the graph.
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

function deleteUntagged() {
	var nodesArray = [];
	rgraph.graph.eachBFS(rgraph.root, function(n) { nodesArray.push(n) });
	while (nodesArray.length > 0) {
		var node = nodesArray.pop();
		if (!node.traversalTag) {
			rgraph.op.removeNode(node.id, rgraph.op.userOptions);
		}
	}
}

function addTemporaryTags()
{
	rgraph.graph.eachNode(function(n) {
		if(n.traversalTag === true)
			tagParents(n, 'temp');
	});
}
/*
 * Function for checking if node has a tagged path to the root node.
 */
function checkRootTagpath(node) {
	var parentNodes = node.getParents();
	if (!node.traversalTag) return false;
	if (parentNodes.length == 0) return true;
	for (var i = 0; i < parentNodes.length; i++) {
		pnode = parentNodes[i]
		if (!pnode.traversalTag) continue;
		if (checkRootTagpath(pnode)) return true;
	}
	return false;
}

function tagNode(node, value) {
	if (!checkRootTagpath(node)) tagParents(node);
	node.traversalTag = value ? value : true;
	rgraph.refresh()
}

/* 
 * Function for tagging a path from node to root, always tags first node in parents list
 */
function tagParents(node, value) {
	var parents = node.getParents();
	while (parents.length > 0) {
		parents[0].traversalTag = value ? value : true;
		console.log("Parent " + parents[0].id + " tagged");
		parents = parents[0].getParents();
	}
	node.traversalTag = true;
	rgraph.refresh()
}

function tagSubnodes(node) {
	if (!checkRootTagpath(node)) tagParents(node);
	node.eachSubnode(function(child) {
		child.traversalTag = true;
		console.log("Child " + child.id + " tagged");
	});
	node.traversalTag = true;
	rgraph.refresh()
}

function tagSubgraph(node) {
	if (!checkRootTagpath(node)) tagParents(node);
	node.eachSubgraph(function(child) {
		child.traversalTag = true;
		console.log("Child " + child.id + " tagged");
	});
	node.traversalTag = true;
	rgraph.refresh()
}

/*
 * Untags a node and all nodes in it's subgraph without tagged path to root.
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

function untagSubgraph(node) {
	node.eachSubgraph(function(sn) {
		sn.traversalTag = false;
	});
	rgraph.refresh()
}

function centerToNode(id, opt){
}
