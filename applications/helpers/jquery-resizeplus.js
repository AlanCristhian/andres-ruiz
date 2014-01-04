;(function($, undefined) {
    $.fn.resizeone = function(callback) {
        if (!jQuery.browser) {
            var userAgent = navigator.userAgent.toLowerCase();
            jQuery.browser = {};
            jQuery.browser.msie = /msie/.test(userAgent);
            jQuery.browser.mozilla = /mozilla/.test(userAgent) && !/webkit/.test(userAgent);
            jQuery.browser.webkit = /webkit/.test(userAgent);
            jQuery.browser.opera = /opera/.test(userAgent);
        }

        return this.each(function(index) {
            var $this = $(this),
                _width = $this.width(),
                _height = $this.height(),
                counter = 0,
                timeoutID;

            $this._width = _width;
            $this._height = _height;

            // start checking
            timeoutID = setInterval(_check_dimensions, 33);

            function _check_dimensions() {
                $this._width = $this.width();
                $this._height = $this.height();

                if (_width !== $this._width
                && _height !== $this._height) {
                    callback();
                    _width = $this._width;
                    _height = $this._height;
                    ++counter;

                    // stop checking
                    if ($.browser.opera && counter === 2) {
                        clearInterval(timeoutID);
                    } else {
                        clearInterval(timeoutID);
                    }
                }

            }
        });
    }
})(jQuery);