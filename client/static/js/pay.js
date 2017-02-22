wx.config({
    debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
    appId: "wx6b2f0442b415ffc8", // 必填，公众号的唯一标识
    timestamp: timestamp, // 必填，生成签名的时间戳
    nonceStr: noncestr, // 必填，生成签名的随机串
    signature: signature,// 必填，签名，见附录1
    jsApiList: ["chooseWXPay"] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
});


//调用微信JS api 支付
function jsApiCall(amount)
{
    $.post("/api", 
        {
            "action": "addPurchaseOrder",
            "money": amount
        },
        function(data) {
            data = data.result;
            wx.chooseWXPay({
                timestamp: data.timeStamp, // 支付签名时间戳，注意微信jssdk中的所有使用timestamp字段均为小写。但最新版的支付后台生成签名使用的timeStamp字段名需大写其中的S字符
                nonceStr: data.nonceStr, // 支付签名随机串，不长于 32 位
                package: data.package, // 统一支付接口返回的prepay_id参数值，提交格式如：prepay_id=***）
                signType: data.signType, // 签名方式，默认为'SHA1'，使用新版支付需传入'MD5'
                paySign: data.paySign, // 支付签名
                appId: data.appId,
                success: function (res) {
                    Msgbox.dialog("支付成功", function() {
                        location.href = "/";
                    });
                }
            });
        });
    
}

//点击充值
function callpay()
{
    var item = $(".pay-amount-list li.active");

    if (item.length == 1) {
        var amount = item.data("amount");
        if (!amount) {
            amount = item.find("input").val();
            amount = parseInt(amount, 10);
        }

        if (!isNaN(amount) && amount > 0) {
            jsApiCall(amount);
        }
    }   

    // jsApiCall();
}

//点击金额
$(".pay-amount-list li").click(function() {
    $(".pay-amount-list li").removeClass("active");
    $(this).addClass("active");
});