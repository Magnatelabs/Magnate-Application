// Source: http://jsfiddle.net/e8B9j/2/,
// Source: http://stackoverflow.com/questions/4165836/javascript-scale-text-to-fit-in-fixed-div
//
// Modified by Sergey Orshanskiy (added binary search to make it faster)


// Requires JQuery!



// Automatically resizes text to fit the given container.
// It finds the container with a class specified by @box. Also only works with a div
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
    
    //console.log("autosizing " + i + " width " + width)
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


/*  OTHER JAVASCRIPT FOR DASHBOARD NAVIGATION, ETC. */

function toggleArticleActive(article_dom_id, is_active) {
  if (is_active) { // deactivate all that are active
    $('.article-active').each(function(index, value) {
      toggleArticleActive($(this).attr('id'), false);
    });
  }

  var a = $('#' + article_dom_id);
  a.attr("class", is_active ? "article-active" : "");

  if (is_active) {
    a.find(".show-when-article-active").show(); // can animate, e.g. show('slow')
    a.find('.show-when-article-not-active').children().addClass("nohover-underline");
    a.find('.fundfeed_title_active').addClass("nohover-underline"); 
    a.find(".show-when-article-not-active").hide();		

    // Load questions about this entry in the main div
    $('#div_activity').load('/f/?entry=' + article_dom_id.replace('entry-','') );
  } else {
    a.find(".show-when-article-active").hide();
    a.find(".show-when-article-not-active").show();
    a.find('.show-when-article-not-active').children().removeClass("nohover-underline");
    a.find('.fundfeed_title_active').removeClass("nohover-underline"); 
  }
}


function toggleArticleNotActive(article_dom_id, is_active) {
  if (is_active) { // deactivate all that are active
    $('.article-active').each(function(index, value) {
      toggleArticleActive($(this).attr('id'), false);
    });
  }
}  
  
  


// Added by Jimi W. 07.19.14
// Used for 'share lightbox'
// This script finds the container with a class specified, helps display placeholder text with a break in it and removes/replaces it
// depending on if someone has actually inputted text.

var placeholder = 'Hi there-- \nMagnate is a financial literacy platform that allows young people to learn about the world of investing. We can help you understand core concepts, save you money and help you invest that saved money wisely. There\'s no additional cost!\nSignup here: https:/\/www.magnate.io.\nHave fun!\nYour friends over at Magnate.';$('.sometin').attr('value', placeholder);

$('.sometin').focus(function(){
    if($(this).val() === placeholder){
        $(this).attr('value', '');
    }
});

$('.sometin').blur(function(){
    if($(this).val() ===''){
        $(this).attr('value', placeholder);
    }    
});

$('#btnHangoutsClose').click(function(){
	$('#hangoutsDropdown').slideUp(200);	
});