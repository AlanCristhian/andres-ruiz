;(function(helpers, $, _, Backbone, window, undefined) {
    "use strict";


    window.ArticleCollectionView = Backbone.View.extend({
        defaults: {
            container: '#content',
        }

        ,initialize: function() {
            var _this = this;
            this.options = _.extend({}, this.defaults, this.options);

            this.shard_cycle = new helpers.Cycle(['', 1, 2, 3, 4]);
            //this.collection = new this.Collection();
            this.collection = new this.options.Collection();

            this.collection
                .on('reset', this.add_shard_values, this)
                .on('reset', this.render_all, this)
                .fetch();

            // cache the content selector
            this.container = this.options.container;

            // cache the content in this.container
            this.inicial_content = $(this.container).html();

            // load all settings of this article and set all event listeners
            $.ajax({
                dataType: 'json',
                url: helpers.set_path('applications/image_settings.json'),
                success: function(data) {
                    _this.settings = $.extend(
                        {},
                        data.defaults,
                        data.cover_image
                    );
                    _this.initialize_events();
                }
            });
        }

        ,initialize_events: function() {
            var _this = this,
                i = 1;

            // this variable is used as comparison point
            this.breakpoints = new helpers.Breakpoints(this.settings);

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

            $(window).on('resize', this.check_dimensions);
        }

        /* set the max size of each element */
        ,fix_sizes: function(breakpoints) {
            var max_width = breakpoints.width + 'px';

            $('article > figure > img').css({
                'max-width': max_width
            });
            $('article').css({
                'max-width': max_width
            });
        }

        ,check_dimensions: function() {
            var breakpoints = new helpers.Breakpoints(this.settings);

            // clear and render all document if the breakpoint is changed
            if (breakpoints.width !== this.breakpoints.width) {

                /* Change the model size only if the new size is larger
                tan the old size and only if the most large image isn't
                loaded */
                if (breakpoints.size > this.breakpoints.size
                && _.indexOf(this.max_size, breakpoints.size) === -1) {
                    this.max_size.push(breakpoints.size);
                    this.render_all();
                }
                this.fix_sizes(breakpoints);

                // update to the last breakpoint
                this.breakpoints = breakpoints;
            }
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
            var breakpoints = new helpers.Breakpoints(this.settings),
                $content = $(this.container);

            article_model.set({
                quality: breakpoints.settings.quality,
                width: breakpoints.width
            });

            var article_view = new this.options.ModelView({
                model: article_model
            });

            /* CAVEAT: agrego un espacio antes de añadir cada elemento
            <article> para que tengan una separación entre ellos. Hago esto
            porque cada <article> es tratado como una letra individual y si
            no les coloco el espacio se muestran pegados.
            */
            if ($content.html() === '') {
                $content.append(article_view.render().el);
            } else {
                $content
                    .append(article_view.render().el)
                    .append(" ");
            }

            this.fix_sizes(breakpoints);
        }

        /* Set all views in the DOM */
        ,render_all: function() {
            $(this.container).html('');
            if (typeof this.inicial_content !== 'undefined') {
                $(this.container).append(this.inicial_content)
            }
            this.collection.each(this.render_one, this);
        }
    });


})(helpers, jQuery, _, Backbone, window);
