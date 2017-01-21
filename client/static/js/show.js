function getParamsFromMeta(name) {
    return $('meta[name=' + name + ']').attr("content");
}

//video player相关逻辑
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


    //IM相关逻辑
    //独立模式，应用名称
    var accountMode = 0;
    var sdkAppID = 1400021877;
    var accountType = 9480;
    var avChatRoomId = getParamsFromMeta("groupId");
    var identifier = getParamsFromMeta("identifier");
    var userSig = getParamsFromMeta("userSig");
    var headurl = getParamsFromMeta("headurl");

    var selType = webim.SESSION_TYPE.GROUP; //广播/私聊
    var selToID = avChatRoomId;
    var selSess = null;

    //默认群组头像(选填)
    var selSessHeadUrl = 'img/2017.jpg';

    //当前用户身份
    var loginInfo = {
        'sdkAppID': sdkAppID, //用户所属应用id,必填
        'appIDAt3rd': sdkAppID, //用户所属应用id，必填
        'accountType': accountType, //用户所属应用帐号类型，必填
        'identifier': null, //当前用户ID,必须是否字符串类型，选填
        'identifierNick': "null", //当前用户昵称，选填
        'userSig': null, //当前用户身份凭证，必须是字符串类型，选填
        'headurl': 'img/2016.gif'//当前用户默认头像，选填
    };

    //监听（多终端同步）群系统消息方法，方法都定义在demo_group_notice.js文件中
    //注意每个数字代表的含义，比如，
    //1表示监听申请加群消息，2表示监听申请加群被同意消息，3表示监听申请加群被拒绝消息等
    var onGroupSystemNotifys = {
        //"1": onApplyJoinGroupRequestNotify, //申请加群请求（只有管理员会收到,暂不支持）
        //"2": onApplyJoinGroupAcceptNotify, //申请加群被同意（只有申请人能够收到,暂不支持）
        //"3": onApplyJoinGroupRefuseNotify, //申请加群被拒绝（只有申请人能够收到,暂不支持）
        //"4": onKickedGroupNotify, //被管理员踢出群(只有被踢者接收到,暂不支持)
        "5": onDestoryGroupNotify, //群被解散(全员接收)
        //"6": onCreateGroupNotify, //创建群(创建者接收,暂不支持)
        //"7": onInvitedJoinGroupNotify, //邀请加群(被邀请者接收,暂不支持)
        //"8": onQuitGroupNotify, //主动退群(主动退出者接收,暂不支持)
        //"9": onSetedGroupAdminNotify, //设置管理员(被设置者接收,暂不支持)
        //"10": onCanceledGroupAdminNotify, //取消管理员(被取消者接收,暂不支持)
        "11": onRevokeGroupNotify, //群已被回收(全员接收)
        "255": onCustomGroupNotify//用户自定义通知(默认全员接收)
    };


    //监听连接状态回调变化事件
    var onConnNotify = function (resp) {
        switch (resp.ErrorCode) {
            case webim.CONNECTION_STATUS.ON:
                //webim.Log.warn('连接状态正常...');
                break;
            case webim.CONNECTION_STATUS.OFF:
                webim.Log.warn('连接已断开，无法收到新消息，请检查下你的网络是否正常');
                break;
            default:
                webim.Log.error('未知连接状态,status=' + resp.ErrorCode);
                break;
        }
    };


    //监听事件
    var listeners = {
        "onConnNotify": onConnNotify, //选填
        "jsonpCallback": jsonpCallback, //IE9(含)以下浏览器用到的jsonp回调函数,移动端可不填，pc端必填
        "onBigGroupMsgNotify": onBigGroupMsgNotify, //监听新消息(大群)事件，必填
        "onMsgNotify": onMsgNotify,//监听新消息(私聊(包括普通消息和全员推送消息)，普通群(非直播聊天室)消息)事件，必填
        "onGroupSystemNotifys": onGroupSystemNotifys, //监听（多终端同步）群系统消息事件，必填
        "onGroupInfoChangeNotify": onGroupInfoChangeNotify//监听群资料变化事件，选填
    };

    var isAccessFormalEnv = true; //是否访问正式环境
    var isLogOn = true; //是否在浏览器控制台打印sdk日志
    //其他选项
    var options = {
        'isAccessFormalEnv': isAccessFormalEnv,
        'isLogOn': isLogOn
    };

    var curPlayAudio = null;
    var openEmotionFlag = false; //是否打开过表情
    sdkLogin();

