function Self(url) {

	/**
	 * 基础变量
	 */
	this.url = url;
	var fs = require('fs');
	this.fs = fs;
	this.page = require('webpage').create();
	this.page.settings.userAgent = 'SpecialAgent';
	this.page.settings.resourceTimeout = 20000; // 20 seconds
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
var fs = require('fs');

var content = fs.read('url.csv');
var arr = content.split("\n");
console.log('length:', arr.length);

// for (var i in arr) {
// // http://as.fang.anjuke.com/loupan/s?kw=恒大
// var url = arr[i];
// url = url.replace('anjuke.com', 'fang.anjuke.com/loupan/s?kw=恒大');
// city.log('打开页面:' + url);
// city.page.open(url, function(status) {
// city.log("Status: " + status);
// if (status != "success") {
// phantom.exit();
// } else {
// var params = {};
// params.keyword = "恒大";
// city.page.evaluate(function(params) {
// console.log("触发【搜索:" + params.keyword + "】事件。");
// document.getElementById("search-esf").value = params.keyword;
// $("#otherBtn").click();
// }, params);
// }
// });
// }

var aaa = function(index) {
	// http://as.fang.anjuke.com/loupan/s?kw=恒大
	var url = arr[index];
	url = url.replace('anjuke.com', 'fang.anjuke.com/loupan/s?kw=' + encodeURIComponent('恒大'));
	city.log('打开页面 ' + index + ' : ' + url);
	// test : 'http://beijing.fang.anjuke.com/loupan/s?kw=%E6%81%92%E5%A4%A7'
	city.page.open(url, function(status) {
		city.log("Status: " + status);
		if (status != "success") {
//			phantom.exit();
			aaa(index);
		} else {
			var arr = city.page.evaluate(function() {
				var arr = [];
				var city = $(".city").text();
				console.log('loupan length : ' + $(".list-contents>.list-results>.key-list>.item-mod").length);
				$(".list-contents>.list-results>.key-list>.item-mod").each(function(i, o) {
					var param = {};
					param.city = city;
					param.name = $(o).find(".infos h3 .items-name").text().replace(/\s+/g, "");
					var html = $(o).find(".favor-pos .price").html();
					if (html == undefined) {
						param.price = '';
						param.unit = '';
						param.content = $(o).find(".favor-pos").text().replace(/\s+/g, "");
					} else {
						param.price = $(o).find(".favor-pos .price span").text().replace(/\s+/g, "");
						param.unit = html.substring(html.indexOf('</span>') + 7).replace(/\s+/g, "");
						param.content = $(o).find(".favor-pos .price").text().replace(/\s+/g, "");
					}
					arr.push(param);
				});
				return arr;
			});
			for ( var i in arr) {
				city.fs.write('data.csv', arr[i].city + "\t" + arr[i].name + "\t" + arr[i].price + "\t" + arr[i].unit + "\t" + arr[i].content + "\n", 'a');
			}
			aaa(index + 1);
		}
	});
};
aaa(0);
// phantom.exit();
//
// setTimeout(function() {
// city.log('打开页面');
// city.page.open('http://as.fang.anjuke.com/loupan/s?kw=' +
// encodeURIComponent('恒大'), function(status) {
// city.log("Status: " + status);
// if (status != "success") {
// phantom.exit();
// }
// });
// }, city.wait(3000));
//
// setTimeout(function() {
// city.render(city.next());
// }, city.wait(1000));
//
// setTimeout(function() {
// var params = {};
// params.city = "上海";
// city.page.includeJs("http://libs.baidu.com/jquery/1.11.3/jquery.min.js",
// function() {
// city.page.evaluate(function(params) {
// console.log("触发【a:" + params.city + "】事件。");
// $(".cities_boxer a").each(function(i,o) {
// if ($(o).text() == params.city) {
// // 创建点击事件进行点击
// var clickEvent = document.createEvent("HTMLEvents");
// clickEvent.initEvent("click",false,true);
// $(o)[0].dispatchEvent(clickEvent);
// }
// });
// return obj;
// }, params);
// console.log("length:" + $(obj).attr('href'));
// });
// }, city.wait(5000));
//
// setTimeout(function() {
// city.render(city.next());
// }, city.wait(2000));
//
// setTimeout(function() {
// var params = {};
// params.keyword = "恒大";
// city.page.evaluate(function(params) {
// console.log("触发【搜索:" + params.keyword + "】事件。");
// document.getElementById("search-esf").value=params.keyword;
// $("#otherBtn").click();
// }, params);
// }, city.wait(5000));
//
// setTimeout(function() {
// city.render(city.next());
// }, city.wait(2000));
//
// setTimeout(function() {
// phantom.exit();
// }, city.wait(1000));
