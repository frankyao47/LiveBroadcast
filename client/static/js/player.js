//url中获取播放器参数
var rtmp = getParamsFromMeta('rtmp'),
    hls = getParamsFromMeta('hls'),
    live = true,
    coverpic = getParamsFromMeta('coverpic'),
    width = $('.video-pane-head').outerWidth(),
    height = $('.video-pane-head').outerHeight(),
    autoplay = true;
/**
 * 视频类型播放优先级
 * mobile ：m3u8>mp4
 * PC ：RTMP>flv>m3u8>mp4
 */
var options = {
    rtmp: rtmp,
    m3u8: hls,
    coverpic: coverpic,
    autoplay: autoplay ? true : false,
    live: live,
    width : width,
    height : height,
    wording: {
        2032: '请求视频失败，请检查网络',
        2048: '请求m3u8文件失败，可能是网络错误或者跨域问题'
    },
    listener: function (msg) {
        //console.log(msg.type);
    }
};


player = new TcPlayer('video-container', options);
console.log(player);

//全屏后关闭弹幕
function checkFullScreen() {
    if (player.fullscreen()) {
        $(".video-pane-body").hide();
    }
    else {
        $(".video-pane-body").show();
    }
    setTimeout(function() { checkFullScreen(); }, 50);
}
checkFullScreen();

//landscape全屏
window.addEventListener("orientationchange", function() {
   player.size($('.video-pane-head').outerWidth(), $('.video-pane-head').outerHeight());
});