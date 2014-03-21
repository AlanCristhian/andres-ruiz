;(function(global, $, Backbone, _, helpers, undefined) {
"use strict";
var main = global.main || {};


main.ARTICLE_NAME = helpers.get_article_name('/admin/editar');


main.MultimediaModel = Backbone.Model.extend({
    defaults: {
        url: ''
        ,description: ''
        ,article_name: main.ARTICLE_NAME
        ,type: 'image_file'
        ,cover: false
    }
});


// A child class of main ArticleDescriptionView. This will be a sub-view of
// the main.MultimediaView class.
main.ImageDescriptionView = main.ArticleDescriptionView.extend({
    tagName: 'div'
});

// The view of an individual multimedia.
main.MultimediaView = Backbone.View.extend({
    tagName: 'article'
    ,Model: main.MultimediaModel

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
            this.templateId = '#video_link_template';;
            this.className = '.video_link_container';
        } else if (typeof multimedia_type === 'undefined') {
            console.error('The type of the multimedia resource is undefined.');
        } else {
            console.error(multimedia_type + ' is an not valid value');
        }

        this.template = _.template($(this.templateId).html());
    }

    ,initialize: function() {

        // set a default model for testing
        if (typeof this.options.model === 'undefined') {
            this.model = new this.Model();
        }
        else {
            this.model = this.options.model;
        }

        this._set_template();

        // add the cid attibute to the model because this identify the field
        // name in the server side.
        this.model.set({cid: this.model.cid});
        this.model.on('change:type', this._set_template, this)
        this.model.on('change', this.render, this);

        // Create an sub-view of the image description
        this.description_view = new main.ImageDescriptionView({
            Model: this.ImageDescriptionModel
            ,model: this.model
            ,url_handler: '/admin/save-multimedia-data'
        });
    }

    ,render: function() {
        var _this = this,
            _data;
        this.$el
            .html(this.template(this.model.toJSON()))
            .attr('id', 'item_' + this.model.cid)
            // append the subview
            .append(this.description_view.render().el);

        // Show a flag if the current resurse is showed in the cover.
        if (this.model.get('cover')) {
            this.$el.find('.cover_wrapper .article_description_done')
                .css('display', 'inline-block');
        }

        // EVENTS AND HANDLERS FOR THE FILE THAT WAS UPLOADED

        // Define the data to be send.
        _data = {
            cid: this.model.cid

            // ???: the main.article_data_view.model object was defined in
            // applications/editArticle/controllers/edit_article_data.js
            ,id_article: main.article_data_view.model.get('id')
            ,id_image: this.model.get('id')
            ,type: 'image_file'
        };

        // cache the input file element
        this.$input_file = this.$el.find(':file');

        // Cache an deferred element from the file upload
        this.uploading_deferred = this.$input_file.fileupload({
            dataType: 'json'
            ,formData: _data
        });

        // add callbacs to the deferred fileupload element
        this.uploading_deferred

            // I call all callbaks inside the anonymous function
            // expression to solve some namespace problems.
            .bind('fileuploadstart', function(e, data) {
                _this._hide_status_flags()
                _this._show_progress_bar('.image_uploading_status');
            })
            .bind('fileuploadprogressall', function(e, data) {
                _this._update_progress_bar('.image_uploading_status', e, data);
            })
            .bind('fileuploadfail', function(e, data) {
                _this._show_error_flag('.image_uploading_status');
            })
            .bind('fileuploaddone', function(e, data) {
                //_this._update_image(e, data);

                // TODO: find a way to render the image without re-render
                // the description.
                _this.model.set({
                    url: data.result.url
                    ,type: data.result.type
                });
                _this._show_done_flag('.image_uploading_status');
            });

        // re-bind all event handlers in the subview.
        this.description_view.delegateEvents();

        return this;
    }

    ,events: {
        // the file uploading events and handler is defined in
        // the render method.
        'click .remove_image': 'remove_image'
        ,'mouseup .input_file': 'trigger_input_file_click'
        ,'click .input_link': 'add_image_link'
        ,'click .input_video': 'add_video_link'
        ,'click .cover_setter': 'set_as_cover'
    }

    ,remove_image: function() {
        var _confirm = confirm( "¿Seguro que desea borrar esta imagen?" +
                " Esta acción no se puede deshacer."),
            _this = this;

        // CAVEAT: I set the this.$el.remove() calling inside a named function
        // to prevent namespaces problems.
        function remove_image_view() {
            _this.$el.remove();
        }

        if (_confirm) {
            $.post(
                helpers.set_path('/admin/remove-multimedia')
                ,this.model.toJSON()
                ,remove_image_view
            );
        }
    }

    ,trigger_input_file_click: function() {
        this.$input_file.trigger('click');
        this._hide_status_flags();
        this._hide_form_elements();
    }

    ,_show_progress_bar: function(container) {
        this.$el
            .find(container + ' .article_description_uploading')
            .css('display', 'inline-block');
    }

    ,_update_progress_bar: function(container, e, data) {
        var progress = Math.round(data.loaded / data.total * 100);
        this.$el.find(container + ' .article_description_uploading .bar')
            .css('width', progress + '%');
    }

    ,_show_error_flag: function(container) {
        this.$el
            .find(container + ' .article_description_error')
                .css('display', 'inline-block');
        this.$el
            .find(container + ' .article_description_uploading')
                .css('display', 'none');
    }

    ,_show_done_flag: function(container) {
        this.$el
            .find(container + ' .article_description_done')
                .css('display', 'inline-block');
        this.$el
            .find(container + ' .article_description_uploading')
                .css('display', 'none');
    }
    ,_hide_form_elements: function() {
        this.$el.find('.input_link_field').css('display','none');
        this.$el.find('.cancel_input_link').css('display','none');
        this.$el.find('.accept_link_button').css('display','none');
    }

    ,_hide_status_flags: function(container) {
        this.$el.find(container + ' .article_description_status')
            .css('display', 'none');
    }

    ,add_multimedia_link: function(options) {
        var _this = this;
            options = options || {
                type: undefined
                ,className: undefined
            };

        // cache the DOM elements (for testing)
        // this._$input_link_button = this.$el.find('.input_link');
        this._$input_link_field = this.$el
            .find(options.className + ' .input_link_field');
        this._$cancel_input_link = this.$el
            .find(options.className + ' .cancel_input_link');
        this._$accept_link_button = this.$el
            .find(options.className + ' .accept_link_button');

        // show and enable the input[type="text"] field
        this._$input_link_field
            .prop('readonly', false)
            .css({
                'background-color': 'white'
                ,'border': '.1em solid lightgray'
                ,'display': 'inline-block'
            });

        // show the cancel button and add handler
        this._$cancel_input_link
            .css('display', 'inline-block')
            .on('click', function() {
                _this._$input_link_field
                    .prop('readonly', true)
                    .css({
                        'background-color': 'transparent'
                        ,'border': '.1em solid transparent'
                        ,'display': 'none'
                    });
                _this._hide_form_elements();
            });

        // show the accept button and add handler
        this._$accept_link_button
            .css('display', 'inline-block')
            .on('click', function() {
                _this._hide_form_elements();
                _this.add_multimedia_link_accept(options);
            });
    }

    ,add_multimedia_link_accept: function(options) {
        var _this = this,
            options = options || {
                type: undefined
                ,className: undefined
            }
            ,_url = _this.$el.find(options.className +
                ' .input_link_field').val()
            ,_multimedia_data;

        if (options.type == 'video_link') {
            var _video_url = global.document.createElement('a'),
                _vid;
                
            // make the vid attribute
            _video_url.href = _url;
            _vid = helpers.get_query_string(_video_url.search).v

            _multimedia_data = {
                id: this.model.get('id')
                ,url: _url
                ,vid: _vid
                ,type: options.type
            }            
        } else {
            _multimedia_data = {
                id: this.model.get('id')
                ,url: _url
                ,type: options.type
                ,article_name: main.ARTICLE_NAME
            }
        }

        this._show_progress_bar(options.className + ' .image_link_status');
        this.$el
            .find(options.className +
                ' .image_link_status .article_description_uploading')
                    .css('display', 'inline-block');
        
        this._deferred_image_link = $.post(
            helpers.set_path('/admin/save-multimedia-link')
            ,_multimedia_data
        );
        this._deferred_image_link
            .done(function() {
                var multimedia_type = _multimedia_data.type;
                // TODO: find a way to render the image without re-render
                // the description.
                if (multimedia_type == 'video_link') {
                    _this.model.set({
                        type: multimedia_type
                        ,vid: _multimedia_data.vid
                    });
                } else {
                    _this.model.set({
                        url: _multimedia_data.url
                        ,type: multimedia_type
                    });
                }

                _this._show_done_flag(options.className + ' .image_link_status');

            })
            .fail(function() {
                _this._show_error_flag(options.className + ' .image_link_status');
            });
    }

    ,add_image_link: function() {
        var container = '.image_wrapper';
        this._hide_status_flags(container);
        this._hide_form_elements();
        this.add_multimedia_link({
            type: 'image_link'
            ,className: container
        });
    }

    ,add_video_link: function() {
        var container = '.video_wrapper';
        this._hide_status_flags(container);
        this._hide_form_elements();
        this.add_multimedia_link({
            type: 'video_link'
            ,className: container
        });
    }

    ,set_as_cover: function() {
        var _this = this;

        this._cover_data =  {
            id: this.model.get('id')
            ,article_name: this.model.get('article_name')
            ,cover: true
        }
        this._set_cover_deferred = $.post(
            helpers.set_path('/admin/set-as-cover')
            ,this._cover_data
        );

        this._set_cover_deferred
            .done(function() {

                // hide the another cover flags in the document
                $('.cover_wrapper .article_description_done')
                    .css('display', 'none');
                _this._show_done_flag('.cover_wrapper' + ' .image_link_status');
            })
            .fail(function() {
                _this._show_error_flag('.cover_wrapper' + ' .image_link_status');
            });
    }

    // NOTE: 1: need investigate a way for update the image without re-render
    // the description. For now I re-render all to re-bind all events in
    // main.MultimediaView. For that reason I maintain the code below.
    /*
    ,_update_image: function(e, data) {
        this.$el
            .find('figure > img')
            .attr('src',
                'http://src' + this.model.get('shard') +
                '.sencha.io/jpg' + this.model.get('quality') + 
                '/' + this.model.get('width') + '/' +
                helpers.set_path(data.result.url));
    }
    */
});


main.ImageCollection = Backbone.Collection.extend({
    url: helpers.set_path('/admin/get-article-data')
    ,model: main.MultimediaModel
});


main.ImageCollectionView = Backbone.View.extend({
    tagName: 'article'
    ,id: 'new_multimedia_container'
    ,template: $('#new_multimedia_template').html()

    ,defaults: {
        ImageModel: main.MultimediaModel
        ,ImageView: main.MultimediaView
        ,ImageCollection: main.ImageCollection
        ,container: '#content'
    }

    ,initialize: function() {
        var _this = this;

        this.options = $.extend({}, this.defaults, this.options);
        this.shard_cycle = new helpers.Cycle(['', 1, 2, 3, 4]);

        this.settings_deferred = $.getJSON(
            helpers.set_path('applications/image_settings.json')
        );

        this.settings_deferred
            .done(function(data) {
                _this.settings = $.extend(
                    {}
                    ,data.defaults
                    ,data.edit_image
                );
            });

        this.collection = new this.options.ImageCollection();

        this.$container = $(this.options.container);
        this.$el.appendTo(this.$container);

        main.article_data_view.fetch_deferred.done(function() {
            _this.render();
        });

        this.collection
            .on('reset', this.add_shard_values, this)
            .on('reset', function() {
                main.article_data_view.fetch_deferred.done(function() {

                    // Ensure that all settings is loaded before call the 
                    // .render_all() method.
                    _this.settings_deferred.done(function(data) {
                        _this.render_all();
                    });
                });
            }, this)
            .fetch({
                data: {
                    edit_url: helpers.get_article_name()
                    ,data_group: 'multimedia'
                }
            });
    }

    ,render: function() {
        this.$el
            .detach()
            .appendTo(this.$container);
        this.$el.html(this.template);

        this.$add_multimedia_file = this.$el.find('#add_multimedia_file');

        var breakpoints = new helpers.Breakpoints(this.settings);
        this.$add_multimedia_file.css('width', breakpoints.width);

        return this;
    }

    ,render_one: function(multimedia_model) {
        var breakpoints = new helpers.Breakpoints(this.settings),
            image_view;
        multimedia_model.set({
            quality: breakpoints.settings.quality
            ,width: breakpoints.width
            ,height: Math.round(breakpoints.width/this.settings.ratio)
        });

        image_view = new this.options.ImageView({
            model: multimedia_model
            ,type: this.options.type
        });
        this.$container
            .append(image_view.render().el)
            .append(' ');
        this.fix_sizes(breakpoints);
        image_view.description_view.fix_textarea_size();
    }

    ,render_all: function() {
        this.$el.detach();
        this.collection.each(this.render_one, this);

        this.$el.appendTo(this.$container);
    }

    ,events: {
        'click #add_multimedia_file': 'add_multimedia_file'
    }

    ,add_multimedia_file: function() {
        var _this = this;

        // remove the edit buttons
        this.$el.detach();

        this._breakpoints = new helpers.Breakpoints(this.settings);
        this._multimedia_model = new this.options.ImageModel();

        // add shard value, quality and width
        this._multimedia_model.set({
            shard: this.shard_cycle.__next__()
            ,cid: this._multimedia_model.cid
            ,quality: this._breakpoints.settings.quality
            ,width: this._breakpoints.width
            ,height: Math.round(this._breakpoints.width/this.settings.ratio)
            ,type: 'image_link'
        });

        // Send the request to create a new image
        // register into server.
        this._deferred_multimedia_data = $.post(
            helpers.set_path('/admin/save-multimedia-data')
            ,_this._multimedia_model.toJSON()
            ,function(data) {
                _this._multimedia_model.set(data)
            }
        );

        this._image_view = new this.options.ImageView({
            model: this._multimedia_model
        });

        // add the view to the container
        this._$image_container = $(this._image_view
            .render(this._multimedia_model).el);
        this._$image_container.appendTo(this.$container);

        // create the input:file element
        this._$input_file = this._$image_container
            .find('[name="input_image_' + this._multimedia_model.cid + '"]');

        // append the form element
        this._$input_file.appendTo(this._$image_container);
        this.$container.append(' ');

        // add the edit buttons at the end of the container
        this.$el.appendTo(this.$container);
    }

    ,add_shard_values: function() {
        var _this = this;
        
        this.collection.each(function(multimedia_model) {
            multimedia_model.set({
                shard: _this.shard_cycle.__next__()
            });
        }, this);
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
});


if (typeof jasmine === 'undefined') {
    $(function() {
        main.multimedia_collection_view = new main.ImageCollectionView();
    });
}
global.main = main;
})(this, jQuery, Backbone, _, helpers);