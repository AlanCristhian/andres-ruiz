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

/* CAVEAT: I set the __testmode___ enviroment variable to true in the test
app. I do that because I don't need an instance of 
main.ArticleCollectionView during the testing. But I need that during the
production. This is equivalent to *if __name__ == "__main__":* on python.
*/
if (typeof jasmine === 'undefined') {
    $(function() {
        main.article_collection_view = new ArticleCollectionView({
            Collection: main.ArticleCollection,
            ModelView: main.ArticleModelView
        });

        main.article_collection_view.before_render_all(function() {
             // Remove the included js file
             $('script[id=twitter-wjs]').remove();

            // Remove the timeline iframe
            $('iframe.twitter-timeline').remove();

            var $initial_content = $(
                main.article_collection_view.initial_content);
            $initial_content.find('a.twitter-timeline').attr('width',
                main.article_collection_view.breakpoints.width);
            console.log($initial_content.html());
        });
    });
}


// Expose main to the global object
window.main = main;
})(helpers, jQuery, _, Backbone, ArticleCollectionView, window);
