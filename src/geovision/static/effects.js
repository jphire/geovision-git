jQuery(function($) {
/*! Function to open the graph-option-navigation with a nice animation.
 */
    var opened = false;
    var closed = true;
    $('#graphnavi').mouseenter(function() {
        if (!opened){
            opened = true;
            $(this).find('#optiontag').hide();
            $(this).animate({width: "40%"}, {complete:
              function() { $(this).find('*').not('#optiontag').fadeIn();  }
            });
        }
    });
    $('#close').click(function() {
        if (opened){
            $('#graphnavi').find('*').hide();/*!Hide all elements*/
            $('#graphnavi').animate({width: "7px"}, {complete: function() {
                       $(this).find('#optiontag').fadeIn();
                       opened = false;
            }});
            
        }
    });
    $('#graphrefresh').click(function(){
	$('#loader').fadeIn();
    });
});