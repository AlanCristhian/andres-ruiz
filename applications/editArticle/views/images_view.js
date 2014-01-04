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


// -----------
// Image Model
// -----------

app.Image = Backbone.Model.extend({
    defaults: {
        url: ''
        ,description: ''
        ,article_name: app.articleInfo.get('article_name')
        ,status: ''
    }
});


// ----------------------------
// The view of individual image
// ----------------------------

app.SingleImageView = Backbone.View.extend({
    tagName: 'li',

    // Cache the template function for a single item
    template: _.template($('#item-template').html()),

    initialize: function() {
        // Bind the actual object with the 'render' event because first need
        // update the model and after need render this view. If not bind, this
        // could be raise some error because try to render the template before
        // finish update the model.
        _.bindAll(this, 'render');
        // Add the cid value to the model because this value is used to make
        // the id attribute in each DOM element.
        this.model.set({cid: this.model.cid})
        this.model.on('change', this.render);
    },

    // the DOM events specific to an item.
    events: function() {
        // The events key is an JSON object. But I need generate each key
        // dinamically with an unique id. To solve this i'm use the _result
        // var and add each key with the square bracket notation.
        var _cid = this.model.cid,
            _result = {};
        // make the name of id of the DOM element and bind a name of event handler
        _result['click #edit_image_description_' + _cid] = 'editImageDescription';
        _result['click #cancel_image_description_' + _cid] = 'cancelImageDescription';
        _result['click #save_image_description_' + _cid] = 'saveImageDescription';
        _result['click #false_image_send_' + _cid] = 'send_image';
        _result['click #remove_image_' + _cid] = 'remove_image';
        // _result[ + _cid] = '';
        return _result;        
    },

    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        // Add the id attribute to the current dom elment because I need
        // remove this item to the DOM if the user want clear one article.
        this.$el.attr('id', 'item_' + this.model.cid);
        // return the actual instance of ImageView
        // for use it then in ImagesViews.
        return this;
    },

    // Event handlers helpers
    swapVisibility: function(status) {
        // If satus is 'visible' hide the paragraph and show all components to
        // edit the current image model. Else if status is 'hidden' hide the 
        // components and show the paragraph.
        var _cid = this.model.cid;
        var status = status || 'hidden',
            $paragraph = $('#item_' + _cid + '>p'),
            $textarea = $('#item_' + _cid + '>textarea'),
            _buttons = _.template(
                '#item_{{cid}}>textarea,' + 
                '#item_{{cid}}>.save_image_description,' + 
                '#item_{{cid}}>.cancel_image_description'
            );
        var $buttons = $(_buttons({cid: _cid}));
        if (status === 'visible') {
            // show all components
            $textarea.css('display', 'block');
            $buttons.css('display', 'inline');
            // hide the paragraph
            $paragraph.css('display', 'none');
            // fill the textarea with the actual content
            $textarea.val(this.model.get('description'))
        } else if (status === 'hidden') {
            // hide all components
            $textarea.css('display', 'none');
            $buttons.css('display', 'none');
            // show the paragraph
            $paragraph.css('display', 'block');
        } else {
            console.error('The status value must be "visible" or "hidden".');
        }
    },

    // Event handlers
    editImageDescription: function() {
        this.swapVisibility('visible');
    },
    cancelImageDescription: function() {
        this.swapVisibility('hidden');
    },
    saveImageDescription: function() {
        // Set the content of textarea into description field
        // of the current model.
        this.model.set({
            description: $('#item_' + this.model.cid + '>textarea').val()
        });
        // Send the changes to the server.
        $.post(
            app.set_path('/admin/save-image-data')
            ,this.model.toJSON()
        );
        // I don't call the swapVisibility method as callback to the $.post
        // metod because this produce some namespace problem with the "this"
        // keyword.
        this.swapVisibility('hidden')
    },
    send_image: function() {
        var _cid = this.model.cid,
            that = this;
        var $image_send = $('#image_' + _cid);
        // trigger the click event on the **image_{{id}}** DOM elemnt
        $image_send.click();
        // the field that contains the buffer of the image has the same name
        // that the "name" atribure of the DOM elment "$image_send".
        $image_send.ajaxfileupload({
            'action': app.set_path('/admin/save-image')
            ,'params': {
                'cid': _cid
                // the object **app.editArticleInfo.model** is in 
                // "applications/editArticle/controllers/app.js"
                // was already loaded
                ,'id': app.editArticleInfo.model.get('id')
                ,'id_image': this.model.get('id')
            }
            ,onStart: function () {
                that.model.set({'status': 'enviando'});
            }
            ,onComplete: function(data) {
                // Update the url attribute into image. This update the view
                // with te new image.
                var jsonString = data.substring(
                    data.indexOf("{"), data.lastIndexOf("}") + 1);
                var jsonObject = JSON.parse(jsonString);
                that.model.set({
                    'url': jsonObject.url
                    ,'status': 'completado'
                });
            }
        });
    }
    ,remove_image: function() {
        var _confirm = confirm(
            "¿Seguro que desea borrar esta imagen?" +
            " Esta acción no se puede deshacer.");
        var remove_view,
            _cid = this.model.cid;
        remove_view = function(data) {
            // remove the current <li> item of the view
            $('#item_' + _cid).remove()
        }
        if (_confirm) {
            $.post(
                app.set_path('/admin/remove-image')
                ,this.model.toJSON()
                ,remove_view
            );
        }

    }
});


//------------------
// Image Collections
//------------------

app.ImageCollection = Backbone.Collection.extend({
    url: app.set_path('/admin/get-article-data')
    ,model: app.Image
});

app.ImageList = new app.ImageCollection();


// ----------------------
// The view of all images
// ----------------------

app.ImageListView = Backbone.View.extend({
    el: '#images-template',

    events: {
        'click #add-image': 'addImage'
    },

    initialize: function() {
        this.upgrade_all_data()
        // Bind the 'reset' event with the renderAll method for render
        // the collections.
        app.ImageList.on('reset', this.renderAll, this);
    },

    upgrade_all_data: function(callback) {
        // load all models
        app.ImageList.fetch({
            data: {
                edit_url: window.location.pathname,
                data_group: 'images'
            }
        });
    },

    renderOne: function(image) {
        // Add a single image item to the list creating a view for it, and
        // appending its element to the <ul>.
        var view = new app.SingleImageView({model: image});
        $('#image-list').append(view.render().el);
    },

    addImage: function() {
        // Add a single image item to the list creating a view for it, and
        // appending its element to the <ul>. 
        var image = new app.Image(),
            view = new app.SingleImageView({model: image});
        // Send the request to create a new image register into server.
        $.post(
            app.set_path('/admin/save-image-data')
            ,image.toJSON()
            // this callback update all data in the collection, then all
            // template is re-rendered.
            ,this.upgrade_all_data
        );
    },

    renderAll: function() {
        this.$('#image-list').html(''); // clear all items
        app.ImageList.each(this.renderOne, this); // add all items
    }
});

app.ImageListView = new app.ImageListView();