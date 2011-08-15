var currentNode;
var currentEdge;
var ctxMenuOpen;

/** Called when the context menu is being hidden */
function hideCtxMenu()
{
	if(!ctxMenuOpen) return;
	ctxMenuOpen = false;
	if(currentNode) rgraph.config.Events.onMouseLeave(currentNode)
	if(currentEdge) rgraph.config.Events.onMouseLeave(currentEdge);
	busy = false;
	currentEdge = currentNode = false;
	rgraph.config.Navigation.panning = true;
	rgraph.config.Tips.enable = true;
	rgraph.events.pressed = false;
}
/** Adds the context menu to the canvas and binds all the necessary events.
* The event bindings are done in the jquery-contextmenu plugin code */
function initContextMenu()
{
	$('#infovis').contextMenu('nodeMenu', {
		'shadow': false,
		'bindings': {
			/* The actual menu events. All the menu entries are defined in templates/graphviz.html */
			'close': function() { },
			'n_center': function() {
				console.log(currentNode.id);
				var id = currentNode.id;
				setBusy('Centering');
				tagNode(rgraph.graph.getNode(id));
				rgraph.onClick(id, rgraph.op.userOptions);
			},
			'e_align': function() { alignmentfunction(currentEdge.data.blast_id, currentEdge.nodeFrom.id, currentEdge.nodeTo.id); },
			'n_tag': function() { 
				if (currentNode.traversalTag != true) {
					tagNode(currentNode);
				}
				else {
					untagNode(currentNode);
				}
			},
			'n_more': function() { fetchJSON(currentNode); },
			'n_tagsubnodes': function() { rgraph.op.tagSubnodes(currentNode)},
			'n_tagsubgraph': function() { rgraph.op.tagSubgraph(currentNode)},
			'n_untagsubgraph': function() { untagSubgraph(currentNode)},
			'n_en_names': function() { $.getJSON('/enzyme_data', { id: currentNode.id }, showEnzymeData); },
			'n_en_brendalink': function() { window.open('http://www.brenda-enzymes.org/php/result_flat.php4?ecno=' + currentNode.id); },
			'n_en_kegglink': function() { window.open('http://www.genome.jp/dbget-bin/www_bget?ec:' + currentNode.id); },
			'n_db_uni_link': function() { window.open('http://www.uniprot.org/uniprot/' + currentNode.id); },
			'n_db_frn_link': function() { window.open('http://www.ncrna.org/frnadb/detail.html?i_name=' + currentNode.id); }

		},
		'onContextMenu': function(event)
		{
			return (currentNode || currentEdge) && !busy;
		},
		'onShowMenu': function(evt, menu)
		{
			/* Removes all the menu items that are not applicable for the currently selected node/edge */
			/* The applicable menu entries are based on the prefix of the element id:
			 *     e_ - for read-dbentry-edges
			 *     n_ - for all nodes
			 *     n_en_ - for all enzyme nodes
			 *     n_db_ - for all database nodes
			 *     n_db_uni - for uniprot database nodes
			 *     n_db_frn - for frnadb database nodes
			 *     n_db_silva - for silva database nodes
			 */
			ctxMenuOpen = true;

			// menu clicks don't play too nicely with JIT - disable panning & tooltips temporarily and re-enable them when hiding the menu.
			rgraph.config.Navigation.panning = false;
			rgraph.config.Tips.enable = false;
			rgraph.tips.hide();

			if(!currentEdge || !currentEdge.data.blast_id ) 
				$('li[id^=e_]', menu).remove();
			if(!currentNode)
				$('li[id^=n_]', menu).remove();
			else
			{
				if(currentNode.data.type != 'enzyme')
					$('li[id^=n_en_]', menu).remove();
				if(currentNode.data.type != 'dbentry')
					$('li[id^=n_db_]', menu).remove();
				else
				{
					if(currentNode.data.source != 'uniprot')
						$('li[id^=n_db_uni]', menu).remove();
					if(currentNode.data.source != 'frnadb')
						$('li[id^=n_db_frn]', menu).remove();
                    if(currentNode.data.source.indexOf('silva') == -1)
                    	$('li[id^=n_db_silva]', menu).remove();

				}
			}
			return menu;
		},
		'onHideMenu': hideCtxMenu
	});
}
