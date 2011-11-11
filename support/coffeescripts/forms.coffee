$ ->
	$('p > textarea').wrap('<div class="textarea"></div>')
	
	$('form > p > input, form > p > textarea, form > p > select').focus ->
		$(this).parent().addClass('focus')
	.blur ->
		$(this).parent().removeClass('focus')
	.parent().click ->
		$('input, textarea', this).focus()
	
	$('form > p > label > input[type=checkbox]').focus ->
		$(this).parent().parent().addClass('focus')
	.blur ->
		$(this).parent().parent().removeClass('focus')
	.click (e) ->
		e.stopImmediatePropagation()
	.parent().click (e) ->
		e.stopImmediatePropagation()
	.parent().parent().click ->
		$('input', this).attr('checked', (index, val) -> not val)

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
	
	# Autosize textareas to fit content
	$('textarea.autosize').height ->
		$(this).prop('scrollHeight') + 2
	
	# Advanced enrollment form controls
	enrollForm = $('form.enroll, form.edit-member')
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

		$('.email', enrollForm).append(smartAddresses)
		updateNames = ->
			input = $(this)
			[name, domain] = input.val().split('@')
			if domain in ['unifr.ch', 'edu.hefr.ch']
				[first_name, last_name] = name.split('.')
				if first_name and last_name
					$('.first_name input', enrollForm).val(first_name.capitalize())
					$('.last_name input', enrollForm).val(last_name.capitalize())
	
		$('.email input', enrollForm)
			.change(updateNames)
			.keyup(updateNames)
			.attr('autocomplete', 'off')
			.focus()
		$('.street_number input', enrollForm)
			.attr('autocomplete', 'off')
