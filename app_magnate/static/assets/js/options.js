$(function(){
	Options.init();
});

/* 
	Options
*/
Options = {
	init: function() {
		$('.options .more').click(function() {
			var more = $(this);
			var options = more.parent();

			if (more.hasClass('closed')) {
				more.find('.fa').removeClass('fa-cog');
				more.find('.fa').addClass('fa-times');
				options.animate(
					{left: "+=220"}, 300, function() {
					more.removeClass('closed');
				});
			} else {
				more.find('.fa').removeClass('fa-times');
				more.find('.fa').addClass('fa-cog');
				options.animate(
					{left: "-=220"}, 300, function() {
					more.addClass('closed');
				});
			}
		});

		// Switch colors
		$('.options .colors a').click(function(e) {
			e.preventDefault();
			var color = $(this).attr('class');

			mainColor = color;
			// Switch google map marker
			GoogleMap.marker.setMap(null);
			GoogleMap.setMarker();

			if ($('link[title="colors"]').length) {
				$('link[title="colors"]').remove();
			}
			$('head').append('<link rel="stylesheet" title="colors" type="text/css" href="assets/css/colors/' + color + '.css">');

			// Switch chart color
			setTimeout(function() {
				if ($('.chart').data('easyPieChart') != undefined) {
					Charts.update();
				}
			}, 300);
		});
	}
}