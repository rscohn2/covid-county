var states
var cur_state = ''
var cur_county = ''

function update_state() {
    var $dropdown = $('#state')
    var key = $dropdown.val()
    var vals = []

    if (key in states) {
        vals = states[key]
    } else {
        vals = ['Choose State Above']
    }
					
    var $county = $('#county')
    $county.empty()
    $county.append('<option> Choose County </option>')
    $.each(vals, function(index, value) {
	$county.append('<option>' + value + '</option>')
    });
}

function update_county() {
    var state = $('#state').val()
    var county = $('#county').val()
    if (cur_state == '')
	$('#plot').attr('src', '/images/' + county + ':' + state + '.png')
    else if (state != cur_state || county != cur_county)
	window.location.href = '?state=' + state + '&county=' + county
    cur_state = state
    cur_county = county
}

function process_query() {
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('state')) {
	state = urlParams.get('state')
	if (!(state in states)) {
	    console.log('Unknown state: ' + state)
	    return
	}
	$('#state').val(state)
	update_state()

	if (urlParams.has('county')) {
	    county = urlParams.get('county')
	    counties = states[state]
	    if (!counties.includes(county)) {
		console.log('Unknown county: ' + county)
		return
	    }
	    $('#county').val(county)
	    update_county(state, county)
	}
    }
}

function process_data(data) {
    states = data
    var $state = $('#state')
    var vals = Object.keys(data)
    $.each(vals, function(index, value) {
	$state.append("<option>" + value + "</option>")
    });

    process_query()
}

$(function() {
    $('#state').change(update_state)

    $('#county').change(update_county)

    $( document ).ready(function() {
        $.getJSON('jsondata/counties.json', process_data)
    })
});
