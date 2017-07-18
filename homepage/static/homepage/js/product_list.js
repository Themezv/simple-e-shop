const list_url = "/market/shop/filter";

$(document).on("submit", ".get-product-list-form", function (e) {
    e.preventDefault();
    var data = $(this).serialize();

    $.ajax({
        type: "GET",
        url: list_url,
        // url: $(this).attr("action"),
        data: data,
        success: function (html) {
            $("#product-list").html(html)
        },
        error: function (e) {
            $("#product-list").html(
                "<h2>Нет таких товаров</h2>"
            )
        }
    });
});

// $(document).on("click", ".get-product-list-link", function (e) {
//     e.preventDefault();
//     var data = $(this).serialize();
//
//     $.ajax({
//         type: "GET",
//         url: list_url,
//         data: data,
//         success: function (html) {
//             $("#product-list").html(html)
//         }
//     });
// });