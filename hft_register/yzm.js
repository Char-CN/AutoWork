var mobile = "";
var currentTime = "";
var zc_url = "https://hft02.evergrande.com/wechatPage/newRegisterPage.html?type=1&id=2762b1f9aa1e447cab317ea8ccf22a66";
var address_area = "广东";
function Self(url) {

	/**
	 * 基础变量
	 */

	this.url = url;
	var fs = require('fs');
	this.fs = fs;
	this.page = require('webpage').create();
	this.page.settings.userAgent = 'SpecialAgent';
	this.args = require('system').args;
	this.log_path = 'log';
	this.pic_path = 'pic';
	this.success_path = 'success';
	this.fail_path = 'fail';

	var setPicPath = function(p) {
		this.pic_path = p;
	};
	this.setPicPath = setPicPath;

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
	this.wait_time_default = 300;
	this.wait = function(add_time) {
		if (!add_time) {
			add_time = this.wait_time_default;
		}
		var wait_time_ = this.wait_time;
		this.wait_time += add_time;
		return wait_time_;
	};

	this.next_picture = 1;
	this.next = function() {
		return this.next_picture++;
	};

	this.render = function(step) {
		this.page.render(this.pic_path + "/" + currentTime + "_" + mobile + '/picture_send' + step + '.png');
		this.log('==== 生成 ' + this.pic_path + "/" + currentTime + "_" + mobile + '/picture_send' + step + '.png');
	};

	this.success_render = function(step) {
		this.page.render(this.success_path + "/" + currentTime + "_" + mobile + '_' + step + '.png');
		this.log('==== 生成 ' + this.success_path + "/" + currentTime + "_" + mobile + '_' + step + '.png');
	};

	this.fail_render = function(step) {
		this.page.render(this.fail_path + "/" + currentTime + "_" + mobile + '_' + step + '.png');
		this.log('==== 生成 ' + this.fail_path + "/" + currentTime + "_" + mobile + '_' + step + '.png');
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

var self = new Self('');
var self2 = new Self('');
self.log('\n\n');
self.log('系统参数 : ' + self.args);

setTimeout(function() {
	self.log('api登录');
	var url = 'http://api.jmyzm.com/http.do?action=loginIn&uid=blazer111&pwd=hyy4646586';
	self.page.open(url, function(status) {
		if (status != "success") {
			phantom.exit();
		}
	});
}, self.wait(1000));

token = "";
setTimeout(function() {
	// self.page.includeJs("http://libs.baidu.com/jquery/1.11.3/jquery.min.js",
	// function() {
	rst = self.page.evaluate(function() {
		return document.body.innerHTML;
	});
	self.log("rst:" + rst);
	arr = rst.split("|");
	token = arr[1];
	self.log("token:" + token);
	// });
}, self.wait(500));

setTimeout(function() {
	self.log('api获取手机号码');
	var pid = "1783"
	var address = encodeURIComponent(address_area);
	var url = "http://api.jmyzm.com/http.do?action=getMobilenum&pid=" + pid + "&uid=blazer111&token=" + token + "&mobile=&size=1&province=" + address;
	self.page.open(url, function(status) {
		if (status != "success") {
			phantom.exit();
		}
	});
}, self.wait(2000));

setTimeout(function() {
	rst = self.page.evaluate(function() {
		return document.body.innerHTML;
	});
	self.log("rst:" + rst);
	arr = rst.split("|");
	mobile = arr[0];
	currentTime = self.nowTime();
//	self.pic_path = mobile;
	self.setPicPath(mobile);
	self.log("mobile:" + mobile);
	if (mobile.length != 11) {
		self.log("api手机号码获取错误。");
		phantom.exit();
	}
}, self.wait());

setTimeout(function() {
	//	var zc_url = 'https://hft02.evergrande.com/wechatPage/newRegisterPage.html?type=1&id=4713e7edf0254b8a996b2bcc113f64d4';
	self2.log('web打开恒房通页面');
	self2.page.open(zc_url, function(status) {
		if (status != "success") {
			phantom.exit();
		}
		self.log('web填写手机号码，并点击发送验证码按钮。');
	});
}, self.wait(1500));

setTimeout(function() {
	var params = {};
	params.mobile = mobile;
	self2.page.evaluate(function(params) {
		$("#phone").val(params.mobile);
//		$("#phone").val("15618194808");
		// 触发验证码事件
		console.log("触发【发送验证码】事件。");
		$("#send_code").click();
		console.log("触发【发送验证码】事件成功。");
	}, params);
}, self.wait(2000));

setTimeout(function() {
	self2.log('保存图片');
	self2.render(self.next());
}, self.wait(1000));

var count = 1;
var forCode = function() {
	self.log('\n');
	self.log('api获取[' + mobile + ']验证码第' + count + '次');
	var url = "http://api.jmyzm.com/http.do?action=getVcodeAndReleaseMobile&uid=blazer111&token=" + token + "&mobile=" + mobile;
	self.page.open(url, function(status) {
		if (status != "success") {
			self.log("获取验证码时。异常退出！");
			phantom.exit();
		}
		rst = self.page.evaluate(function() {
			return document.body.innerHTML;
		});
		self.log("第" + count + "次获取结果:" + rst);
		if (rst == "not_receive" || rst == "not_found_moblie") {
			setTimeout(forCode, 2000);
		} else {
			var arr = rst.split("|");
			self.log('web填写姓名、短信验证码、密码、重复密码，并点击注册按钮。');
			var params = {};
			params.code = arr[1];
			self2.page.evaluate(function(params) {
				console.log("获取验证码成功：" + params.code);
				params.code = params.code.replace(/[^0-9]/ig,"");
				console.log("解析之后的验证码为:" + params.code);
				$("#nick").val("李刚");
				$("#code").val(params.code);
//				$("#code").val("123456");
				$("#password").val("qweqwe");
				$("#check").val("qweqwe");
				// 出发注册事件
				console.log("触发【注册】事件");
				Register.toRegister();
//				console.log($('#register-word').parent().parent().parent().click());
//				$('#register-word').parent().parent().parent().click();
				console.log("触发【注册】事件成功。");
			}, params);
			setTimeout(function() {
				self2.log('保存图片');
				self2.render(self.next());
			}, 500);
			setTimeout(function() {
				self2.log('保存图片');
				self2.render(self.next());
			}, 1500);
			setTimeout(function() {
				self2.log('保存图片');
				self2.render(self.next());
				var rst = self2.page.evaluate(function(self2) {
					var local_url = "" + document.location.href;
					console.log(document.location.href);
					if (local_url == "http://appd.evergrande.com/hengfangtong/index_gg.jsp") {
						console.log("成功！成功！成功！成功！成功！成功！成功！成功！成功！成功！成功！成功！成功！成功！成功！成功！");
						return true;
					} else {
						console.log("失败！失败！失败！失败！失败！失败！失败！失败！失败！失败！失败！失败！失败！失败！失败！失败！");
						return false;
					}
				}, self2);
				if (rst) {
					self2.success_render(self.next());
				} else {
					self2.fail_render(self.next());
				}
				self.log("api加入黑名单。");
				var pid = "1783"
				var url = "http://api.jmyzm.com/http.do?action=addIgnoreList&pid=" + pid + "&uid=blazer111&token=" + token + "&mobiles=" + mobile;
				self.page.open(url, function(status) {
					if (status != "success") {
						self.log("加入黑名单。异常退出！");
						phantom.exit();
					}
				});
				setTimeout(function() {
					rst = self.page.evaluate(function() {
						return document.body.innerHTML;
					});
					self.log("加入黑名单结果:" + rst);
					phantom.exit();
				}, 1000);
			}, 3000);
		}
		if (count == 15) {
			self.log("api加入黑名单。");
			var pid = "1783"
			var url = "http://api.jmyzm.com/http.do?action=addIgnoreList&pid=" + pid + "&uid=blazer111&token=" + token + "&mobiles=" + mobile;
			self.page.open(url, function(status) {
				if (status != "success") {
					self.log("加入黑名单。异常退出！");
					phantom.exit();
				}
			});
			setTimeout(function() {
				rst = self.page.evaluate(function() {
					return document.body.innerHTML;
				});
				self.log("加入黑名单结果:" + rst);
				self.log("api手机号码获取错误次数达到 15 次。退出程序！");
				phantom.exit();
			}, 1000);
		}
		count++;
	});
}

setTimeout(forCode, self.wait(2000));





