;(function($, undefined) {
    $.fn.resizeone = function(callback) {

        return this.each(function(index) {
            var $this = $(this),
                _width = $this.width(),
                _height = $this.height(),
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

                    // stop checking
                    clearInterval(timeoutID);
                }
            }
        });
    }
})(jQuery);