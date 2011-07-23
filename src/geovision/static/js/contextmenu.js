
var currentNode;
var currentEdge;
var ctxMenuOpen;
var overLabel;

function hideCtxMenu()
{
	if(!ctxMenuOpen) return;
	ctxMenuOpen = false;
	if(currentNode) rgraph.config.Events.onMouseLeave(currentNode)
	if(currentEdge) rgraph.config.Events.onMouseLeave(currentEdge); // XXX does this work completely?
	busy = false;
	currentEdge = currentNode = false;
	rgraph.config.Navigation.panning = true;
	rgraph.config.Tips.enable = true;
//	rgraph.events.pressed = undefined;
}
function initContextMenu()
{
	$('#infovis').contextMenu('nodeMenu', {
		'shadow': false,
		'bindings': {
			'close': function() { },
			'n_center': function() {
				console.log(currentNode.id);
				var id = currentNode.id;
				busy = true;
				rgraph.onClick(id, { 
					type: 'fade:con', 
					fps:30, duration: 500, 
					hideLabels: false, 
					onComplete: function() { 
						busy = false;
						rgraph.canvas.getElement().style.cursor = '';
					}
				});
			},
			'e_align': function() { alignmentfunction(currentEdge.data.id); },
			'n_tag': function() { 
				if (currentNode.traversalTag != true) {
					tagNode(currentNode);
				}
				else {
					untagNode(currentNode);
				}
			},
			'n_tagparents': function() { rgraph.op.tagParents(currentNode)},
			'n_tagsubnodes': function() { rgraph.op.tagSubnodes(currentNode)},
			'n_tagsubgraph': function() { rgraph.op.tagSubgraph(currentNode)},
			'n_untagsubgraph': function() { untagSubgraph(currentNode)},
			'n_tagpath': function() { console.log(checkRootTagpath(currentNode))},
			'n_en_names': function() { $.getJSON('/enzyme_data?id=' + currentNode.id, showEnzymeData); },
			'n_en_brendalink': function() { window.open('http://www.brenda-enzymes.org/php/result_flat.php4?ecno=' + currentNode.id); },
			'n_en_kegglink': function() { window.open('http://www.genome.jp/dbget-bin/www_bget?ec:' + currentNode.id); },
			'n_db_uni_link': function() { window.open('http://www.uniprot.org/uniprot/' + currentNode.id); },
			'n_db_frn_link': function() { window.open('http://www.ncrna.org/frnadb/detail.html?i_name=' + currentNode.id); }

		},
		'onContextMenu': function(event)
		{
			return currentNode || currentEdge;
		},
		'onShowMenu': function(evt, menu)
		{
			ctxMenuOpen = true;
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
				}
			}
			return menu;
		},
		'onHideMenu': hideCtxMenu
	});
}
