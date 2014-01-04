$(function() {
    // cache al DOM elements
    var $figure = $('figure'),
        $imageContainer = $('#zoom-in-container'),
        $fullSizeBox = $('#full-size-box'),
        $img = $('img');

    

    function fix_image_size(element, wrapper, container) {
        /* Adjust the image size of the viewport size without distorting.
        */
        var $element = element instanceof $ ? element : $(element),
            $container = container instanceof $ ? container : $(container);
            $wrapper = wrapper instanceof $ ? wrapper : $(wrapper);
        /*
        while (true) {
            if ($element[0].naturalHeigth != 0
            || $element[0].naturalHeigth != '0'
            || $element.outerHeight != 0
            || $element.outerHeight != '0') {
                $element.animate({opacity: 1});
                break;
            }
        }
        */
        function _resize_and_position() {
            $element.css({
                'max-width': $container.outerWidth()
                ,'max-height': $container.outerHeight()
                ,'height': 'auto'
                ,'width': 'auto'
            });
            if ($element.outerHeight() < $container.outerHeight()) {
                delta = $container.outerHeight() - $element.outerHeight();
                distance = String(delta/2) + 'px';
            } else {
                distance = '0px';
            }
            $wrapper.css({'top': distance})
        }

        $element.on('load', _resize_and_position);
        $(window).resize(_resize_and_position);
    }


    function _zoom_out_image(_this) {
        /* Show a box with the max size version of the image.
        */
        // Get the path of the max size version of the image.
        var _src = $('.extralargeImage', _this).attr('src'),
            _start = _src.indexOf('database'),
            _image_path = _src.substring(_start, _src.length),
            $image = $('#zoom-in-image');

        // reports that the image has been magnified
        $.post(
            app.set_path('/articles/image-statistics')
            ,{
                'maximization_counter': 1
                ,'image_path': _image_path
            }
        );

        // set the path of the image in the DOM
        $image.attr('src', _src);
        // adjust the size of the image.
        fix_image_size($image, $imageContainer, $fullSizeBox);
        // Show the box with the image.
        $fullSizeBox.fadeIn();
    }

    function _zoom_in_image(_this) {
        // function _callback() {
        //     $('img', _this).animate({opacity: 0});
        // }
        // _this.fadeOut(_callback);
        _this.fadeOut();
    }


    function set_event_handlers(index) {
        /* Apply a set of event handlers to all elements inside the DOM element
        that call this function.
        */
        var $this = $(this);

        // HACK: I call the callback inside the lambda function to allow pass
        // the *$this* var to the callback.
        $('.icon-resize-full', $this)
            .on('click', function(){_zoom_out_image($this)});

        $('.icon-resize-small', $fullSizeBox)
            .on('click', function(){_zoom_in_image($fullSizeBox)});
    }


    $figure.each(set_event_handlers);
});