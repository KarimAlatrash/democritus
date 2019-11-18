(function () {
	$(document).on('click', '.btn-submit', function() {
		if(!$(this).hasClass('loading')){
			$(this).addClass('loading');
			let self = this;
			
			setTimeout(function() {
				$(self).removeClass('loading');
				$(self).addClass('checked');
			},1500);
			
			setTimeout(function() {
				$(self).removeClass('checked');
			}, 3000);
		}
	});
})();