jQuery(function($) {
/*! Function to open the graph-option-navigation with a nice slide.
 */
    var opened = false;
    var closed = true;
    $('#graphnavi').mouseenter(function() { /*if mouse enters right edge.. */
        if (!opened){ /*if open, do nothing*/
            opened = true;
            $(this).find('#optiontag').hide();
            $(this).animate({width: "40%"}, {complete: /*otherwise slide menu open and after that fill in content*/
              function() { $(this).find('*').not('#optiontag').fadeIn();  }
            });
        }
    });
    $('#close').click(function() {/*if user clicks close-button..*/
        if (opened){ /*if not open, do nothing*/
            $('#graphnavi').find('*').hide();/*Hide all elements inside*/
            $('#graphnavi').animate({width: "7px"}, {complete: function() {
                       $(this).find('#optiontag').fadeIn();/*close navi and show optiontag*/
                       opened = false;
            }});
            
        }
    });
});