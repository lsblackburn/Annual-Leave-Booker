$(document).ready(function () {

    $('#passwordVisible img:nth-child(1)').hide();

    $('#passwordVisible img').on('click', function () {

        $('#passwordVisible img:nth-child(1)').toggle();
        $('#passwordVisible img:nth-child(2)').toggle();

        // Toggle input type between password and text
        var passwordInput = $('#passwordContainer input');
        var currentType = passwordInput.attr('type');

        if (currentType === 'password') {
            passwordInput.attr('type', 'text');
        } else {
            passwordInput.attr('type', 'password');
        }

    });

});