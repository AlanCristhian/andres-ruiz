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

    it('Should get the container width', function() {
        expect(this.article_view_collection.container_width).toBeDefined();
    });
});
