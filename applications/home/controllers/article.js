;(function(helpers, $, _, Backbone, ImageCollectionView, window, undefined) {
    "use strict";


    var main = window.main || {};


    /* Get the article name with the current location.pathname */
    main.get_article_name = function(pathname) {
        var pathname = pathname || window.location.pathname;
        pathname = pathname.replace('/proyectos/', '')
        pathname = pathname.replace('~andresru', '')
        // normalize the path
        if (pathname[0] === '/') {
            pathname = pathname.substr(1);
        }
        return pathname
    }


    // cache the global and unique DOM elements
    main.$image = $('#zoom-in-image');
    main.$wrapper = $('#zoom-in-container');
    main.$container = $('#full-size-box');


    // ======
    // Models
    // ======

    main.ImageModel = Backbone.Model.extend({
        defaults: {
            id: null,
            url: '',
            article_name: '',
            description: '',
            completed: false,
            quality: null,
            width: null,
            shard: null
        }
    });


    // ===========
    // Collections
    // ===========

    main.ImageCollection = Backbone.Collection.extend({
        url: helpers.set_path('images/' + main.get_article_name()),
        model: main.ImageModel
    });


    // =====
    // Views
    // =====


    main.ImageModelView = Backbone.View.extend({
        tagName: 'article'
        ,className: 'image_item'
        ,template: _.template($('#imageTemplate').html())

        ,render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }

        ,events: {
            'click .icon-resize-full': 'zoom_out_image'
        }

        ,fix_image_size: function($element, $wrapper, $container) {
            /* Adjust the image size of the viewport size without distorting.
            */

            function _resize_and_position() {
                var delta,
                    distance;

                // add styles
                $element.css({
                    'max-width': $container.outerWidth()
                    ,'max-height': $container.outerHeight()
                    ,'height': 'auto'
                    ,'width': 'auto'
                });

                // fix the position
                if ($element.outerHeight() < $container.outerHeight()) {
                    delta = $container.outerHeight() - $element.outerHeight();
                    distance = String(Math.round(delta/2)) + 'px';
                } else {
                    distance = '0px';
                }
                $wrapper.css({'top': distance});
            }

            $element.on('load resize error', _resize_and_position);
            $(window).on('resize', _resize_and_position);
        }

        ,zoom_out_image: function() {
            /* Show a box with the max size version of the image.*/
            var _url = this.model.get('url'),
                _src = 'http://src.sencha.io/jpg90/720/'
                    + helpers._PROTOCOL + '//'
                    + helpers._HOSTNAME
                    + helpers.set_path(_url);

            // set the path of the image in the DOM
            main.$image.attr('src', _src);
            // adjust the size of the image.
            this.fix_image_size(main.$image, main.$wrapper, main.$container);
            // Show the box with the image.
            main.$container.fadeIn();
        }
    });

    $('.icon-resize-small').on('click', function() {
        main.$container.fadeOut(function() {
            main.$image.attr('src', '');
        });
    })

    /* CAVEAT: I set the __testmode___ enviroment variable to true in the test
    app. I do that because I don't need an instance of 
    main.ImageCollectionView during the testing. But I need that during the
    production. This is equivalent to *if __name__ == "__main__":* on python.
    */
    if (typeof __testmode__ === 'undefined') {
        $(function() {
            main.image_collection_view = new ImageCollectionView({
                Collection: main.ImageCollection,
                ModelView: main.ImageModelView
            });
        });
    }


    // Expose main to the global object
    window.main = main;
})(helpers, jQuery, _, Backbone, ArticleCollectionView, window);
