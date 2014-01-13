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
            id: null,
            completed: false,
            quality: null,
            width: null,
            shard: null
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
        ,template: _.template($('#articleTemplate').html())

        ,render: function() {
            this.$el.html(this.template(this.model.toJSON()));

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
    if (typeof __testmode__ === 'undefined') {
        $(function() {
            main.article_collection_view = new ArticleCollectionView({
                Collection: main.ArticleCollection,
                ModelView: main.ArticleModelView
            });
        });
    }


    // Expose main to the global object
    window.main = main;
})(helpers, jQuery, _, Backbone, ArticleCollectionView, window);
