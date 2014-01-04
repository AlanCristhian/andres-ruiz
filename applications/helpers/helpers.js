;console.error('This module is deprecated, use helpers2.js');

var app = app || {};


// cache the constants
app.PROTOCOL = window.location.protocol;
app.HOSTNAME = window.location.hostname;


/**
 * Checks the protocol. If the protocol is https then set the shared ssl
 * username, else not change the path argument.
 * @param {String} path is the url to normalize
 */
app.set_path = function(path) {
    return (app.PROTOCOL === 'https:') 
        ? '/~andresru' + path
        : path
};


/**
 * Redirect to the correct location.
 * @param  {String} location is the url where the user will be redirected
 */
app.redirect = function(location) {
    window.location = (app.PROTOCOL === 'https:') 
                      ? "https://" + app.HOSTNAME + "/~andresru" + location
                      : "http://" + app.HOSTNAME + location;
};
