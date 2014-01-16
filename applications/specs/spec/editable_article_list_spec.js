;describe('main.ArticleItemModel', function() {

    beforeEach(function() {
        this.article_item_model = new main.ArticleItemModel();
    })

    it('shuld has the defaults values', function() {
        expect(this.article_item_model.defaults).toEqual({
            title: ''
            ,cover_image: ''
            ,id: ''
            ,quality: null
            ,width: null
            ,shard: null
        });
    });
});


describe('main.ArticleListCollection', function() {

    beforeEach(function() {
        this.article_list_collection = new main.ArticleListCollection();
    });

    it('should has the correct url', function() {
        expect(this.article_list_collection.url)
            .toEqual(helpers.set_path('/admin/get-list-of-articles'));
    });
});


describe('main.ArticleItemView', function() {

    beforeEach(function() {
        this.model = new main.ArticleItemModel();
        this.model.set({
            title: 'Test 1'
            ,cover_image: 'applications/specs/static/' + 
                'casa-gr-EBwJcukXrehhuixkGvNH53.jpg'
            ,id: 1
        });

        this.article_item_view = new main.ArticleItemView({
            model: this.model
        });
    });

    it('should has the cid value', function() {
        expect(this.article_item_view.model.get('cid')).toBeDefined();
    });

    it('should render the image src', function() {
        this.article_item_view.render();
        expect(this.article_item_view.$el.html())
            .toContain('applications/specs/static/' + 
                'casa-gr-EBwJcukXrehhuixkGvNH53.jpg');
    });

    it('should has the .go_to_edit_page() method', function() {
        expect(this.article_item_view.go_to_edit_page).toBeDefined();
    });

    it('should has the .remove_article() method', function() {
        expect(this.article_item_view.remove_article).toBeDefined();
    });

    it('should add the id DOM attribute', function() {
        this.article_item_view.render();
        expect(this.article_item_view.$el.attr('id'))
            .toEqual('item_' + this.article_item_view.model.cid);
    });
});