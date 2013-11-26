// Source: http://jsfiddle.net/e8B9j/2/,
// Source: http://stackoverflow.com/questions/4165836/javascript-scale-text-to-fit-in-fixed-div
//
// Modified by Sergey Orshanskiy (added binary search to make it faster)


// Requires JQuery!




// Automatically resizes text to fit the given container.
// It finds the container with a class specified by @box. 
// @i is a dummy argument for $('some_class').each.
//
// Sample usage: 
// <div class="box" style="width:700px">This is a sentence</div>
// <div class="box" style="width:600px">This is a sentence</div>
// ...
// $( '.box' ).each(autosize_font);
function autosize_font ( i, box ) {
    var width = $( box ).width(),
        html = '<span style="white-space:nowrap">',
        line = $( box ).wrapInner( html ).children()[ 0 ];
    
    var l=1.0
    var r=500.0
    while (r-l>1) {      
        m = (l+r)/2
        $( box ).css( 'font-size', m );
        if ($( line ).width() >= width) {
             r = m   
        } else {
             l = m
        }
    }
    m=l
    $( box ).css( 'font-size', m );
    $( box ).text( $( line ).text() );
}
 
//$( '.dollar' ).each(autosize_font);
