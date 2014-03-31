;(function(helpers, $, _, Backbone, ArticleCollectionView, window, undefined) {
"use strict";


var main = window.main || {};


// ======
// Models
// ======

main.ArticleModel = Backbone.Model.extend({
    defaults: {
        title: '',
        description: '',
        url: '',
        cover_image: '',
        id: '',
        completed: false,
        quality: '',
        width: '',
        shard: ''
    }
});


// ===========
// Collections
// ===========

main.ArticleCollection = Backbone.Collection.extend({
    url: helpers.set_path('home/get_collection'),
    model: main.ArticleModel
});


// =====
// Views
// =====


main.ArticleModelView = Backbone.View.extend({
    tagName: 'article'
    ,className: 'cover_article_item'

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
        this.model.set({
            cid: this.model.cid
        });
        this._set_template();
    }

    ,render: function() {
        if (this.model.get('description')
        && this.model.get('cover_image')) {
            this.$el.html(this.template(this.model.toJSON()));
        }

        var _image = this.$el.find('img'),
            _item_container = this.$el
                .find('.article_item_container figure');

        return this;
    }

});


// Alow change the twitter settings dymanically
main.TwitterTimeline = (function() {
    var defaults = {
        script_id: 'twitter-wjs',
        container: undefined,
        widget_id: undefined,
        nick_name: undefined,
        height: '',
        width: '',
        theme: '',
        color: ''
    };

    function __new__(settings) {
        this.settings = $.extend({}, defaults, settings);
        this.$container = $(this.settings.container);
        this.__init__();
    }

    // Call the three function to make the twitter widget
    __new__.prototype.__init__ = function() {
        this._remove_twitter_timeline();
        this._add_twitter_timeline();
        this._load_twitter_timeline(
            document, "script", this.settings.script_id);
    }

    // Erase any trace of the twitter timeline
    __new__.prototype._remove_twitter_timeline = function() {

        // Remove the included js file
        $('script[id=' + this.settings.script_id + ']').remove();

        // Remove the timeline iframe
        $('iframe.twitter-timeline').remove();
    }

    // Create the anchor tag
    __new__.prototype._add_twitter_timeline = function() {
        var template = _.template(
                '<a class="twitter-timeline"'
                + ' width={{width}}'
                + ' height={{height}} data-theme={{theme}}'
                + ' data-link-color={{color}}'
                + ' href="https://twitter.com/{{nick_name}}"'
                + ' data-widget-id="{{widget_id}}">'
                + 'Tweets por &#64;{{nick_name}}</a>'
            ),
            a_tag = template(this.settings);
        this.$container.append(a_tag);
    }

    // this is de official function that generate the widget
    __new__.prototype._load_twitter_timeline = function (d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0],
            p = /^http:/.test(d.location) ? 'http' : 'https';
        if (!d.getElementById(id)) {
            js = d.createElement(s);
            js.id = id;
            js.src = p + "://platform.twitter.com/widgets.js";
            fjs.parentNode.insertBefore(js, fjs);
        }
    };

    return __new__;
})();


/* CAVEAT: I set the __testmode___ enviroment variable to true in the test
app. I do that because I don't need an instance of 
main.ArticleCollectionView during the testing. But I need that during the
production. This is equivalent to *if __name__ == "__main__":* on python.
*/
if (typeof jasmine === 'undefined') {
    $(function() {
        main.set_twitter_timeline = function() {
            var _size = main.article_collection_view.breakpoints.width;
            new main.TwitterTimeline({
                height: _size,
                width: _size,
                container: '#twitter_timeline_container',
                widget_id: '447407654080491521',
                nick_name: 'ruiz_andres'
            });
        }

        main.article_collection_view = new ArticleCollectionView({
            Collection: main.ArticleCollection,
            ModelView: main.ArticleModelView
        });

        main.article_collection_view.after_render_all(
            main.set_twitter_timeline);
    });
}


// Expose main to the global object
window.main = main;
})(helpers, jQuery, _, Backbone, ArticleCollectionView, window);
