;(function(Backbone, _, helpers, global, undefined) {
"use strict";
var main = global.main || {};


main.ArticleDataModel = Backbone.Model.extend({
    url: helpers.set_path('/admin/get-article-data')
});


main.ArticleDataView = Backbone.View.extend({
    tagName: 'article'
    ,id: 'article_data_container'
    ,template: _.template($('#article_data_template').html())
    ,defaults: {
        Model: main.ArticleDataModel
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

        this.model = new this.options.Model();

        this.model.on('change', function() {
            // Ensure that all settings is loaded before call the 
            // .render() method.
            _this.settings_deferred.done(function(data) {
                _this.render();
            });
        }, this);

        this.fetch_deferred = this.model.fetch({
            data: {
                edit_url: global.location.pathname,
                data_group: 'info'
            }
        });

        // set te template in the document
        this.$el
            .appendTo('#content')
            .after(' ');
    }

    ,render: function() {
        this.$el.html(this.template(this.model.toJSON()));

        var breakpoints = new helpers.Breakpoints(this.settings);
        this.$el.css({
            width: breakpoints.width + 'px'
        });

        // cache all input fields
        this.$input_text = this.$el.find('input[type="text"]');
        this.$classification = this.$el.find('#classification');
        this.$country = this.$el.find('#country');
        this.$state = this.$el.find('#state');
        this.$city = this.$el.find('#city');
        this.$autor = this.$el.find('#autor');
        this.$colaborators = this.$el.find('#colaborators');
        this.$project_date = this.$el.find('#project_date');

        // cache all buttons
        this.$edit_buttons = this.$el.find(
            '#save_article_data, #cancel_article_data'
        );
        this.$edit_article_data= this.$el.find('#edit_article_data');

        // cache status flags
        this.$article_data_status = this.$el.find(".article_data_status");
        this.$article_status_done = this.$el.find(".article_data_done");
        this.$article_status_error = this.$el.find(".article_data_error");
        this.$article_status_uploading = this.$el
            .find(".article_data_uploading");

        return this;
    }

    ,events: {
        'click #edit_article_data': 'show_info_and_buttons'
        ,'click #cancel_article_data': 'hide_info_and_buttons'
        ,'click #save_article_data': 'save_info_fields'
    }

    ,show_info_and_buttons: function() {
        this.$article_data_status.css('display', 'none');
        this.$edit_buttons.css('display', 'inline');
        this.$input_text
            .prop('readonly', false)
            .css({
                'background-color': 'white'
                ,'border': '.1em solid lightgray'
            });
        this.$edit_article_data.css('display', 'none');
    }

    ,hide_info_and_buttons: function() {
        this.$article_data_status.css('display', 'none');
        this.$edit_buttons.css('display', 'none');
        this.$input_text
            .prop('readonly', true)
            .css({
                'background-color': 'transparent'
                ,'border': '1px solid transparent'
            });
        this.$edit_article_data.css('display', 'inline');
    }

    ,save_info_fields: function () {
        var _this = this,
            deferred_post;

        this.$article_data_status.css('display', 'none');
        this.$article_status_uploading.css('display', 'inline-block');

        // update the local model
        this.model.set({
            classification: this.$classification.val()
            ,country: this.$country.val()
            ,state: this.$state.val()
            ,city: this.$city.val()
            ,autor: this.$autor.val()
            ,colaborators: this.$colaborators.val()
            ,project_date: this.$project_date.val()
        });

        // update the server model
        deferred_post = $.post(
            helpers.set_path('/admin/save-article-data')
            ,this.model.toJSON()
        );

        deferred_post
            .done(function() {
                _this.hide_info_and_buttons();
                _this.$article_status_done.css('display', 'inline-block');
            })
            .fail(function() {
                _this.hide_info_and_buttons();
                _this.$article_status_error.css('display', 'inline-block');
            });
    }
});


if (typeof jasmine === 'undefined') {
    $(function() {
        main.article_data_view = new main.ArticleDataView()
    });
}
global.main = main;
})(Backbone, _, helpers, window);