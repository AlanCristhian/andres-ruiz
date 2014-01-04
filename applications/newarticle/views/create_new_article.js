var app = app || {};


// cache the constants
app.PROTOCOL = window.location.protocol;
app.HOSTNAME = window.location.hostname;


app.set_path = function (path) {
    // This function check the protocol. If the protocol is https then set the 
    // shared ssl username, else not change the path argument.
    return (app.PROTOCOL === 'https:') 
        ? '/~andresru' + path
        : path
}


app.redirect = function(location) {
    // Redirect to the correct location
    window.location = (app.PROTOCOL === 'https:') 
                      ? "https://" + app.HOSTNAME + "/~andresru" + location
                      : "http://" + app.HOSTNAME + location;
};


// ------------------
// Project data model
// ------------------

app.ProjectData = Backbone.Model.extend({
    url: app.set_path('/admin/new_article')
    ,defaults: {
        article_name: '',
        article_name_status: '',
        create_status: ''
    }
});

app.projectData = new app.ProjectData();


app.View = Backbone.View.extend({
    template: _.template($("#step1-template").html()),

    initialize: function () {
        this.render();
        _.bindAll(this, 'render');
        this.model.on('change', this.render);
    },

    render: function () {
        var content, context;
        context = this.model.toJSON();
        content = this.template(context);
        this.$el.html(content);
    },

    events: {
        'change #article_name': 'validate_article_name',
        'click #check_article_name': 'validate_article_name',
        'click #create': 'create_new_article'
    },

    validate_article_name: function () {
        var name, that;
        name = $('#article_name').val();
        that = this;


        if (name === '') {
            this.model.set({
                'article_name': name,
                'article_name_status': 'Debe rellenar este campo'
            });
            return false;
        } else {
            $.post(app.set_path('/admin/nuevo/validate_field'), {
                'article_name': name
            }, function (data) {
                if (data.exists) {
                    that.model.set({
                        'article_name': name,
                        'article_name_status': 'Ya existe un artículo con ese nombre. Elija otro.'
                    });
                    return true;
                } else {
                    that.model.set({
                        'article_name': name,
                        'article_name_status': 'Ok'
                    });
                    return false;
                }
            });
        }
    },

    create_new_article: function () {
        var name = $('#article_name').val(),
            that = this,
            callback;

        callback = function (data) {
            if (data.exists) {
                that.model.set({
                    'article_name': name,
                    'article_name_status': 'Ya existe un artículo con ese nombre. Elija otro.',
                    'create_status': 'Por favor, corrija los errores.'
                });
            } else if (data.status) {
                // go to edit page
                app.redirect('/' + data.edit_url)
            } else {
                that.model.set({
                    'article_name': name,
                    'article_name_status': '',
                    'create_status': 'Ha ocurrido un error durante la creación del artículo. Póngase en contacto con Alan Cristhian.'
                });
            }
        }

        if (name === '') {
            this.model.set({
                'article_name': name,
                'article_name_status': 'Debe rellenar este campo',
                'create_status': 'Por favor, corrija los errores.'
            });
            return false;
        }
        $.post(app.set_path('/admin/nuevo/create'), this.model.toJSON(), callback);
    }
});

app.form = new app.View({
    el: $('#step1-container'),
    model: app.projectData
});