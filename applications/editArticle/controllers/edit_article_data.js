;(function(Backbone, _, helpers, global, undefined) {
"use strict";
var main = global.main || {};


main.ArticleDataModel = Backbone.Model.extend({
    url: helpers.set_path('/admin/get-article-data')
});


// A custom switch button
main.SwitcherButton = (function() {
    function __new__(options) {
        var defaults = {
                className: '.switcher_button',
                container: undefined,
                on: false
            }

        this.settings = $.extend({}, defaults, options);

        // chache all DOM elements
        this.$container = this.settings.container ||
            $(this.settings.className);
        this.$status = this.$container.find('.status')
        this.$switch_button = this.$container.find('.switch_button');
        this.$on_label = this.$container.find('.on_label');
        this.$off_label = this.$container.find('.off_label');
        this.$switch_slider = this.$container.find('.switch_slider');

        // cache all properties
        this._switch_button_width = this.$switch_button.outerWidth();
        this._container_width = this.$container.innerWidth();
        this._distance = this._container_width- this._switch_button_width;

        // Store a list of callback that will be
        // called after the animation ends
        this._click_callbacks = [];

        this.__init__();
    }

    __new__.prototype.__init__ = function() {
        var _this = this;
        this._set_default_state();
        this.$switch_button.on('click', function() {
            _this._switch_state();
        });
    }

    __new__.prototype.add_click_callback = function(callback) {
        this._click_callbacks.push(callback);
        return this;
    }

    __new__.prototype._set_default_state = function() {
        if (this.settings.on) {
            this.$switch_slider.css({
                left: 0
            });
        } else {
            this.$switch_slider.css({
                left: -this._distance + 'px'
            });
        }
    }

    __new__.prototype._switch_state = function() {
        var _this = this;

        this.settings.on = !this.settings.on;

        function __run_callbacks__() {
            _this._run_callbacks();
        }

        if (this.settings.on) {
            this.$switch_slider.animate({
                left: 0
            }, 'fast', __run_callbacks__);
        } else {
            this.$switch_slider.animate({
                left: -this._distance + 'px'
            }, 'fast', __run_callbacks__);
        }
    }

    // Call each callback in the callback_list argument
    __new__.prototype._run_callbacks = function() {
        if (typeof this._click_callbacks === 'undefined') {
            console.log(undefined);
            return;
        }
        var index = 0,
            amount = this._click_callbacks.length;
        if (amount) {
            for (index; index < amount; index++) {
                this._click_callbacks[index]();
            }
        }
    }

    return __new__;
})();


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

        // Listen for the change of the title field
        this.model.on('change:title', function() {
            $('h2').html(_this.model.get('title'));
        });

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

        var breakpoints = new helpers.Breakpoints(this.settings),
            _this = this;

        this.$el.css({
            width: breakpoints.width + 'px'
        });

        // cache all input fields
        this.$input_text = this.$el.find('input[type="text"]');
        this.$title = this.$el.find('#title');
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

        // set the switcher plugin
        this.article_visibility = new main.SwitcherButton({
            on: this.model.get('public'),
            element: this.$el.find('.switcher_button')
        });

        this.article_visibility.add_click_callback(function() {
            _this.model.set({'public': _this.article_visibility.settings.on});
            _this.save_info_fields();
        });

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
            ,title: this.$title.val()
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