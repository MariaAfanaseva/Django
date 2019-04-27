window.onload = function () {
    $('.basket-list').on('click', 'input[type="number"]', function () {
        var t_href = event.target;

        if (t_href.value > 0) {
            $.ajax({
                url: "/basket/edit/" + t_href.name + "/?quantity=" + t_href.value,

                success: function (data) {
                    $('.basket-total').html(data.result);
                },
            });
        }

        event.preventDefault();
    });
}