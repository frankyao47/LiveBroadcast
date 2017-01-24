$(function() {
    //打开/关闭礼物菜单
    $("#bt-gift").click(function() {
        show_gift_panel();
    });

    $(".gift-close").click(function() {
        show_danmu_panel();
    });

    $(".gift-list li").click(function() {
        $(".gift-list li").removeClass("active");
        $(this).addClass("active");
        //enable submit button
    });

    $(".gift-action button").click(function() {
        var item = $(".gift-list li.active");

        if (item.length == 1) {
            var giftModelId = item.find(".giftModelId").text();
            var cost = parseFloat(item.find(".gift-num strong").text());
            var anchorUid = $('meta[name="anchorUid"]').attr("content");

            $.post("/api", 
            {
                "action": "addGift",
                "anchorUid": anchorUid,
                "giftModelId": giftModelId
            },
            function(data) {
                if (data.errno != 0 || data.result == false) {
                    alert("赠送失败!");
                }
                else {
                    var last_coin = parseFloat($("#user-coin").text());
                    $("#user-coin").text(last_coin - cost);
                    alert("赠送成功!");
                }
            });
        }
    });

    //跳转到充值页面
    $("#bt-tipping").click(function() {
        location.href = "/pay";
    });
})

