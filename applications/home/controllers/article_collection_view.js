;(function(helpers, $, _, Backbone, window, undefined) {
    "use strict";


    window.ArticleCollectionView = Backbone.View.extend({
        defaults: {
            container: '#content'
            ,element_space: 48
        }

        ,initialize: function() {
            var _this = this;

            // load all settings of this article
            this.settings_deferred = $.getJSON(
                helpers.set_path('applications/image_settings.json')
            );

            this.settings_deferred
                .done(function(data) {
                    _this.settings = $.extend(
                        {},
                        data.defaults,
                        data.cover_image
                    );
                })
                .always(function() {
                    // CAVEAT: don't pass the .initialize_events() method
                    // directly to prevent some namespace bugs.
                    _this.initialize_events();
                });

            this.options = _.extend({}, this.defaults, this.options);

            this.shard_cycle = new helpers.Cycle(['', 1, 2, 3, 4]);
            this.collection = new this.options.Collection();

            this.collection
                .on('reset', this.add_shard_values, this)
                .on('reset', function() {
                    // Ensure that all settings is loaded before call the 
                    // .render_all() method.
                    _this.settings_deferred.done(function(data){
                        _this.render_all();
                    });
                }, this)
                .fetch();

            // cache the content selector
            this.container = this.options.container;
            this.$container = $(this.container);

            // cache the content in this.container
            this.initial_content = this.$container.html();
        }

        ,initialize_events: function() {
            var _this = this,
                i = 1;

            // this variable is used as comparison point
            this.breakpoints = new helpers.Breakpoints(this.settings);
            this._current_width = this.breakpoints.width;

            // This propertie store all sizes loaded
            this.max_size = [];

            /* Marco el tamaño inicial como cargado. También marco como
            cargados todos los tamaños menores que el inicial. Hago esto
            porque si ya cargó una imagen grande, no necesita cargar las
            imágenes chiquitas porque la imágen no pierde calidad al
            achicarse. */
            for (i; i <= this.breakpoints.size; i++) {
                this.max_size.push(i);
            }


            /* CAVEAT: defino una función anónima en el event handler porque
            si la defino como método de la clase Backbone.View me da problemas
            con el valor de la variable this. */
            $(window).on('resize', function() {
                var breakpoints = new helpers.Breakpoints(_this.settings);

                // clear and render all document if the breakpoint is changed
                if (breakpoints.width !== _this.breakpoints.width) {

                    /* Change the model size only if the new size is larger
                    tan the old size and only if the most large image isn't
                    loaded */
                    /*
                    if (breakpoints.size > _this.breakpoints.size
                    && _.indexOf(_this.max_size, breakpoints.size) === -1) {
                        _this.max_size.push(breakpoints.size);
                        _this.render_all();
                    }
                    */
                    _this.render_all();
                    _this.fix_sizes(breakpoints);

                    // update to the last breakpoint
                    _this.breakpoints = breakpoints;
                    _this._current_width = _this.breakpoints.width;
                }
            });
        }


        // Calculates the number of columns to fit in the container
        ,_get_columns_amount: function() {
            var container_width = this.$container.width(),
                _columns = Math.round(container_width / this._current_width),
                total_width = _columns*this._current_width
                    + this.options.element_space*(_columns - 1);

                if (container_width >= total_width) {
                    return _columns;
                } else if (container_width < total_width) {
                    return (_columns > 1) ? (_columns - 1) : 1;
                } else {
                    return 1;
                }
        }


        /* set the max size of each element */
        ,fix_sizes: function(breakpoints) {
            var max_width = breakpoints.width + 'px';

            $('article > figure > img').css({
                'max-width': max_width
            });
            $('.column').css({
                'max-width': max_width
            });
        }

        ,add_shard_values: function() {
            var _this = this;
            
            this.collection.each(function(article_model) {
                article_model.set({
                    shard: _this.shard_cycle.__next__()
                });
            }, this);
        }

        /* Set an individual model view in the DOM */
        ,render_one: function(article_model) {

            // get an object with the correct dimensions
            var breakpoints = new helpers.Breakpoints(this.settings);

            article_model.set({
                quality: breakpoints.settings.quality,
                width: breakpoints.width,
                height: Math.round(breakpoints.width/this.settings.ratio)
            });

            var article_view = new this.options.ModelView({
                model: article_model
            });

            $('#hidden_container').append(article_view.render().el);

            this.fix_sizes(breakpoints);
        }

        /* Set all views in the DOM */
        ,render_all: function() {
            var columns = this._get_columns_amount(),
                index = 0,
                breakpoints = new helpers.Breakpoints(this.settings),
                $columns;

            // remove all elements
            this.$container.html('');

            // create and append the all columns
            for (index; index < columns; ++index) {

                $('<div>', {
                    id: 'column' + index
                    ,class: 'column'
                })
                    .css('max-width', breakpoints.width + 'px')
                    .appendTo(this.container)
                    .after(' ');
            };

            if (typeof this.initial_content !== 'undefined') {
                $('#column0').append($(this.initial_content));
            }
            this.collection.each(this.render_one, this);

            // place all articles in the columns
            $columns = $('.column');

            // find all articles hidden
            $('#hidden_container article').each(function(index) {
                var $this = $(this),
                    _height,
                    _item_id;

                // find the image of each article
                $this.find('img')
                    .sizeloaded()
                    .on('sizeloaded', function() {

                        // find the most lower column
                        $columns.each(function(index) {
                            var $this = $(this),
                                _l_height = $this.height();

                            if (_height === undefined) {
                                _height = _l_height;
                                _item_id = $this.attr('id');
                            } else if (_l_height < _height) {
                                _height = _l_height;
                                _item_id = $this.attr('id');
                            }
                        });

                        // move the article to the most lower column
                        $this
                            .detach()
                            .appendTo($('#' + _item_id))
                            // show the content
                            .find('.article_item_container figure')
                                .css({opacity: 0, visibility: "visible"})
                                .animate({ opacity:1 }, "slow");
                    })

                    // Load the original image if fail the cloud resource.
                    .on('error', function() {
                        var _$this = $(this),
                            _src = _$this.attr('src'),
                            _array = _src.split('http:'),

                            // The last item of the array is the path of the 
                            // original image.
                            _original = _array[_array.length - 1];
                        _$this.attr('src', _original);
                    });

                // find the iframe of each article
                $this.find('iframe')
                    // I use "one" instead "on" to avoid a blink effect
                    .one('load', function() {

                        // find the most lower column
                        $columns.each(function(index) {
                            var $this = $(this),
                                _l_height = $this.height();

                            if (_height === undefined) {
                                _height = _l_height;
                                _item_id = $this.attr('id');
                            } else if (_l_height < _height) {
                                _height = _l_height;
                                _item_id = $this.attr('id');
                            }
                        });

                        // move the article to the most lower column
                        $this
                            .detach()
                            .appendTo($('#' + _item_id))
                            // show the video
                            .css({opacity: 1, visibility: "visible"})
                            .animate({ opacity:1 }, "slow")
                            .find('.article_item_container figure')
                                // show the buttons
                                .css({opacity: 0, visibility: "visible"})
                                .animate({ opacity:1 }, "slow");
                    });
                
            });

        }
    });


})(helpers, jQuery, _, Backbone, window);
