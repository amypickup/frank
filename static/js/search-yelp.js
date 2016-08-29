$(function() {
    $('#searchYelp').click(function() {

        $.ajax({
            url: '/searchYelp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});