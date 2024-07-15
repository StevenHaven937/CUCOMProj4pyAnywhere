document.addEventListener('DOMContentLoaded', function () {
    'use strict';

const forms = document.querySelectorAll('.needs-validation');

Array.from(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }

        form.classList.add('was-validated');
    }, false);
    });

});

function sendEmail (url, message) {
    // Spinner scripts
    const spinnerBox = document.getElementById("spinner_box")
    const successBox = document.getElementById("success_box")
    const titleBox = document.getElementById("title_ID")
    const messageBox = document.getElementById("message_ID")

    $.ajax({
        type: 'GET',
        url: url,
        success: function(response){
            spinnerBox.classList.add('not-visible')
            successBox.innerHTML = response
            titleBox.innerText = "Success"
            messageBox.innerText = message
        },
        error: function(error){
            console.log(error)
        },
    })
}
