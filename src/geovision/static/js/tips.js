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

				if(node.nodeFrom)
				{
					//if(node.data.bitscore)
					//{
						//it's an edge
						tip.innerHTML += "bitscore: " + node.data.bitscore + "<br/>";
						tip.innerHTML += "e-value: " + node.data.error_value + "<br/>";

					//}
					//else
					//	tip.innerHTML = 'enzyme edge';
				}
				else if(node.data.type != 'enzyme')
				{
					//it's a read or db entry
					tip.innerHTML += "<b>" + node.id + "</b><br/>";
					tip.innerHTML += node.data.description + "<br/>";
					if(node.data.hidden_nodes_count) tip.innerHTML += "<b>Matching hidden nodes:</b> " + node.data.hidden_nodes_count + "<br/>";
				}
				else
				{
					tip.innerHTML = "<b>" + node.id + "</b>";
					tip.innerHTML = tip.innerHTML + "<br/>" + node.data.name + "</br>";
					if(node.data.hidden_nodes_count) tip.innerHTML += "<b>Matching hidden nodes:</b> " + node.data.hidden_nodes_count + "<br/>";
				}
			}
};
