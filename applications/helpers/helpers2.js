;(function($, window, undefined) {
    "use strict";


    var previousHelpers = window.helpers,
        helpers = {};


    // cache the constants
    helpers._PROTOCOL = window.location.protocol.toLowerCase();
    helpers._HOSTNAME = window.location.hostname.toLowerCase();


    /**
     * Checks the protocol. If the protocol is https then set the shared ssl
     * username, else not change the path argument.
     * @param {String} path is the url to normalize
     */
    helpers.set_path = function(path) {
        /*
        var parser = document.createElement('a');
        parser.href = path;
        return parser.href;
        */

        // normalize the path
        if (path[0] !== '/') {
            path = '/' + path;
        }
        return (helpers._PROTOCOL === 'https:')
            ? '/~andresru' + path
            : path
    };


    /**
     * Redirect to the correct location.
     * @param  {String} location is the url where the user will be redirected
     */
    helpers.redirect = function(location) {

        // normalize the location
        if (location[0] !== '/') {
            location = '/' + location;
        }
        // the _test_location property alow me test this function.
        var _location = (helpers._PROTOCOL === 'https:')
            ? "https://" + helpers._HOSTNAME + "/~andresru" + location
            : "http://" + helpers._HOSTNAME + location;
        if (typeof jasmine === 'undefined') {
            window.location = _location;
        } else {
            helpers._test_location = _location;
        }
    };


    helpers.Breakpoints = (function() {
        var defaults = {
            small: 360,
            medium: 480,
            large: 720,
            extralarge: 1080,
            quality: 90,
            ratio: 1.7777777777777777,
            reduction: 0.4
        };

        /* Make a object with responsive dimensions */
        function __new__(settings, viewport) {
            var $window = $(window);
            this.settings = $.extend({}, defaults, settings);

            // store the window size
            this.viewport = viewport || {
                width: $window.outerWidth(true),
                height: $window.outerHeight(true)
            };
            this.__init__();
        };

        // Set the correct dimensions to the element
        __new__.prototype.__init__ = function() {
            var viewport_height = this.viewport.height,
                viewport_width = this.viewport.width,
                reduction = this.settings.reduction,
                ratio = this.settings.ratio;

            // small
            if (
                (viewport_height <= this.settings.small
                || viewport_width <= this.settings.small*ratio)
            ) {
                this.height = Math.round(this.settings.small*reduction);
                this.width = Math.round(this.settings.small*ratio*reduction);
                this.size = 1;

            // medium
            } else if (
                (this.settings.small < viewport_height 
                && viewport_height <= this.settings.medium)
                || (this.settings.small*ratio < viewport_width
                && viewport_width <= this.settings.medium*ratio)
            ) {
                this.width = Math.round(this.settings.medium*ratio*reduction);
                this.height = Math.round(this.settings.medium*reduction);
                this.size = 2;

            // large
            } else if (
                (this.settings.medium < viewport_height
                && viewport_height <= this.settings.large)
                || (this.settings.medium*ratio < viewport_width
                && viewport_width <= this.settings.large*ratio)
            ) {
                this.width = Math.round(this.settings.large*ratio*reduction);
                this.height = Math.round(this.settings.large*reduction);
                this.size = 3;

            // extralarge
            } else if (
                (this.settings.large < viewport_height)
                || (this.settings.large*ratio < viewport_width)
            ) {
                this.width = Math.round(this.settings.extralarge*ratio*reduction);
                this.height = Math.round(this.settings.extralarge*reduction);
                this.size = 4;
            }
        };

        return __new__;
    })();


    /* Make an iterator returning elements from the iterable and saving a copy
    of each. When the iterable is exhausted, return elements from the saved
    copy. Repeats indefinitely. */
    helpers.Cycle = (function() {

        // The object constructor.
        function __new__(iterable) {
            this.iterable = iterable;
            this._LENGTH = iterable.length - 1
            this._index = -1;
        }

        // Return the next item from the iterator.
        __new__.prototype.__next__ = function() {
            if (this._index < this._LENGTH ) {
                this._index++;
            } else {
                this._index = 0;
            }
            return this.iterable[this._index];
        }

        return __new__;
    })();


    // return the article name from the url
    helpers.get_article_name = function(category, pathname) {
        var pathname = pathname || window.location.pathname;

        pathname = pathname.replace(category, '').replace('~andresru/', '');

        // normalize the path
        if (pathname[0] === '/') {
            pathname = pathname.substr(1);
        }
        return pathname;
    }


    // Extract the json string from the HTML tag
    helpers.get_json_string = function(data) {
        return data.substring(data.indexOf("{"), data.lastIndexOf("}") + 1);
    }

    // Turning the Querystring into a JSON object
    helpers.get_query_string = function(search) {
        var query = search || window.location.search,
            pairs;

        if (!query) {
            return undefined;
        }

        pairs = query.slice(1).split('&');

        var result = {};
        pairs.forEach(function(pair) {
            pair = pair.split('=');
            result[pair[0]] = decodeURIComponent(pair[1] || '');
        });

        return JSON.parse(JSON.stringify(result));
    }

    helpers.noConflict = function() {
        window.helpers = previousHelpers;
        return helpers;
    }


    // Expose helpers to the global object
    window.helpers = helpers
})(jQuery, window);
