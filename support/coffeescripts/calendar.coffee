$ ->
    month = $('table.calendar').attr('summary')
    $('section.main.content > h1:first-child').text(month)
    $('head title').text (i, title) ->
        return title + ' · ' + month

