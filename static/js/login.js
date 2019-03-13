$(document).ready(function () {
    var setup = function () {
        // tab click
        $('.zh-tab > a').on('click', function () {
            var self = $(this);
            console.log('click a')
            $('.active').removeClass('active');
            self.addClass('active');
        });
        // tab action
        var tabAction = function (position, showLogin) {
            console.log(position);
            $(".zh-block").animate({
                "left": position
            }, "fast");
            $('#zh-form-login').toggle(showLogin);
            $('#zh-form-signup').toggle(!showLogin);
        };
        $('#zh-signup').on('click', function () {
            var position = '100px';
            var showLogin = false;
            tabAction(position, showLogin);
        });
        $('#zh-login').on('click', function () {
            var position = '155px';
            var showLogin = true;
            tabAction(position, showLogin);
        });
    };
    var __main = function () {
        setup();
        // select signup
        $('#zh-signup').click();
    };
    __main();
});