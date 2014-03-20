;(function($, Backbone, _, helpers, ArticleCollectionView, gobal, undefined) {
"use strict";


var main = gobal.main || {};


// ------------------
// Article item model
// ------------------

main.ArticleItemModel = Backbone.Model.extend({
    defaults: {
        title: ''
        ,cover_image: ''
        ,id: ''
        ,quality: ''
        ,width: ''
        ,height: ''
        ,shard: ''
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
    tagName: 'article'

    // Choose the correct template and className
    // depending on the type of media file
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
        var _this = this;

        // Bind the actual object with the 'render' event because first need
        // update the model and after need render this view. If not bind, this
        // could be raise some error because try to render the template before
        // finish update the model.
        _.bindAll(this, 'render');

        // Some templates use the cid field.
        this.model.set({
            cid: this.model.cid
        });
        this._set_template();
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


/* If the jasmine object is defined mean that this module is called for
testing. If not mean that is called for produccition. This is equivalent to
*if __name__ == "__main__":* on python.
*/
if (typeof jasmine === 'undefined') {
    $(function() {
        main.articleListView = new ArticleCollectionView({
            Collection: main.ArticleListCollection,
            ModelView: main.ArticleItemView
        });
    });
}


// Expose main to the global object
gobal.main = main;

})(jQuery, Backbone, _, helpers, ArticleCollectionView, window);
