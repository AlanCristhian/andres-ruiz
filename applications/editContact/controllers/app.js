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


// -----------------------------
// The model of the contact data
// -----------------------------

app.ContactInfoModel = Backbone.Model.extend({
    url: app.set_path('/admin/get-contact-info')
});

app.contactInfo = new app.ContactInfoModel();


// ---------------------------------
// The view of the contact info data
// ---------------------------------

app.ContactInfoView = Backbone.View.extend({

    template: _.template($("#field-template").html()),

    initialize: function () {
        _.bindAll(this, 'render');
        this.model.on('change', this.render);
        this.model.fetch();
    },

    render: function () {
        var content, context;
        context = this.model.toJSON();
        content = this.template(context);
        this.$el.html(content);
    },

    events: {
        'change #address': 'updateAddress',
        'change #email': 'updateEmail',
        'change #facebook': 'updateFacebook',
        'change #twitter': 'updateTwitter',
        'change #pinterest': 'updatePinterest',
        'change #telephone': 'updateTelephone',
        'change #mobile': 'updateMobile',
        'click #update': 'updateModel'
    },

    updateStatus: function (status) {
        status = status || 'Los datos han cambiado';
        $('#status').text(status);
    },

    updateAddress: function () {
        this.model.set({
            address: $('#address').val()
        });
        this.updateStatus();
    },

    updateEmail: function () {
        this.model.set({
            email: $('#email').val()
        });
        this.updateStatus();
    },

    updateFacebook: function () {
        this.model.set({
            facebook: $('#facebook').val()
        });
        this.updateStatus();
    },

    updateTwitter: function () {
        this.model.set({
            twitter: $('#twitter').val()
        });
        this.updateStatus();
    },

    updatePinterest: function () {
        this.model.set({
            pinterest: $('#pinterest').val()
        });
        this.updateStatus();
    },

    updateTelephone: function () {
        this.model.set({
            telephone: $('#telephone').val()
        });
        this.updateStatus();
    },

    updateMobile: function () {
        this.model.set({
            mobile: $('#mobile').val()
        });
        this.updateStatus();
    },

    updateModel: function () {
        var self = this;
        $.get(app.set_path('/admin/update-contact-info')
            ,this.model.toJSON(), function () {
            self.updateStatus('Los datos han sido guardados.');
        });
    }
});

app.form = new app.ContactInfoView({
    el: $('#fields-container'),
    model: app.contactInfo
});