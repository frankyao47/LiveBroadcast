cost = parseInt(getParamsFromMeta("cost"));
money = parseInt(getParamsFromMeta("money"));
next = getParamsFromMeta("next");
anchorUid = getParamsFromMeta("anchorUid");

if (cost < money) {
    msg = "当前直播需要支付" + cost +"金币后才可以观看，是否支付？（现有金币：" + money + "）"
    Msgbox.confirm(
        msg,
        function() { //支付逻辑
            $.post("/api",
            {
                "action": "checkChannelRecord",
                "anchorUid": anchorUid
            },
            function(data) {
                status = data.result.status;
                message = data.result.message;
                if (data.errno != 0 || status != 0) {
                    Msgbox.dialog("支付失败," + message + "!", function() {
                        location.href = "/";
                    });

                }
                else {
                    Msgbox.dialog("支付成功!", function() {
                        location.href = next;
                    });
                }
            });
        },
        function() { //取消，退回大厅
            location.href = "/";
        });
}
else {
    msg = "当前直播需要支付" + cost +"金币后才可以观看，您的金币不足，是否充值？（现有金币：" + money + "）";
    Msgbox.confirm(
        msg,
        function() { //跳转到充值页面
            location.href = "/pay/";
        },
        function() { //取消，退回大厅
            location.href = "/";
        },
        "充值");
}