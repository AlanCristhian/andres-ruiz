;(function($, undefined) {
    "use strict";


    $.fn.sizeloaded = function(options) {
        var defaults = {
                delay: 33
            },
            settings = $.extend({}, defaults, options);


        return this.each(function () {
            var checker = setInterval(_check_dimensions,
                    settings.delay),
                $this = $(this),
                image = $this[0];

            $this.on('error', function() {
                $this.trigger('sizeloaded');
                clearInterval(checker);
            });

            function _check_dimensions() {
                if (image.naturalWidth !== 0
                && image.naturalHeight !== 0
                || image.complete) {
                    $this.trigger('sizeloaded');
                    clearInterval(checker);
                }
            }
        });
    };
})(jQuery);