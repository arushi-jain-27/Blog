Skip to content
Features
Business
Explore
Marketplace
Pricing
This repository
Search
Sign in or Sign up
74 362 322 buckyroberts/Viberr
 Code  Issues 2  Pull requests 1  Projects 0  Insights
Viberr/music/static/music/js/main.js
7179fb8  on Mar 28, 2016
@buckyroberts buckyroberts Initial commit
     
61 lines (48 sloc)  1.04 KB

var AlbumsListPage = {
	init: function() {
		this.$container = $('.albums-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active');
				}
			});

			return false;
		});
	}
};

var SongsListPage = {
	init: function() {
		this.$container = $('.songs-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-favorite', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-star', self).toggleClass('active');
				}
			});

			return false;
		});
	}
};

$(document).ready(function() {
	AlbumsListPage.init();
	SongsListPage.init();
});
© 2018 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
API
Training
Shop
Blog
About
Press h to open a hovercard with more details.