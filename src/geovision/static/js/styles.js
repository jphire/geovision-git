dotLineLength = function( x, y, x0, y0, x1, y1, o ){
	function lineLength( x, y, x0, y0 ){
		return Math.sqrt( ( x -= x0 ) * x + ( y -= y0 ) * y );
	}
	if( o && !( o = function( x, y, x0, y0, x1, y1 ){
		if( !( x1 - x0 ) ) return { x: x0, y: y };
		else if( !( y1 - y0 ) ) return { x: x, y: y0 };
		var left, tg = -1 / ( ( y1 - y0 ) / ( x1 - x0 ) );
		return { x: left = ( x1 * ( x * tg - y + y0 ) + x0 * ( x * - tg + y - y1 ) ) / ( tg * ( x1 - x0 ) + y0 - y1 ), y: tg * left - tg * x + y };
	}( x, y, x0, y0, x1, y1 ), o.x >= Math.min( x0, x1 ) && o.x <= Math.max( x0, x1 ) && o.y >= Math.min( y0, y1 ) && o.y <= Math.max( y0, y1 ) ) ){
		var l1 = lineLength( x, y, x0, y0 ), l2 = lineLength( x, y, x1, y1 );
		return l1 > l2 ? l2 : l1;
	}
	else {
		var a = y0 - y1, b = x1 - x0, c = x0 * y1 - y0 * x1;
		return Math.abs( a * x + b * y + c ) / Math.sqrt( a * a + b * b );
	}
};

RGraph.Plot.NodeTypes.implement({
    'customCircle': {
      'render': function(node, canvas){
          var pos = node.pos.getc(),
              radius = node.getData('dim');
          var ctx = canvas.getCtx();
          ctx.beginPath();
          ctx.arc(pos.x, pos.y, radius, 0, Math.PI * 2, true);
          ctx.closePath();
          ctx.fill();

          if(node.traversalTag)
          {
	          ctx.fillStyle = '#ffffff';
	          ctx.beginPath();
	          ctx.arc(pos.x, pos.y, radius/2, 0, Math.PI * 2, true);
	          ctx.closePath();
	          ctx.fill();
          }


        },
        'contains': function(node, pos){
          if(node.ignore)
              return false;
          var npos = node.pos.getc(true),
              radius = node.getData('dim');
          var diffx = npos.x - pos.x,
              diffy = npos.y - pos.y,
              diff = diffx * diffx + diffy * diffy;
          return diff <= radius * radius;
        }
    }
});

RGraph.Plot.EdgeTypes.implement({  
	'customArrow':{
	    'render': function(adj, canvas) {
            var from = adj.nodeFrom.pos.getc(),
                to = adj.nodeTo.pos.getc(),
                dim = adj.getData('dim'),
                direction = adj.data.$direction,
//                swap = (direction && direction.length>1 && direction[0] != adj.nodeFrom.id);
                swap = false; // XXX - may cause bugs

            var ctx = canvas.getCtx();
            Complex = $jit.Complex;
            // invert edge direction
            if (swap) {
              var tmp = from;
              from = to;
              to = tmp;
            }
            var vect = new Complex(to.x - from.x, to.y - from.y);
	    var norm = vect.norm();
            to.$add(vect.scale(-adj.nodeTo.getData("dim") / norm));
            from.$add(vect.$scale(adj.nodeFrom.getData("dim") / norm));
            vect = new Complex(to.x - from.x, to.y - from.y);

            vect.$scale(dim / vect.norm());
            var intermediatePoint = new Complex(to.x - vect.x, to.y - vect.y),
                normal = new Complex(-vect.y / 2, vect.x / 2),
                v1 = intermediatePoint.add(normal), 
                vM = intermediatePoint.clone();
                v2 = intermediatePoint.$add(normal.$scale(-1));
            
            ctx.beginPath();
	    if(from.x != from.x) return;
            ctx.moveTo(from.x, from.y);
            ctx.lineTo(vM.x, vM.y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(v1.x, v1.y);
            ctx.lineTo(v2.x, v2.y);
            ctx.lineTo(to.x, to.y);
            ctx.closePath();
            ctx.fill();

        },
        'contains': function(adj, pos) {
            var from = adj.nodeFrom.pos.getc(),
		        to = adj.nodeTo.pos.getc();
            var lineWidth = adj.getData('epsilon');
            var d = lineWidth/2;

            var vect = new Complex(to.x - from.x, to.y - from.y);
	    var norm = vect.norm();
            to.$add(vect.scale(-adj.nodeTo.getData("dim") / norm));
            from.$add(vect.$scale(adj.nodeFrom.getData("dim") / norm));

            var minX = Math.min(from.x, to.x) - d, maxX = Math.max(from.x, to.x) + d;
            var minY = Math.min(from.y, to.y) - d, maxY = Math.max(from.y, to.y) + d;
            if(pos.x < minX || pos.x > maxX || pos.y < minY || pos.y > maxY)
	            return false;
        return dotLineLength(pos.x, pos.y, from.x, from.y, to.x, to.y, false) < lineWidth;
	    }
    }
});  
