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
						tip.innerHTML += '<b>' + node.nodeFrom.id + ' <-> ' + node.nodeTo.id + '</b><br/>';
						tip.innerHTML += "bitscore: " + node.data.bitscore + "<br/>";
						tip.innerHTML += "e-value: " + node.data.error_value + "<br/>";
				}
				else if(node.data.type != 'enzyme')
				{
					//it's a read or db entry
					var source = node.data.source || node.data.sample;
					tip.innerHTML += "<b>" + node.id + "<br/>(" + source + ")</b><br/>";
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
