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

/*
 * Function for checking if node has a tagged path to the root node.
 */
function checkRootTagpath(node) {
	var parentNodes = node.getParents();
	if (!node.traversalTag) return false;
	if (parentNodes.length == 0) return true;
	for (var i = 0; i < parentNodes.length; i++) {
		pnode = parentNodes[i]
		if (pnode.traversalTag != true) continue;
		if (checkRootTagpath(pnode)) return true;
	}
	return false;
}

function tagNode(node) {
	if (!checkRootTagpath(node)) tagParents(node);
	node.traversalTag = true;
	rgraph.refresh()
}

/* 
 * Function for tagging a path from node to root, always tags first node in parents list
 */
function tagParents(node) {
	var parents = node.getParents();
	while (parents.length > 0) {
		parents[0].traversalTag = true;
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
    if (this.root != id && !this.busy) {
      this.busy = true;
      this.root = id;
      var that = this;
      var obj = that.getNodeAndParentAngle(id);

      // second constraint
      this.tagChildren(obj.parent, id);
      this.parent = obj.parent;
      this.compute('end');

      // first constraint
      var thetaDiff = obj.theta - obj.parent.endPos.theta;
      this.graph.eachNode(function(elem){
        elem.endPos.set(elem.endPos.getp().add($P(thetaDiff, 0)));
      });

      var mode = this.config.interpolation;
      opt = $.merge( {
        onComplete: $.empty
      }, opt || {});

      this.fx.animate($.merge( {
        hideLabels: true,
        modes: [
          mode
        ]
      }, opt, {
        onComplete: function(){
          that.busy = false;
          opt.onComplete();
        }
      }));
    }
  }
