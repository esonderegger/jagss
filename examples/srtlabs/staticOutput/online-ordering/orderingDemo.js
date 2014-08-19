function prettyUSD(cents){
    return '$' + (cents/100).toFixed(2);
}
function addToCart(item, price) {
    var currentTotal = parseInt($("#cartData").data("total"), 10);
    currentTotal += price;
    $("#cartData").data("total", currentTotal);
    $("#currentTotal").html(prettyUSD(currentTotal));
    var currentNumItems = parseInt($("#cartData").data("numitems"), 10);
    currentNumItems = currentNumItems + 1;
    if (currentNumItems == 1){
        $("#itemCount").html("1 item");
    } else {
        $("#itemCount").html(currentNumItems + " items");
    }
    $("#cartData").data("numitems", currentNumItems);
    var currentItems = $("#cartData").data("items");
    if (currentNumItems == 1){
        currentItems = item;
    } else {
        currentItems += ', ' + item;
    }
    $("#cartData").data("items", currentItems);
}
$.getJSON('menu.json', function(data) {
    $.each(data.drinks, function(i) {
        var cItem = '<div class="col-12 col-sm-4 col-lg-3 cTownItem"';
        cItem += 'style="background: url(http://srtlabs.com/online-ordering/' + data.drinks[i].image + ') no-repeat center top;">';
        cItem += '<div class="itemName row"><a href="#' + data.drinks[i].name.replace(" ", "") + 'Sizes" data-toggle="collapse">';
        cItem += data.drinks[i].name + '</a></div>';
        cItem += '<div class="itemSizes collapse" id="' + data.drinks[i].name.replace(" ", "") + 'Sizes">';
        for (var j = 0; j < data.drinks[i].sizes.length; j++) {
            cItem += '<div class="itemSize row"><div class="col-9 text-right">';
            cItem += data.drinks[i].sizes[j].size + ' - ' + prettyUSD(data.drinks[i].sizes[j].price) + '</div>';
            cItem += '<div class="col-3 text-center"><button type="button" class="btn btn-success btn-small" ';
            var sizeName = data.drinks[i].sizes[j].size.split(" ")[0] + ' ' + data.drinks[i].name;
            cItem += 'onclick="addToCart(\'' + sizeName + '\', ';
            cItem += data.drinks[i].sizes[j].price + ')">add</button></div></div>';
        }
        cItem += '</div></div>';
        $("#menuDrinks").append(cItem);
    });
});
$('#checkoutButton').click(function(){
var currentTotal = parseInt($("#cartData").data("total"), 10);
var currentItems = $("#cartData").data("items");

var token = function(res){
    var $input = $('<input type=hidden name=stripeToken />').val(res.id);
    var $inputTotal = $('<input type=hidden name=cartTotal />').val(currentTotal);
    var $inputItems = $('<input type=hidden name=cartItems />').val(currentItems);
    $('form').append($input).append($inputTotal).append($inputItems).submit();
};

StripeCheckout.open({
key:         'pk_test_OU9JFitH2RwInYfkhPmXNFZf',
address:     false,
amount:      currentTotal,
currency:    'usd',
name:        'Mom and Pop Coffee Co.',
description: currentItems,
image:       'http://srtlabs.com/online-ordering/MomAndPopLogo.jpg', 
panelLabel:  'Charge',
token:       token
});

return false;
});