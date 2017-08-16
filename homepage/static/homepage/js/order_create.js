function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).on('click', '#show-modal', function (e) {
    e.preventDefault();
    $('#order-modal').modal('show');
});

$(document).ready(function () {
    setTimeout(function () {
        $("#id_phone").rules("add", {
            minlength: 6,
            maxlength: 20
        });

        $("#id_first_name").rules("add", {
            maxlength: 50
        });

        $("#id_last_name").rules("add", {
            maxlength: 50
        });

        $("#hiddenRecaptcha").rules("add", {
            required: function () {
                return (grecaptcha.getResponse() == '');
            }
        });
    }, 1000);

    $("#user-data-form").validate({
        submitHandler: function (form) {
            var form_ = $('#user-data-form');

            var item_id = $('#id_item')[0].value;
            var count_nodes = $('#count');
            var count = count_nodes[0] && count_nodes[0].value;

            var userData = form_.serializeArray();
            var url = $('#sub-order-form').attr('action');

            var data = {
                order: {
                    item_id: item_id,
                    count: count
                },
                user: userData
            };

            $.ajaxSetup({
                headers: {"X-CSRFToken": getCookie("csrftoken")}
            });

            console.log(JSON.stringify(data))

            $.ajax({
                url: url,
                type: "POST",
                data: JSON.stringify(data),
                success: function () {
                    $('#order-modal').modal('hide')
                },

                error: function (error) {
                    alert(error + ' error')
                }
            })
        }
    });

});