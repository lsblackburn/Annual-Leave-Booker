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

$(document).ready(function() {

    $('input[type="date"]').on('click', function() {

        this.showPicker && this.showPicker();
        // When clicking on the whole input, show the native date picker

    });

});


$(document).ready(function () {
    $('.confirmation_pop').on('click', function (e) {
        e.preventDefault();
        var form = $(this).closest('form');
        
        if ($(this).hasClass('delete-user-form')) {
            var title = 'Are you sure want to delete this user?';
            var text = "You won't be able to revert this!";
            var confirmButtonText = 'Yes, delete it!';
        } else if ($(this).hasClass('revoke-user-form')) {
            var title = 'Are you sure want to revoke admin rights from this user?';
            var text = "This is a reversible action!";
            var confirmButtonText = 'Yes, revoke it!';
        } else if ($(this).hasClass('promote-user-form')) {
            var title = 'Are you sure want to promote this user to admin?'; 
            var text = "This is a reversible action!";
            var confirmButtonText = 'Yes, promote it!';
        }
        
        Swal.fire({
            title: title,
            text: text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: confirmButtonText
        }).then(function (result) {
            if (result.isConfirmed) {
                form.submit();
            }
        });
    });
});
