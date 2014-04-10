;(function(helpers, $, _, Backbone, ImageCollectionView, window, undefined) {
    "use strict";


    var main = window.main || {};


    // cache the global and unique DOM elements
    main.$image = $('#zoom-in-image');
    main.$wrapper = $('#zoom-in-container');
    main.$container = $('#full-size-box');
    main.$spinner = $('#zoom-spinner');
    main.$item_wrapper = $("#item-wrapper figure");


    // ======
    // Models
    // ======

    main.ImageModel = Backbone.Model.extend({
        defaults: {
            id: '',
            url: '',
            article_name: '',
            description: '',
            completed: false,
            quality: '',
            width: '',
            height: '',
            shard: '',
            vid: ''
        }
    });


    // ===========
    // Collections
    // ===========

    main.ImageCollection = Backbone.Collection.extend({
        url: helpers.set_path('images/' +
                helpers.get_article_name('/proyectos/')),
        model: main.ImageModel
    });


    // =====
    // Views
    // =====


    main.ImageModelView = Backbone.View.extend({
        tagName: 'article'
        ,className: 'image_item'

        // Choose the correct template depending on the type of media file
        ,_set_template: function() {
            var multimedia_type = this.model.get('type');

            // The template and the className depends whether the model is an
            // image, link or video.
            if (multimedia_type === 'image_file') {
                this.templateId = '#image_file_template';
                this.className = '.image_file_container';
            } else if (multimedia_type === 'image_link') {
                this.templateId = '#image_link_template';
                this.className = '.image_link_container';
            } else if (multimedia_type === 'video_link') {
                this.templateId = '#video_link_template';
                this.className = '.video_link_container';
            } else {
                this.templateId = '#image_link_template';
                this.className = '.image_link_container';
            }
            this.template = _.template($(this.templateId).html());
        }

        ,initialize: function() {
            this._set_template();
        }

        ,render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            var _image = this.$el.find('img'),
                _item_container = this.$el
                    .find('.article_item_container figure');
            return this;
        }

        ,events: {
            'click img': 'zoom_out_image'
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

            $element
                .sizeloaded()
                .on('sizeloaded', _resize_and_position);
            $(window).on('resize', _resize_and_position);
        }

        ,zoom_out_image: function() {
            /* Show a box with the max size version of the image.*/
            var _src = 'http://src.sencha.io/jpg90/1920/1080/' +
                    this.model.get('url'),
                _this = this;
            // set the path of the image in the DOM
            main.$image
                .attr('src', _src)
                .sizeloaded()
                .one('sizeloaded', function() {
                    main.$spinner.fadeOut('slow');
                    main.$item_wrapper
                        .css({opacity: 0, visibility: "visible"})
                        .animate({opacity: 1}, "slow");
                })

                // Load the original image if fail the cloud resource.
                .one('error', function() {
                    $(this).attr('src', _this.model.get('url'));
                });
            // adjust the size of the image.
            this.fix_image_size(main.$image, main.$wrapper, main.$container);
            // Show the box with the image.
            main.$container.fadeIn();
        }
    });


    function hide_image_zoomed() {
        main.$container.fadeOut(function() {
            main.$image.attr('src', '');

            // restore the spinner and container styles.
            main.$spinner.css('display', 'block');
            main.$item_wrapper.css('visibility', 'hidden');
        });
    }


    $(window).on('keydown', hide_image_zoomed);
    $('#full-size-box').on('click', hide_image_zoomed);

    /* CAVEAT: I set the __testmode___ enviroment variable to true in the test
    app. I do that because I don't need an instance of 
    main.ImageCollectionView during the testing. But I need that during the
    production. This is equivalent to *if __name__ == "__main__":* on python.
    */
    if (typeof jasmine === 'undefined') {
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
