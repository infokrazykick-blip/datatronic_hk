/*//在本网页的任何键盘敲击事件都是无效操作 （防止F12和shift+ctrl+i调起开发者工具）
window.onkeydown = window.onkeyup = window.onkeypress = function () {
    window.event.returnValue = false;
    return false;
};
//禁用开发者工具F12
document.onkeydown = function () {
    if (window.event && window.event.keyCode == 123) {
        event.keyCode = 0;
        event.returnValue = false;
        return false;
    }
};*/

//禁用F12
window.onkeydown = window.onkeyup = window.onkeypress = function (event) {
    // 判断是否按下F12，F12键码为123
    if (event.keyCode == 123) {
        event.preventDefault(); // 阻止默认事件行为
        window.event.returnValue = false;
    }
};
//屏蔽右键菜单
document.oncontextmenu = function (event) {
    if (window.event) {
        event = window.event;
    }
    try {
        var the = event.srcElement;
        if(!((the.tagName == "INPUT" && the.type.toLowerCase() == "text") || the.tagName == "TEXTAREA")) {
            return false;
        }
        return true;
    } catch (e) {
        return false;
    }
};


window.addEventListener('DOMContentLoaded', function () {
    var system = {};
    var p = navigator.platform;
    system.win = p.indexOf("Win") == 0;
    system.mac = p.indexOf("Mac") == 0;
    system.ispc = navigator.userAgent.match(/spider|iPad|iPhone|iPod|Android/i) == null;
    if (system.win || system.mac || system.ispc) {
        var host = window.location.host;
        $("head").html('<meta charset="UTF-8"><meta name="referrer" content="no-referrer"><title>网页无法访问</title> ');
        $("body").html('<iframe style="width:100%;height:100%;position:absolute;left:0%;top:0%;z-index:999999" id="mainFrame" src="/n404.html" frameborder="0" scrolling="yes"></iframe>').show()
    }
});