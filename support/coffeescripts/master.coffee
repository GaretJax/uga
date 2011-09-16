$ ->
	$('body > .main').css('min-height', $('body > .sidebar').outerHeight(true) + 20)

	$('body').keypress (e) ->
		if e.charCode == 102
			$(this).toggleClass('fixed')
		else if e.charCode == 119
			$(this).toggleClass('wide')

	sidebarHeight = $('body > .sidebar').outerHeight(true) + $('body > footer').outerHeight(true) + 95
	fixedThreshold = ->
		$(window).height() > sidebarHeight

	$(window).resize ->
		if fixedThreshold()
			$('body').addClass('fixed')
		else
			$('body').removeClass('fixed')
	.resize()
	