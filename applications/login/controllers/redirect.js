var app = app || {};

app.PROTOCOL = window.location.protocol;
app.HOSTNAME = window.location.hostname;

var redirect = function(location) {
    window.location = (app.PROTOCOL === 'https:') 
                      ? "https://" + app.HOSTNAME + "/~andresru" + location
                      : "http://" + app.HOSTNAME + location;
};

setTimeout(redirect('/admin/home'), 1000);
