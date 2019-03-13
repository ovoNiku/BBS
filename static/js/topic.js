var e = function (sel) {
    return document.querySelector(sel)
}

var es = function (sel) {
    return document.querySelectorAll(sel)
}

var markContents = function () {
    var contentDivs = es('.markdown-text')
//    var guaMarkdowns = es('.gua-markdown')
    for (var i = 0; i < contentDivs.length; i++) {
        var contentDiv = contentDivs[i]
//        var guaMarkdown = guaMarkdowns[i]
        // 掩饰注入攻击
//         var content = marked(contentDiv.textContent)
        var content = marked(contentDiv.textContent)
        // console.log(content, contentDiv.innerHTML)
        contentDiv.innerHTML = content
    }
}

var highlight = function () {
    var code_list = es('pre code')
    for (var i = 0; i < code_list.length; i++) {
        var code = code_list[i]
        code.className = code.className.replace('lang', 'language')
    }
}

var registerTimer = function () {
    setInterval(function () {
        var times = es('.gua-time')
        for (var i = 0; i < times.length; i++) {
            var t = times[i]
            var time = Number(t.id)
            var now = Math.floor(new Date() / 1000)
            var delta = now - time
            var s = `秒前 ${delta}`
            t.innerText = s
        }
    }, 1000)
}

var __main = function () {
    markContents()
    registerTimer()
    highlight()
}

__main()
