$ ->
	$('p > textarea').wrap('<div class="textarea"></div>')
	
	$('form > p > input, form > p > textarea, form > p > select').focus ->
		$(this).parent().addClass('focus')
	.blur ->
		$(this).parent().removeClass('focus')
	.parent().click ->
		$('input, textarea', this).focus()
	
	$('fieldset.composite p > input, fieldset.composite p > textarea, fieldset.composite p > select').focus ->
		$(this).closest('fieldset.composite').addClass('focus')
	.blur ->
		$(this).closest('fieldset.composite').removeClass('focus')
	.closest('fieldset.composite').click (e) ->
		if $.inArray(e.target.nodeName, ['INPUT', 'TEXTAREA', 'LABEL']) >= 0
			return
		$('input, textarea', this).first().focus()

	$('button').click (e) ->
		e.stopPropagation()

	$('p > div.textarea > textarea').focus ->
		$(this).parent().parent().addClass('focus')
	.blur ->
		$(this).parent().parent().removeClass('focus')
	.parent().parent().click ->
		$('textarea', this).focus()
	
	# Add .error class to invalid fields wrappers
	$('fieldset.composite .errorlist').closest('fieldset.composite').addClass('error')
	$('.errorlist + p').addClass('error')

	# Focus input when clicking on error item
	$('.errorlist li').each ->
		input = $(this).parent().next().find('input, textarea, select')
		$(this).click (e) ->
			e.stopPropagation()
			input.focus()

	# Merge error lists from multiple fields into single when using inside a composite field
	$('fieldset.composite').each ->
		errorlist = $('<ul></ul>').addClass('errorlist')
		errors = $('.errorlist li', this).append ->
			$('<span/>').text($(this).parent().next().find('label').text())
		.appendTo(errorlist)

		if errors.size()
			$('.errorlist', this).remove()
			$(this).before(errorlist)
	
	$('button, a.button').wrapInner('<span/>')
	
	# Advanced enrollment form controls
	enrollForm = $('form.enroll')
	if enrollForm.size()
		smartAddresses = $('<ul></ul>').addClass('smart-addresses')

		for domain in ['@unifr.ch', '@edu.hefr.ch']
			do (domain) ->
				address = $('<button/>')
					.addClass('small')
					.attr('type', 'button')
					.append($('<span/>').text(domain))
					.click (e) ->
						e.stopPropagation()
						$(this).closest('.email').find('input').val (index, val) ->
							(val + domain).replace(/@.*/, domain)
						.change()
						$(this).closest('form').find('.street input').focus()
					.appendTo($('<li></li>').appendTo(smartAddresses))

		$('form.enroll .email').append(smartAddresses)
		updateNames = ->
			input = $(this)
			[name, domain] = input.val().split('@')
			if domain in ['unifr.ch', 'edu.hefr.ch']
				[first_name, last_name] = name.split('.')
				if first_name and last_name
					$('form.enroll .first_name input').val(first_name.capitalize())
					$('form.enroll .last_name input').val(last_name.capitalize())
	
		$('form.enroll .email input')
			.change(updateNames)
			.keyup(updateNames)
			.attr('autocomplete', 'off')
			.focus()
		$('form.enroll .street_number input')
			.attr('autocomplete', 'off')
