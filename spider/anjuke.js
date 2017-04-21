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
		this.page.render(this.pic_path + '/picture_send' + step + '.png');
		this.log('==== 生成 ' + this.pic_path + '/picture_send' + step + '.png');
	};

	this.success_render = function(step) {
		this.page.render(this.success_path + '_' + step + '.png');
		this.log('==== 生成 ' + this.success_path + '_' + step + '.png');
	};

	this.fail_render = function(step) {
		this.page.render(this.fail_path + '_' + step + '.png');
		this.log('==== 生成 ' + this.fail_path + '_' + step + '.png');
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

var city = new Self('http://www.anjuke.com/sy-city.html');

setTimeout(function() {
	city.log('打开页面');
	city.page.open(city.url, function(status) {
		log("Status: " + status);
		if (status != "success") {
			phantom.exit();
		}
	});
}, city.wait(3000));

setTimeout(function() {
	city.render(city.next());
}, city.wait(1000));

setTimeout(function() {
	var params = {};
	params.city = "上海";
	city.page.includeJs("http://libs.baidu.com/jquery/1.11.3/jquery.min.js", function() {
		city.page.evaluate(function(params) {
			console.log("触发【a:" + params.city + "】事件。");
			$(".cities_boxer a").each(function(i,o) {
				if ($(o).text() == params.city) {
//					console.log("length:" + $(".cities_boxer a").eq(i).html());
//					console.log("length:" + $(o).attr('href'));
//					$(".cities_boxer a").eq(i).click();
					var clickEvent = document.createEvent("HTMLEvents");  
					clickEvent.initEvent("click",false,true);  
					$(o)[0].dispatchEvent(clickEvent);  
				}
			});
			return obj;
		}, params);
		console.log("length:" + $(obj).attr('href'));
	});
}, city.wait(10000));

setTimeout(function() {
	city.render(city.next());
}, city.wait(2000));

setTimeout(function() {
	phantom.exit();
}, city.wait(1000));
