window.onload = function () {
    var _quantity, _price, orderitemNum, deltaQuantity, orderitemQuantity, deltaCost;
    var quantityArr = [];
    var priceArr = [];
    var $orderForm = $('.order_form');
    var $orderTotalQuantity = $('.order_total_quantity');
    var $orderTotalCost = $('.order_total_cost');

    var TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());

    var orderTotalQuantity = parseInt($orderTotalQuantity.text()) || 0;
    var orderTotalCost = parseFloat($orderTotalCost.text().replace(',', '.')) || 0;

    function orderSummaryUpdate(orderitemPrice, deltaQuantity) {
       deltaCost = orderitemPrice * deltaQuantity;

       orderTotalCost = Number((orderTotalCost + deltaCost).toFixed(2));
       orderTotalQuantity = orderTotalQuantity + deltaQuantity;

       $orderTotalCost.html(orderTotalCost.toString());
       $orderTotalQuantity.html(orderTotalQuantity.toString());
    }

    for (i = 0; i < TOTAL_FORMS; i++) {
       _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
       _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
       quantityArr[i] = _quantity;
       if (_price) {
           priceArr[i] = _price;
       } else {
           priceArr[i] = 0;
       }
    }

    if (!orderTotalQuantity) {
       for (i = 0; i < TOTAL_FORMS; i++) {
           orderTotalQuantity += quantityArr[i];
           orderTotalCost += quantityArr[i] * priceArr[i];
       }
       $orderTotalQuantity.html(orderTotalQuantity.toString());
       $orderTotalCost.html(Number(orderTotalCost.toFixed(2)).toString());
    }

    $orderForm.on('change', 'input[type="number"]', function (event) {
       var target = event.target;
       orderitemNum = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
       if (priceArr[orderitemNum]) {
           orderitemQuantity = parseInt(target.value);
           deltaQuantity = orderitemQuantity - quantityArr[orderitemNum];
           quantityArr[orderitemNum] = orderitemQuantity;
           orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
       }
    });

    $orderForm.on('change', 'input[type="checkbox"]', function (event) {
       var target = event.target;
       orderitemNum = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
       if (target.checked) {
           deltaQuantity = -quantityArr[orderitemNum];
       } else {
           deltaQuantity = quantityArr[orderitemNum];
       }
       orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
    });

};