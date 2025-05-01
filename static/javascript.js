$(document).ready(function () {

    $('#passwordVisible img:nth-child(1)').hide(); // Hide the open eye icon initially

    $('#passwordVisible img').on('click', function () { // Toggle visibility of the password visibility icon

        $('#passwordVisible img:nth-child(1)').toggle();
        $('#passwordVisible img:nth-child(2)').toggle();

        // Toggle input type between password and text
        var passwordInput = $('#passwordContainer input');
        var currentType = passwordInput.attr('type');

        if (currentType === 'password') { // If the current type is password, change it to text
            passwordInput.attr('type', 'text');
        } else { // If the current type is text, change it to password
            passwordInput.attr('type', 'password');
        }

    });

});