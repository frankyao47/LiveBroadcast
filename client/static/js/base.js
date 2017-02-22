//消息弹出框
Msgbox = {
    "dialog": function(msg, ok="确认", cancel="取消") {
        Ply.lang.ok = ok;
        Ply.lang.cancel = cancel;
        Ply.dialog("alert", msg);
    },
    "confirm": function(msg, ok="确认", cancel="取消") {
        Ply.lang.ok = ok;
        Ply.lang.cancel = cancel;
        Ply.dialog(
            "confirm",
            { effect: "3d-sign" },
            "msg"
        );
    }

};