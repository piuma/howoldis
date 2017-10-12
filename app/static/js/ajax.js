jQuery(document).ready(function() {
    $('input#name').autocomplete({
	serviceUrl: $SCRIPT_ROOT + '/_autocomplete',
	minLength: 3,
        onSelect: function(suggestion) {
            console.log(suggestion.value); // not in your question, but might help later
        }
    });
});
