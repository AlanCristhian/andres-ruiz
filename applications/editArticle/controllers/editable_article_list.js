(function($, Backbone, _, helpers, ArticleCollectionView, window, undefined) {
"use strict";


var main = window.main || {};


// ------------------
// Article item model
// ------------------

main.ArticleItemModel = Backbone.Model.extend({
    defaults: {
        title: ''
        ,cover_image: ''
        ,id: ''
        ,quality: null
        ,width: null
        ,shard: null
    }
});


// -----------------------
// Article list collection
// -----------------------

main.ArticleListCollection = Backbone.Collection.extend({
    url: helpers.set_path('/admin/get-list-of-articles')
    ,model: main.ArticleItemModel
});


// -----------------
// Article item view
// -----------------

main.ArticleItemView = Backbone.View.extend({
    // the DOM element is an **<li>** tag
    tagName: 'article'
    ,className: 'cover_article_item'
    ,template: _.template($('#articleTemplate').html())


    ,initialize: function() {
        // Bind the actual object with the 'render' event because first need
        // update the model and after need render this view. If not bind, this
        // could be raise some error because try to render the template before
        // finish update the model.
        _.bindAll(this, 'render');
        this.model.set({cid: this.model.cid});
        this.model.on('change', this.render);
    }

    ,render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        // Add the id attribute to the current dom elment because I need
        // remove this item to the DOM if the user want clear one article
        this.$el.attr('id', 'item_' + this.model.cid);
        // Return the actual instance of ArticleItemView
        // for use it after in the renderOne method of ArticleListView.
        return this;
    }

    ,events: function() {
        var _cid = this.model.cid,
            _events = {}
        _events['click #edit_' + _cid] = 'go_to_edit_page';
        _events['click #remove_' + _cid] = 'remove_article';
        return _events;
    }

    ,go_to_edit_page: function() {
        helpers.redirect('/' + this.model.get('edit_url'));
    }

    ,remove_article: function () {
        var _confirm = confirm(
            "¿Seguro que desea borrar el artículo **" +
            this.model.get('title') + "**?" +
            " Esta acción no se puede deshacer.");
        var remove_view,
            _cid = this.model.cid;
        remove_view = function(data) {
            // remove the current <li> item of the view
            $('#item_' + _cid).remove()
        }
        if (_confirm) {
            $.post(
                helpers.set_path('/admin/remove-article')
                ,this.model.toJSON()
                ,remove_view
            );
        }
    }

});


/* CAVEAT: I set the __testmode___ enviroment variable to true in the test
main. I do that because I don't need an instance of 
main.ImageCollectionView during the testing. But I need that during the
production. This is equivalent to *if __name__ == "__main__":* on python.
*/
if (typeof __testmode__ === 'undefined') {
    $(function() {
        main.articleListView = new ArticleCollectionView({
            Collection: main.ArticleListCollection,
            ModelView: main.ArticleItemView
        });
    });
}


// Expose main to the global object
window.main = main;

})(jQuery, Backbone, _, helpers, ArticleCollectionView, window);
