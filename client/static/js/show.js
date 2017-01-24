function show_danmu_panel() {
    $("#danmu-panel").show();
    $("#offline-panel").hide();
    $("#gift-panel").hide();
}

function show_gift_panel() {
    $("#gift-panel").show();
    $("#offline-panel").hide();
    $("#danmu-panel").hide();
}

function show_offline_panel() {
    $("#offline-panel").show();
    $("#danmu-panel").hide();
    $("#gift-panel").hide();
}
