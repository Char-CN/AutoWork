function Self(url) {

	/**
	 * 基础变量
	 */

	this.url = url;
	var fs = require('fs');
	this.fs = fs;
	this.page = require('webpage').create();
	this.args = require('system').args;
	this.login_info = {};
	this.login_info.code = this.args[1];
	this.login_info.user_name = this.args[2];
	this.login_info.password = this.args[3];
	this.run_time = '';
	this.pic_path = '';
	this.sms = {};
	this.sms.head = '【恒大金服】';
	this.sms.content = '';

	this.work_path = '';
	this.sms.content_path = 'msg.txt';
	this.sms.person_path = 'list.txt';

	if (this.args.length > 4) {
		this.work_path = this.args[4];
	}

	if (this.args.length > 5) {
		this.sms.content_path = this.args[5];
	}

	if (this.args.length > 6) {
		this.sms.person_path = this.args[6];
	}

	this.log_path = '';

	this.rst = {};
	this.rst.msgid = '';
	this.rst.taskid = '';

	/**
	 * 封装函数
	 */

	var getDate = function() {
		var date = new Date();
		var yyyy = date.getFullYear();
		var MM = date.getMonth() + 1;
		var dd = date.getDate();
		var HH = date.getHours();
		var mm = date.getMinutes();
		var ss = date.getSeconds();
		MM = MM < 10 ? "0" + MM : MM;
		dd = dd < 10 ? "0" + dd : dd;
		HH = HH < 10 ? "0" + HH : HH;
		mm = mm < 10 ? "0" + mm : mm;
		ss = ss < 10 ? "0" + ss : ss;
		return yyyy + "-" + MM + "-" + dd + " " + HH + ":" + mm + ":" + ss;
	};
	this.getDate = getDate;

	var nowTime = function() {
		var date = new Date();
		var yyyy = date.getFullYear();
		var MM = date.getMonth() + 1;
		var dd = date.getDate();
		var HH = date.getHours();
		var mm = date.getMinutes();
		var ss = date.getSeconds();
		MM = MM < 10 ? "0" + MM : MM;
		dd = dd < 10 ? "0" + dd : dd;
		HH = HH < 10 ? "0" + HH : HH;
		mm = mm < 10 ? "0" + mm : mm;
		ss = ss < 10 ? "0" + ss : ss;
		return yyyy + "" + MM + "" + dd + "_" + HH + "" + mm + "" + ss;
	};
	this.nowTime = nowTime;

	var log = function(str) {
		str = this.getDate() + " " + str;
		console.log(str);
		this.fs.write(this.log_path, str + "\n", 'a');
	};
	this.log = log;

	var exit = function(code) {
		this.log('退出程序.');
		this.log('共生成' + (this.next() - 1) + '张图片');
		this.log('总耗时' + (this.wait(0)) + '毫秒');
		this.page.close();
		phantom.exit(code == undefined ? 0 : code);
	};
	this.exit = exit;

	this.wait_time = 0;
	this.wait = function(add_time) {
		var wait_time_ = this.wait_time;
		this.wait_time += add_time;
		return wait_time_;
	};

	this.next_picture = 1;
	this.next = function() {
		return this.next_picture++;
	};

	this.render = function(step) {
		this.page.render(this.pic_path + '/picture_send' + step + '.png');
		this.log('==== 生成 picture_send' + step + '.png');
	};

	// 检查id是否存在
	this.existsId = function(id) {
		return this.page.evaluate(function(id) {
			var _btn = document.getElementById(id);
			return _btn == undefined || _btn == null ? false : true;
		}, id);
	};

	/**
	 * 回调函数
	 */

	this.page.onConsoleMessage = function(str) {
		str = getDate() + " [onConsoleMessage] " + str;
		console.log(str);
		fs.write(log_path, str + "\n", 'a');
	}

	this.page.onUrlChanged = function(str) {
		str = getDate() + " [onUrlChanged] " + str;
		console.log(str);
		fs.write(log_path, str + "\n", 'a');
	};

	/**
	 * 读取内容
	 */

	this.fs.changeWorkingDirectory(this.work_path);
	this.run_time = this.nowTime();
	this.pic_path = this.fs.workingDirectory + '/' + this.run_time;
	this.log_path = this.fs.workingDirectory + '/' + this.run_time + '/run.log';
	var log_path = this.fs.workingDirectory + '/' + this.run_time + '/run.log';
	if (this.fs.makeDirectory(this.pic_path)) {
		this.log('图片存放路径[' + this.pic_path + '] create success');
	} else {
		this.log('图片存放路径[' + this.pic_path + '] create fail');
	}
	this.sms.content = this.fs.read(this.sms.content_path);
	if (this.sms.content.lastIndexOf('\n') == this.sms.content.length - 1) {
		this.sms.content = this.sms.content.substr(0,
				this.sms.content.length - 1);
	}

	// 验证短信内容
	var check_content = function() {
		var total_content = this.sms.head + this.sms.content;
		this.log('发送内容: [' + total_content + ']');
		var total_length = this.sms.head.length + this.sms.content.length;
		this.log('字符长度: [' + total_length + ']');
		if (total_length > 70) {
			this.log('字符长度 > 70, return false, 未通过验证');
			return false;
		}
		this.log('字符长度 <= 70, return true, 通过验证');
		return true;
	};
	this.check_content = check_content;
};

var self = new Self('http://ums.zj165.com/index.jsp');

// 验证短信内容
// if (!self.check_content()) {
// self.exit(255);
// };

self.page.settings.userAgent = 'SpecialAgent';
self.log('默认userAgent: ' + self.page.settings.userAgent);
self.log('系统参数 : ' + self.args);

setTimeout(function() {
	self.log('打开主页');
	self.page.open(self.url, function(status) {
		log("Status: " + status);
		if (status != "success") {
			phantom.exit();
		}
	});
}, self.wait(3000));

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));

setTimeout(function() {
	self.log('填写登录信息');
	self.page.evaluate(function(self) {
		console.log("获取网页标题 : " + document.title);
		$("#spCode").val(self.login_info.code);
		$("#userName").val(self.login_info.user_name);
		$("#password").val(self.login_info.password);
	}, self);
}, self.wait(1000));

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));

setTimeout(function() {
	self.log('触发登录事件');
	self.page.evaluate(function() {
		var _btn = document.getElementsByClassName('login_btn')[0];
		var _event = document.createEvent('MouseEvents');
		_event.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0,
				false, false, false, false, 0, null);
		_btn.dispatchEvent(_event);
	});
}, self.wait(1000));

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));

setTimeout(function() {
	self.log('点击[短信标签页]');
	self.page.evaluate(function() {
		var _btn = document.getElementById('bizNav110201');
		var _event = document.createEvent('MouseEvents');
		_event.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0,
				false, false, false, false, 0, null);
		_btn.dispatchEvent(_event);
	});
}, self.wait(3000));

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));

setTimeout(function() {
	self.log('填写[短信内容]');
	self.log('短信内容:' + self.sms.content);
	self
			.log('短信长度:' + (self.sms.content.length + self.sms.head.length)
					+ '个字符');
	self.page.evaluate(function(content) {
		$("#sendTitleTextArea").val(content);
	}, self.sms.content);
}, self.wait(1000));

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));

setTimeout(function() {
	self.log('点击[使用个性化短信]');
	self.page.evaluate(function() {
		var _btn = document.getElementById('useSpecialSmsCK');
		var _event = document.createEvent('MouseEvents');
		_event.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0,
				false, false, false, false, 0, null);
		_btn.dispatchEvent(_event);
	});
}, self.wait(2000));

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));

setTimeout(function() {
	self.log('点击[选择文件] 文件路径:' + self.sms.person_path);
	self.page.uploadFile('input[name=dynaDataFile]', self.sms.person_path);
}, self.wait(300));

setTimeout(function(){
	if (self.existsId('dynDataImportFinishBtn')) {
		self.log('found.');
		return;
	}
}, 3000);

setTimeout(function(){
	if (self.existsId('dynDataImportFinishBtn')) {
		self.log('found.');
		return;
	}
}, 3000);

setTimeout(function(){
	if (self.existsId('dynDataImportFinishBtn')) {
		self.log('found.');
		return;
	}
}, 3000);

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));

setTimeout(function() {
	self.log('点击[完成 | 忽略并完成]');
	self.page.evaluate(function() {
		var _btn = document.getElementById('dynDataImportFinishBtn');
		var _event = document.createEvent('MouseEvents');
		_event.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0,
				false, false, false, false, 0, null);
		_btn.dispatchEvent(_event);
	});
}, self.wait(3000));

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));

setTimeout(function() {
	self.log('点击[发送]');
	self.page.evaluate(function() {
		var _btns = document.getElementsByClassName('confimbtn2 w120 mar10');
		var _btn;
		for ( var i in _btns) {
			if (_btns[i].innerHTML == "发送") {
				_btn = _btns[i];
			}
		}
		var _event = document.createEvent('MouseEvents');
		_event.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0,
				false, false, false, false, 0, null);
		_btn.dispatchEvent(_event);
	});
}, self.wait(3000));

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));

// setTimeout(function() {
// self.log('点击[确定发送]');
// self.page.evaluate(function() {
// var _btn = document.getElementById('confirmSendBtn');
// var _event = document.createEvent('MouseEvents');
// _event.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false,
// false, false, false, 0, null);
// _btn.dispatchEvent(_event);
// });
// }, self.wait(3000));

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));

setTimeout(function() {
	self.exit();
}, self.wait(0));
