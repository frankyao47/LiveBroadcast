

$(function(){
	var api = {
		"getChannels": "http://139.196.56.202:8080/LiveBroadcast/api/getChannels.action",
		"authForWeixin": "http://139.196.56.202:8080/LiveBroadcast/api/authForWeixin.action",
	};

	function getChannels(offset = 0, limit = 10) {
		$.post(api.getChannels, {
			limit: limit, 
			offset: offset
		}, function(data) {
			if (!data.errno) {
				console.log(data.result);
			}
		})
	}

	function authForWeixin(weixin, avatar, nickname, gender) {
		$.post(api.authForWeixin, {
			weixin: weixin, 
			avatar: avatar,
			nickname: nickname,
			gender: gender
		}, function(data) {
			if (!data.errno) {
				console.log(data.result);
			}
		})
	}

	getChannels();
	
})