describe('ArticleCollectionView', function() {

    beforeEach(function() {

        setFixtures('<section id="content"></section>');
        this.article_view_collection = new ArticleCollectionView({
            Collection: main.ArticleCollection,
            ModelView: main.ArticleModelView
        });
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

    it('Should has the initial_content property', function() {
        expect(this.article_view_collection.initial_content).toBeDefined();
    });

    it('Should has the .element_space property', function() {
        expect(this.article_view_collection.options.element_space)
            .toBeDefined();
    });
});

describe('ArticleCollectionView asyncronous functions', function() {
    var async_flag;

    beforeEach(function(done) {
        setFixtures('<section id="content"></section>');
        this.article_view_collection = new ArticleCollectionView({
            Collection: main.ArticleCollection,
            ModelView: main.ArticleModelView
        });

        setTimeout(function() {
            // store a flag property to test asyncronous tasks
            async_flag = false;
            done();
        }, 5);
    });

    it('Should has the ._current_width property', function(done) {
        this.article_view_collection.settings_deferred.always(function() {
            async_flag = true;
        });
        expect(this.article_view_collection._current_width).toBeDefined();
        done();
    });

    it('Should count two columns if the container width is the same that ' +
        'the sum of the two columns and their space', function(done) {
        this.article_view_collection.settings_deferred.always(function() {
            async_flag = true;
        });

        spyOn(this.article_view_collection.$container, 'width')
            .and.returnValue(748);
        this.article_view_collection.options.element_space = 48;

        this.article_view_collection._current_width = 350;
        var obtained = this.article_view_collection._get_columns_amount();
        expect(obtained).toBe(2);

        done();
    });

    it('Should count two columns if the container width is one pixel larger ' +
            'than the sum of the two columns and their space', function(done) {

        this.article_view_collection.settings_deferred.always(function() {
            async_flag = true;
        });

        spyOn(this.article_view_collection.$container, 'width')
            .and.returnValue(749);
        this.article_view_collection.options.element_space = 48;

        this.article_view_collection._current_width = 350;
        var obtained = this.article_view_collection._get_columns_amount();
        expect(obtained).toBe(2);

        done();
    });

    it('Should count one columns if the container width is one pixel ' +
            'smaller than the sum of the two columns and their space',
            function(done) {
        this.article_view_collection.settings_deferred.always(function() {
            async_flag = true;
        });

        spyOn(this.article_view_collection.$container, 'width')
            .and.returnValue(747);
        this.article_view_collection.options.element_space = 48;

        this.article_view_collection._current_width = 350;
        var obtained = this.article_view_collection._get_columns_amount();
        expect(obtained).toBe(1);

        done();
    });

    it('Should count one columns if the container is smaller than the current '
            + 'column width', function(done) {
        this.article_view_collection.settings_deferred.always(function() {
            async_flag = true;
        });

        spyOn(this.article_view_collection.$container, 'width')
            .and.returnValue(349);
        this.article_view_collection.options.element_space = 48;

        this.article_view_collection._current_width = 350;
        var obtained = this.article_view_collection._get_columns_amount();
        expect(obtained).toBe(1);

        done();
    });
});