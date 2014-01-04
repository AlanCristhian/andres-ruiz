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
// Article data Model
// ------------------

app.ArticleInfo = Backbone.Model.extend({
    url: app.set_path('/admin/get-article-data')
});

app.articleInfo = new app.ArticleInfo();


// -----------------
// Article data view
// -----------------

app.ArticleInfoView = Backbone.View.extend({

    template: _.template($('#info-template').html()),

    initialize: function () {
        _.bindAll(this, 'render');
        this.model.on('change', this.render);
        this.model.fetch({
            data: {
                edit_url: window.location.pathname,
                data_group: 'info'
            },
            async: false
        });
    },

    render: function () {
        var content, context;
        context = this.model.toJSON();
        content = this.template(context);
        this.$el.html(content);
    },

    events: {
        'click #info #edit_info': 'showInfoFields'
    },

    hideInfoFields: function () {
        $('#info>input[type="text"], #info>#save, #info>#cancel')
            .css('display', 'none');
        $('#info>span').css('display', 'inline');
    },

    showInfoFields: function () {
        var self = this;
        $('#info>input[type="text"], #info>#save, #info>#cancel')
            .css('display', 'inline');
        $('#info>span').css('display', 'none');
        $('#info #cancel').on('click', this.hideInfoFields);
        $('#info #save').on('click', function () {
            self.model.set({
                'classification': $('#classification').val(),
                'country': $('#country').val(),
                'state': $('#state').val(),
                'city': $('#city').val(),
                'autor': $('#autor').val(),
                'colaborators': $('#colaborators').val(),   
                'project_date': $('#date').val()
            });
            $.post(
                app.set_path('/admin/save-article-data')
                ,self.model.toJSON()
                ,self.hideInfoFields
            );
        });
    }
});

app.editArticleInfo = new app.ArticleInfoView({
    'el': $('#info-container'),
    'model': app.articleInfo
});


// ------------------------
// Article descripion Model
// ------------------------

app.ArticleDescription = Backbone.Model.extend({
    url: app.set_path('/admin/get-article-data')
});

app.articleDescription = new app.ArticleDescription();


// ------------------------
// Article description View
// ------------------------

app.ArticleDescriptionView = Backbone.View.extend({
    template: _.template($('#description-template').html()),
    initialize: function () {
        _.bindAll(this, 'render');
        this.model.on('change', this.render);
        this.model.fetch({
            data: {
                edit_url: window.location.pathname,
                data_group: 'description'
            }
        });
        this.$description = $('#description')
    },

    render: function () {
        var content, context;
        context = this.model.toJSON();
        content = this.template(context);
        this.$el.html(content);
    },

    events: {
        'click #edit_description': 'sowDescriptionFields'
    },

    hideDescriptionFields: function () {
        $('#description-article pre').css('display', 'block');
        $('#description, #save_description, #cancel_description')
            .css('display', 'none');
    },

    sowDescriptionFields: function () {
        var self = this,
            $description = $('#description');
        $('#description-article pre').css('display', 'none');
        $description
            .css('display', 'block')
            .val(this.model.get('description'));
        $('#save_description, #cancel_description').css('display', 'inline');
        $('#cancel_description').on('click', this.hideDescriptionFields);
        $('#save_description').on('click', function () {
            self.model.set('description', $description.val());
            $.post(
                app.set_path('/admin/save-article-data')
                ,self.model.toJSON()
                ,self.hideInfoFields
            );
        });
    }
});

app.editArticleDescription = new app.ArticleDescriptionView({
    'el': $('#description-container'),
    'model': app.articleDescription
});