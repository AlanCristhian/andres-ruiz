describe("helpers.set_path", function() {
    beforeEach(function() {
        this.original_PROTOCOL = helpers._PROTOCOL;
        this.original_HOSTNAME = helpers._HOSTNAME;
        helpers._HOSTNAME = 'andres.dev';
    });

    afterEach(function() {
        helpers._PROTOCOL = this.original_PROTOCOL;
        helpers._HOSTNAME = this.original_HOSTNAME;
    });

    xit("should return the same if have the username", function() {
        expect(helpers.set_path('andres.dev/same/path'))
            .toBe('andres.dev/same/path');
    });

    xit("should");

    xit("Should add the ``shared ssl username`` to the\
            ``path`` if is HTTPS mode", function() {
        helpers._PROTOCOL = 'https:';
        expect(helpers.set_path('path'))
            .toBe(helpers._HOSTNAME + '/~andresru/path');
    });

    xit("Should return the same that ``path`` if not in HTTPS mode", function(){
        helpers._PROTOCOL = 'http:';
        expect(helpers.set_path('path')).toBe(helpers._HOSTNAME + '/path');
    });

    xit("should set the hostname if this isn't present in the path", function(){
        expect(helpers.set_path('/path')).toBe(helpers._HOSTNAME + '/path')
    });

    xit("should maintain the path if have any hostname", function() {
        expect(helpers.set_path('http://someting.com/path'))
            .toBe('http://someting.com/path');
    });

    xit("should add https protocol if the environ is in secure mode and" +
            " the path is in insecure mode", function() {
        helpers._PROTOCOL = 'https:';
        expect(helpers.set_path('http://someting.com/path'))
            .toBe('https://someting.com/path');
    });

    xit("shoud remove the initial bar if the protocol is present", function() {
        expect(helpers.set_path('/http://someting.com/path'))
            .toBe('http://someting.com/path');
    });
});


describe("helpers.redirect", function() {
    beforeEach(function() {
        this.original_PROTOCOL = helpers._PROTOCOL;
        this.original_HOSTNAME = helpers._HOSTNAME;
        helpers._HOSTNAME = 'domain.dev';
    });

    afterEach(function() {
        helpers._PROTOCOL = this.original_PROTOCOL;
        helpers._HOSTNAME = this.original_HOSTNAME;
    });

    it("Should add the ``https`` protocol, the ``shared ssl username`` and the\
            ``hostname`` to the ``path`` if is in HTTPS mode", function() {
        helpers._PROTOCOL = 'https:';
        helpers.redirect('path');
        expect(helpers._test_location)
            .toBe('https://domain.dev/~andresru/path');
    });

    it("Should add the ``http`` protocol and the ``hostname``tho the ``path``\
            argument if not in HTTPS mode", function() {
        helpers._PROTOCOL = 'http:';
        helpers.redirect('path');
        expect(helpers._test_location)
            .toBe('http://domain.dev/path');    
    });
});


describe('Breakpoints class deffinition', function() {
    beforeEach(function() {
        this.breakpoints = new helpers.Breakpoints();
    });

    it('Should be defined', function() {
        expect(helpers.Breakpoints).toBeDefined();
    });

    it('Shuld has a setting property', function() {
        expect(this.breakpoints.settings).toBeDefined();
    });

    it('Should has the viewport.width property', function() {
        expect(this.breakpoints.viewport.width).toBeDefined();
    });

    it('Should has the viewport.height property', function() {
        expect(this.breakpoints.viewport.width).toBeDefined();
    });

    it('Should has __init__ method', function() {
        expect(this.breakpoints.__init__).toBeDefined();
    });

    it('Shuld has the height property', function() {
        expect(this.breakpoints.height).toBeDefined();
    });

    it('Shuld has the width property', function() {
        expect(this.breakpoints.width).toBeDefined();
    });
});


describe('Image object spec', function() {
    beforeEach(function() {
        this.ratio = 1.7777777777777777;
        this.reduction = 0.4;
    });

    it('Should set the small height', function() {
        var viewport = {
                width: 360*this.ratio - 1,
                height: 360
            },
            breakpoints = new helpers.Breakpoints(undefined, viewport),
            _expected,
            _obtained;
        _obtained = breakpoints.height;
        _expected = breakpoints.settings.small * this.reduction
        expect(_expected - 0.1 < _obtained < _expected + 0.1).toBeTruthy();
        expect(breakpoints.size).toEqual(1);
    });

    it('Should set the small width', function() {
        var viewport = {
                width: 360*this.ratio,
                height: 360 + 1
            },
            breakpoints = new helpers.Breakpoints(undefined, viewport),
            _expected,
            _obtained;
        _obtained = breakpoints.width;
        _expected = breakpoints.settings.small*this.ratio*this.reduction;
        expect(!isNaN(_obtained)).toBeTruthy();
        expect(_expected - 0.1 < _obtained < _expected + 0.1).toBeTruthy();
        expect(breakpoints.size).toEqual(1);
    });

    it('Should set the medium height', function() {
        var viewport = {
                width: 480*this.ratio - 1,
                height: 480
            },
            breakpoints = new helpers.Breakpoints(undefined, viewport),
            _expected,
            _obtained;
        _obtained = breakpoints.height;
        _expected = breakpoints.settings.medium*this.reduction;
        expect(!isNaN(_obtained)).toBeTruthy();
        expect(_expected - 0.1 < _obtained < _expected + 0.1).toBeTruthy();
        expect(breakpoints.size).toEqual(2);
    });

    it('Should set the medium width', function() {
        var viewport = {
                width: 480*this.ratio,
                height: 480 + 1
            },
            breakpoints = new helpers.Breakpoints(undefined, viewport),
            _expected,
            _obtained;
        _obtained = breakpoints.width;
        _expected = breakpoints.settings.medium*this.reduction*this.ratio;
        expect(!isNaN(_obtained)).toBeTruthy();
        expect(_expected - 0.1 < _obtained < _expected + 0.1).toBeTruthy();
        expect(breakpoints.size).toEqual(2);
    });

    it('Should set the large height', function() {
        var viewport = {
                width: 720*this.ratio-1,
                height: 720
            },
            breakpoints = new helpers.Breakpoints(undefined, viewport),
            _obtained,
            _expected;
        _obtained = breakpoints.height;
        _expected = breakpoints.settings.large*this.reduction;
        expect(!isNaN(_obtained)).toBeTruthy();
        expect(_expected - 0.1 < _obtained < _expected + 0.1).toBeTruthy();
        expect(breakpoints.size).toEqual(3);
    });

    it('Should set the large width', function() {
        var viewport = {
                width: 720*this.ratio,
                height: 720 + 1
            },
            breakpoints = new helpers.Breakpoints(undefined, viewport),
            _obtained,
            _expected;
        _obtained = breakpoints.width;
        _expected = breakpoints.settings.large*this.ratio*this.reduction;
        expect(!isNaN(_obtained)).toBeTruthy();
        expect(_expected - 0.1 < _obtained < _expected + 0.1).toBeTruthy();
        expect(breakpoints.size).toEqual(3);
    });

    it('Should set the extralarge height', function() {
        var viewport = {
                width: 1080*this.ratio-1,
                height: 1080
            },
            breakpoints = new helpers.Breakpoints(undefined, viewport),
            _obtained,
            _expected;
        _obtained = breakpoints.height;
        _expected = breakpoints.settings.extralarge*this.reduction;
        expect(!isNaN(_obtained)).toBeTruthy();
        expect(_expected - 0.1 < _obtained < _expected + 0.1).toBeTruthy();
        expect(breakpoints.size).toEqual(4);
    });

    it('Should set the extralarge width', function() {
        var viewport = {
                width: 1080*this.ratio,
                height: 1080 + 1
            },
            breakpoints = new helpers.Breakpoints(undefined, viewport),
            _obtained,
            _expected;
        _obtained = breakpoints.width;
        _expected = breakpoints.settings.extralarge*this.reduction*this.ratio;
        expect(!isNaN(_obtained)).toBeTruthy();
        expect(_expected - 0.1 < _obtained < _expected + 0.1).toBeTruthy();
        expect(breakpoints.size).toEqual(4);
    });

    it('Should set the extralarge height if the viewport is major tan the ' +
            'max limit', function() {
        var viewport = {
                width: 1080*this.ratio+1,
                height: 1080
            },
            breakpoints = new helpers.Breakpoints(undefined, viewport),
            _obtained,
            _expected;
        _obtained = breakpoints.height;
        _expected = breakpoints.settings.extralarge*this.reduction;
        expect(!isNaN(_obtained)).toBeTruthy();
        expect(_expected - 0.1 < _obtained < _expected + 0.1).toBeTruthy();
        expect(breakpoints.size).toEqual(4);
    });

    it('Should set the extralarge width if the viewport is major tan the ' +
            'max limit', function() {
        var viewport = {
                width: 1080*this.ratio + 1,
                height: 1080 + 1
            },
            breakpoints = new helpers.Breakpoints(undefined, viewport),
            _obtained,
            _expected;
        _obtained = breakpoints.width;
        _expected = breakpoints.settings.extralarge*this.reduction*this.ratio;
        expect(!isNaN(_obtained)).toBeTruthy();
        expect(_expected - 0.1 < _obtained < _expected + 0.1).toBeTruthy();
        expect(breakpoints.size).toEqual(4);
    });
});


describe('Generator object', function() {
    beforeEach(function() {
        this.iterable = [1, 2, 3];
        this.cycle = new helpers.Cycle(this.iterable);
    });

    it('Should be defined', function() {
        expect(helpers.Cycle).toBeDefined();
    });

    it('Should have the next method', function() {
        expect(this.cycle.__next__).toBeDefined();
    });

    it('Should return the correct values', function() {
        var result = [];
        for (var i = 1; i <= 6; i++) {
            result.push(this.cycle.__next__());
        }
        expect(result).toEqual([1, 2, 3, 1, 2, 3]);
    });
});


describe('helpers.get_article_name', function() {
    it('Should remove the "proyectos" word of the url path name', function() {
        var _location = helpers.get_article_name('/proyectos/',
                '/proyectos/article');
        expect(_location).toBe('article');
    });

    it('Should remove the "~andresru/" word of the url path name', function() {
        var _location = helpers.get_article_name('/proyectos/',
                 '/~andresru/proyectos/article');
        expect(_location).toBe('article');
    });

    it('Should remove the "/" at the begin of the url path name', function() {
        var _location = helpers.get_article_name('/proyectos/', 'article');
        expect(_location).toBe('article');
    });

    it('Should remove the slash and if no arguments', function() {
        var _location = helpers.get_article_name('', '/proyectos/article');
        expect(_location).toBe('proyectos/article');
    });
});


describe('helpers.get_json_string()', function(){
    it('should remove the HTML tag info', function() {
        var result = helpers
            .get_json_string('<div>{"a": {"b": 1},"c": 2}</div');
        expect(result).toEqual('{"a": {"b": 1},"c": 2}');
    });
});


describe('helpers.get_query_string()', function() {
    it('?a=1', function() {
        var result = helpers.get_query_string('?a=1');
        expect(result).toEqual({a: '1'});
    });

    it('?a=1&b=2', function() {
        var result = helpers.get_query_string('?a=1&b=2');
        expect(result).toEqual({a: '1', b: '2'});
    });

    it('?a=1&jp=ほげ&en=Hoge', function() {
        var result = helpers.get_query_string('?a=1&jp=%E3%81%BB%E3%81%92&en=Hoge');
        expect(result).toEqual({a: '1', jp: 'ほげ', en: 'Hoge'});
    });

    it('?a=1&jp=%E3%81%BB%E3%81%92&en=Hoge', function() {
        var result = helpers.get_query_string('?a=1&jp=ほげ&en=Hoge');
        expect(result).toEqual({a: '1', jp: 'ほげ', en: 'Hoge'});
    });

    it('?a&b=2', function() {
        var result = helpers.get_query_string('?a&b=2');
        expect(result).toEqual({a: '', b: '2'});
    });

    it('', function() {
        var result = helpers.get_query_string('');
        expect(result).toEqual(undefined);
    });
});