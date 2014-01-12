describe('Test for ArticleCollectionView', function() {
    var collection_example = [{
        title: 'Test 1',
        description: 'First description.',
        ulr: 'test-1',
        cover_image: 'path/to/image-1.jpg',
        id: 1,
        completed: false
    }, {
        title: 'Test 2',
        description: 'Second description.',
        ulr: 'test-2',
        cover_image: 'path/to/image-2.jpg',
        id: 2,
        completed: false
    }];

    beforeEach(function() {
        setFixtures('<section id="content"></section>');
        //this.article_view_collection = new main.ArticleCollectionView();
        this.article_view_collection = new ArticleCollectionView({
            Collection: main.ArticleCollection,
            ModelView: main.ArticleModelView
        });

        // store a flag property to test asyncronous tasks
        this.flag = false;
    });

    it('Should exist the #content DOM element', function() {
        expect($('section#content')).toExist();
    });

    it('Should has the shard_cycle generator', function() {
        expect(this.article_view_collection.shard_cycle).toBeDefined();
    });

    it('main.shard_cycle should has the [1, 2, 3, 4] in the iterable property',
            function() {
        expect(this.article_view_collection.shard_cycle.iterable)
        	.toEqual(['', 1, 2, 3, 4]);
    });

    it('Should has article_collection property', function() {
        expect(this.article_view_collection.collection).toBeDefined();
    });

    // TODO: need implementation.
    xit('Should add one <article>', function() {
        console.warn('Not yet implemented.');
    });

    // TODO: need implementation.
    xit('Should add one space before the <article>', function() {
        console.warn('Not yet implemented.');
    });

    // TODO: need implementation.
    xit('Should add the shard value to all models', function() {
        console.warn('Not yet implemented.');
    });

    it('Should has the container property', function() {
        expect(this.article_view_collection.container).toBe('#content');
    });

    it('Should has the inicial_content property', function() {
        expect(this.article_view_collection.inicial_content).toBeDefined();
    });

    it('Should has the .element_space property', function() {
        expect(this.article_view_collection.options.element_space)
            .toBeDefined();
    });

    it('Should has the ._current_width property', function() {
        var _this = this;

        this.article_view_collection.settings_deferred.always(function() {
            _this.flag = true;
        });

        waitsFor(function() {
            return _this.flag
        }, 'the .settings_deffered object should get all settings', 1000);

        runs(function() {
            expect(this.article_view_collection._current_width).toBeDefined();
        });
    });

    //-------------------------------------------------------------------------

    it('Should count two columns if the container width is the same that ' +
        'the sum of the two columns and their space', function() {
        var _this = this;

        this.article_view_collection.settings_deferred.always(function() {
            _this.flag = true;
        });

        waitsFor(function() {
            return _this.flag
        }, 'the .settings_deffered object should get all settings', 1000);

        spyOn(this.article_view_collection.$container, 'width').andReturn(748);
        this.article_view_collection.options.element_space = 48;

        runs(function() {
            this.article_view_collection._current_width = 350;
            var obtained = this.article_view_collection._get_columns_amount();
            expect(obtained).toBe(2);
        });
    });

    it('Should count two columns if the container width is one pixel larger ' +
        'than the sum of the two columns and their space', function() {
        var _this = this;

        this.article_view_collection.settings_deferred.always(function() {
            _this.flag = true;
        });

        waitsFor(function() {
            return _this.flag
        }, 'the .settings_deffered object should get all settings', 1000);

        spyOn(this.article_view_collection.$container, 'width').andReturn(749);
        this.article_view_collection.options.element_space = 48;

        runs(function() {
            this.article_view_collection._current_width = 350;
            var obtained = this.article_view_collection._get_columns_amount();
            expect(obtained).toBe(2);
        });
    });

    it('Should count one columns if the container width is one pixel ' +
        'smaller than the sum of the two columns and their space', function() {
        var _this = this;

        this.article_view_collection.settings_deferred.always(function() {
            _this.flag = true;
        });

        waitsFor(function() {
            return _this.flag
        }, 'the .settings_deffered object should get all settings', 1000);

        spyOn(this.article_view_collection.$container, 'width').andReturn(747);
        this.article_view_collection.options.element_space = 48;

        runs(function() {
            this.article_view_collection._current_width = 350;
            var obtained = this.article_view_collection._get_columns_amount();
            expect(obtained).toBe(1);
        });
    });

    it('Should count one columns if the container is smaller than the current '
        + 'column width', function() {
        var _this = this;

        this.article_view_collection.settings_deferred.always(function() {
            _this.flag = true;
        });

        waitsFor(function() {
            return _this.flag
        }, 'the .settings_deffered object should get all settings', 1000);

        spyOn(this.article_view_collection.$container, 'width').andReturn(349);
        this.article_view_collection.options.element_space = 48;

        runs(function() {
            this.article_view_collection._current_width = 350;
            var obtained = this.article_view_collection._get_columns_amount();
            expect(obtained).toBe(1);
        });
    });
});
