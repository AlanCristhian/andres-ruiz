;(function($, Backbone, _, helpers, window, undefined) {
"use strict";
main = window.main || {};


main.ArticleDescriptionModel = Backbone.Model.extend({
    url: helpers.set_path('/admin/get-article-data')
});


main.ArticleDescriptionView = Backbone.View.extend({
    tagName: 'article'
    ,className: 'article_description_container'
    ,template: _.template($('#article_description_template').html())
    ,defaults: {
        Model: main.ArticleDescriptionModel
        ,url_handler: '/admin/save-article-data'
    }

    ,initialize: function() {
        var _this = this;

        this.options = _.extend({}, this.defaults, this.options);

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

        // instance the model
        this.model = this.options.model || new this.options.Model();
        this.model
            .on('change', function() {

                // Ensure that all settings is loaded before call the 
                // .render() method.
                _this.settings_deferred.done(function(data) {
                    _this.render();
                });
            }, this);

        // I don't fetch the model diretly because I need use this class
        // in the edit_article_image.js module
        if (typeof this.options.model === 'undefined') {
            this.model.fetch({
                data: {
                    edit_url: window.location.pathname,
                    data_group: 'description'
                }
            });
        }
    }

    ,render: function() {
        this.$el.html(this.template(this.model.toJSON()));

        this.$textarea_description = this.$el.find('.textarea_description');
        this.$article_description = this.$el.find('.description');

        // cache all buttons
        this.$edit_buttons = this.$el.find(
            '.save_article_description, .cancel_article_description');
        this.$edit_article_description = this.$el.find(
            '.edit_article_description');

        // cache status flags
        this.$article_description_status = this.$el.find(
            '.article_description_status');
        this.$article_description_done = this.$el
            .find(".article_description_done");
        this.$article_description_error = this.$el
            .find(".article_description_error");
        this.$article_description_uploading = this.$el
            .find(".article_description_uploading");

        this.fix_textarea_size();

        return this;
    }

    ,fix_textarea_size: function() {
        var breakpoints = new helpers.Breakpoints(this.settings);
        this.$textarea_description.css({
            'max-width': breakpoints.width -16 + 'px'
        });

        this.$article_description
            .height(this.$textarea_description.height())
            .width(this.$textarea_description.width());

        return this;
    }

    ,events: {
        'click .edit_article_description': 'show_info_and_buttons'
        ,'click .cancel_article_description': 'hide_info_and_buttons'
        ,'click .save_article_description': 'save_description'
    }

    ,show_info_and_buttons: function() {
        this.$article_description_status.css('display', 'none');
        this.$edit_buttons.css('display', 'inline');
        this.$article_description
            .prop('readonly', false)
            .css({
                'background-color': 'white'
                ,'border': '.1em solid lightgray'
            });
        this.$edit_article_description.css('display', 'none');
    }

    ,hide_info_and_buttons: function() {
        this.$article_description_status.css('display', 'none');
        this.$edit_buttons.css('display', 'none');
        this.$article_description
            .prop('readonly', true)
            .css({
                'background-color': 'transparent'
                ,'border': '1px solid transparent'
            });
        this.$edit_article_description.css('display', 'inline');
    }

    ,save_description: function() {
        var _this = this,
            deferred_post;

        this.$article_description_status.css('display', 'none');
        this.$article_description_uploading.css('display', 'inline-block');

        // update the local model
        this.model.set('description', this.$article_description.val());

        // update the server model
        deferred_post = $.post(
            helpers.set_path(this.options.url_handler)
            ,this.model.toJSON()
        );

        deferred_post
            .done(function() {
                _this.hide_info_and_buttons();
                _this.$article_description_done.css('display', 'inline-block');
            })
            .fail(function() {
                _this.hide_info_and_buttons();
                _this.$article_description_error
                    .css('display', 'inline-block');
            });
    }
});


if (typeof jasmine === 'undefined') {
    $(function() {
        main.article_desc_view = new main.ArticleDescriptionView();
        // set te view in the document
        main.article_desc_view.$el
            .appendTo('#content')
            .after(' ');
    });
}
window.main = main;
})(jQuery, Backbone, _, helpers, window);