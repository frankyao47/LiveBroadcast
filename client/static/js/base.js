//消息弹出框
Msgbox = {
    "dialog": function(msg, done=null, ok="确定", cancel="取消") {
        Ply.lang.ok = ok;
        Ply.lang.cancel = cancel;
        Ply.dialog("alert", msg)
        .done(function (ui) {
            if (done) done();
        });
    },
    "confirm": function(msg, done, fail,  ok="确定", cancel="取消") {
        Ply.lang.ok = ok;
        Ply.lang.cancel = cancel;
        Ply.dialog(
            "confirm",
            { effect: "3d-sign" },
            msg
        )
        .done(function (ui) {
            done();
        })
        .fail(function (ui) {
            fail();
        });
    }
};

function getParamsFromMeta(name) {
    return $('meta[name=' + name + ']').attr("content");
}