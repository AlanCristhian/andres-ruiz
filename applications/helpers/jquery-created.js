;(function($, undefined) {
    "use strict";


    $.fn.created = function(options) {
        var defaults = {
                element: undefined,
                delay: 33
            },
            settings = $.extend({}, defaults, options);


        return this.each(function () {
            var checker = setInterval(_check_existence, settings.delay),
                $this = $(this);

            function _check_existence() {
                if ($this.find(settings.element).length > 0) {
                    $this.trigger('created');
                    clearInterval(checker);
                }
            }
        });
    };
})(jQuery);