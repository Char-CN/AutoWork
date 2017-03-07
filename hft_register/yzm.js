
function Self(url) {

	/**
	 * 基础变量
	 */

	this.url = url;
	var fs = require('fs');
	this.fs = fs;
	this.page = require('webpage').create();
	this.args = require('system').args;
	this.log_path = 'log';
	this.pic_path = 'pic';

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

};

url = '';
var self = new Self(url);

self.page.settings.userAgent = 'SpecialAgent';
self.log('默认userAgent: ' + self.page.settings.userAgent);
self.log('系统参数 : ' + self.args);

setTimeout(function() {
	self.log('打开主页');
	self.page.open('http://api.jmyzm.com/http.do?action=loginIn&uid=blazer111&pwd=hyy4646586', function(status) {
		if (status != "success") {
			phantom.exit();
		}
	});
}, self.wait(1000));

setTimeout(function() {
  var token = self.page.content;
  var index=self.page.content.indexOf('<body>');
  var lastIndex=self.page.content.indexOf('</body>');
  self.log("token:" + token.substring(index+6+9,lastIndex));
}, self.wait(1000));

setTimeout(function() {
	self.render(self.next());
}, self.wait(1000));







