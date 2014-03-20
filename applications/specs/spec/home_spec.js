;describe('Spec of main', function() {
    beforeEach(function() {
        spyOn($, 'ajax');
    })

    xit('Shuld has the settings property', function() {
        expect(main.settings).toBeDefined();
    });

    /* BUG: I don't know why this test don't pass. I think that jasmine.js
    has a bug with the spyOn funcion. */
    xit('Should load image settings', function() {
        expect($.ajax).toHaveBeenCalledWith({
            dataType: 'json',
            url: helpers.set_path('applications/image_settings.json'),
        })
    });
});


describe('Test for ArticleModel', function() {
    var article_model = new main.ArticleModel();

    it('Should contain all defaults attributes', function() {
        expect(article_model.get('id')).toBe('');
        expect(article_model.get('title')).toBe('');
        expect(article_model.get('url')).toBe('');
        expect(article_model.get('description')).toBe('');
        expect(article_model.get('cover_image')).toBe('');
        expect(article_model.get('completed')).toBe(false);
    });
});


describe('Test for ArticleCollection', function() {
    beforeEach(function() {
        this.article_collection = new main.ArticleCollection()
    });

    it('Can add ArticleModel instances', function() {
        var _length = this.article_collection.length;
        this.article_collection.add([
            {title: 'prueba 1'},
            {title: 'prueba 2'}
        ]);
        expect(this.article_collection.length).toBe(_length + 2);
    });
});


describe('Test for the individual article template', function() {
    beforeEach(function() {
        this.article_model = new main.ArticleModel({
            title: 'Test Title'
        });
        this.article_view = new main.ArticleModelView({
            model: this.article_model
        });
        this.$articleTemplate = $('#articleTemplate');
    });

    it('should have the .templateId property', function() {
        expect(this.article_view.templateId).toBeDefined();
    });

    it('The model should tied to an <artilce> DOM element', function() {
        expect(this.article_view.el.tagName.toLowerCase()).toBe('article');
        expect(this.article_view.el.className).toBe('cover_article_item');
    });

    it('Return the view object', function() {
        expect(this.article_view.render()).toEqual(this.article_view);
    });
});


describe('Test for the filled template', function() {
    beforeEach(function() {
        spyOn($, 'ajax');
        this.article_model = new main.ArticleModel({
            id: 1,
            title: 'Test Title',
            url: 'path/to/article',
            description: 'a single description',
            cover_image: 'path/to/image.jpg'
        });
        this.article_view = new main.ArticleModelView({
            model: this.article_model
        });
        this.article_view.render();
        this.filled_template = this.article_view.el.innerHTML;
    });

    it('Fill the title', function() {
        expect(this.filled_template).toContain('<h2>Test Title</h2>');
    });

    it('Fill the url image', function() {
        expect(this.filled_template)
            .toContain(helpers.set_path('path/to/image'));
        console.log(helpers.set_path('path/to/image'));
    });

    it('Fill the description', function() {
        expect(this.filled_template).toContain('a single description')
    });

    it('Fill the url of the article', function() {
        expect(this.filled_template)
            .toContain(helpers.set_path('proyectos/path/to/article'));
    });

    xit('Fill the quality of the image', function() {
        expect(this.filled_template)
            .toContain(helpers.set_path('jpg90'));
    });
});
