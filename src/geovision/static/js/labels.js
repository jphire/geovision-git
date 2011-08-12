/* Label configurations for nodes.
 */

$.extend(Config, {
		//Label styling is done via CSS!
		Label:
		{
			$extend: true,
			type: 'HTML',
			overridable: true,
		},
		onCreateLabel: function(domElement, node)
		{
			if(node.name)
				domElement.innerHTML = node.name.substr(0, 10);
		},
		//Change some label dom properties.
		//This method is called each time a label is plotted.
		onPlaceLabel: function(domElement, node)
		{
			var style = domElement.style;
			style.display = '';
			style.cursor = 'pointer';

			var left = parseInt(style.left);
			var w = domElement.offsetWidth;
			style.left = (left - w / 2) + 'px';
		}		
});
