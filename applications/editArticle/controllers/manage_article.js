var app = app || {};


// cache the constants
app.PROTOCOL = window.location.protocol;


app.set_path = function (path) {
    // This function check the protocol. If the protocol is https then set the 
    // shared ssl username, else not change the path argument.
    return (app.PROTOCOL === 'https:') 
        ? '/~andresru' + path
        : path
}

// ------------------
// Article item model
// ------------------

app.ArticleItemModel = Backbone.Model.extend({
    defaults: {
        title: ''
        ,cover_image: ''
        ,id: ''
    }
});


// -----------------
// Article item view
// -----------------

app.ArticleItemView = Backbone.View.extend({
    // the DOM element is an **<li>** tag
    tagName: 'li'

    // Cache the template for the single item
    ,template: _.template($('#article-template').html())

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
        window.location = window.location.protocol + '//' +
            window.location.hostname +
            app.set_path('/' + this.model.get('edit_url'));
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
                app.set_path('/admin/remove-article')
                ,this.model.toJSON()
                ,remove_view
            );
        }
    }
});


// -----------------------
// Article list collection
// -----------------------

app.ArticleListCollection = Backbone.Collection.extend({
    // the url associate to the handler that send a lis of articles
    url: app.set_path('/admin/get-list-of-articles')
    ,model: app.ArticleItemModel
});

app.articleList = new app.ArticleListCollection();


// -----------------
// Article list view
// -----------------

app.ArticleListView = Backbone.View.extend({
    // this is the container of all **app.ArticleItemView**. Remember that
    // the DOM element of **app.ArticleItemView** is the **<li>** tag.
    el: '#article-list-container'

    ,initialize: function() {
        // the **app.articleList** object is an instance of 
        // **app.ArticleListCollection** and was created before.
        // Get the list of articles
        app.articleList.fetch();
        app.articleList.on('reset', this.renderAll, this);
    }

    ,renderOne: function(article) {
        // render a single item
        var view = new app.ArticleItemView({model: article});
        $('#article-list').append(view.render().el);
    }

    ,renderAll: function() {
        // render all items
        this.$('#article-list').html(''); // clear all existent items
        app.articleList.each(this.renderOne, this); // render all items
    }
});

app.articleListView = new app.ArticleListView();
