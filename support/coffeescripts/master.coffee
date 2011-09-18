String.prototype.capitalize = ->
    this.charAt(0).toUpperCase() + this.slice(1)

$ ->
	# Set body min-height to the sidebar height
	$('body > .main').css('min-height', $('body > .sidebar').outerHeight(true) + $('body > header').outerHeight(true) - 56 + 20)

	# Support for manual switch between fixed/normal and wide/tight layout
	$('body').keypress (e) ->
		if $.inArray(e.target.nodeName, ['INPUT', 'TEXTAREA', 'SELECT']) >= 0
			return
		if e.charCode == 102
			$(this).toggleClass('fixed')
		else if e.charCode == 119
			$(this).toggleClass('wide')

	# Support for automatic switch between fixed and scroll layout
	sidebarHeight = $('body > .sidebar').outerHeight(true) + $('body > footer').outerHeight(true) + 95
	fixedThreshold = ->
		$(window).height() > sidebarHeight

	$(window).resize ->
		if fixedThreshold()
			$('body').addClass('fixed')
		else
			$('body').removeClass('fixed')
	.resize()

	###
	hideAll = ->
		$('section.messages').animate({'opacity': 0}, 300)
		.animate({
			'height': 0,
			'padding-top': 0,
			'padding-bottom': 0
		}, 70, -> $(this).remove())
	###
	
	$('section.messages li').click ->
		if $(this).siblings().size()
			$(this).remove()
		else
			$('section.messages').remove()
		
		###
		$(this).slideUp 300, ->
			if !$(this).siblings().size()
				hideAll()
			else
				$(this).remove()
				
		if !$(this).siblings().size()
			hideAll()
		###