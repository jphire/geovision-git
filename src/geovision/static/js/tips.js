/* This is tooltip configurations file. You can change the shown info about nodes
 * or edges by modifying the innerHtml element.
 *
 */

Config.Tips = 
{
			enable: true,
			type: 'Native',
			align: 'left',
			
			onShow: function(tip, node)
			{
				if(ctxMenuOpen)
					return false;
				tip.innerHTML = "";
				if (!node) return false;
				//edge data
				if(node.nodeFrom)
				{
						tip.innerHTML += '<b>' + node.nodeFrom.id + ' <-> ' + node.nodeTo.id + '</b><br/>';
						tip.innerHTML += "bitscore: " + node.data.bitscore + "<br/>";
						tip.innerHTML += "e-value: " + node.data.error_value + "<br/>";
				}
				//node data
				else if(node.data.type != 'enzyme')
				{
					//it's a read or db entry
					var source = node.data.source || node.data.sample;
					tip.innerHTML += "<b>" + node.id + "<br/>(" + source + ")</b><br/>";
					tip.innerHTML += node.data.description + "<br/>";
				}
				else
				{
					tip.innerHTML = "<b>" + node.id + "</b><br/>" + node.data.name + "<br/>";
				}
				if(node.data.hidden_nodes_count) tip.innerHTML += "<b>Matching hidden nodes:</b> " + node.data.hidden_nodes_count + "<br/>";
			}
};
