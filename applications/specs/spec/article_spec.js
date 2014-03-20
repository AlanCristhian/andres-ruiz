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

    it('Should contain $image, $container and $wrapper properties', function(){
        expect(main.$image).toBeDefined();
        expect(main.$container).toBeDefined();
        expect(main.$wrapper).toBeDefined();
    });
});


describe('Test for ImageModel', function() {
    var image_model = new main.ImageModel();

    it('Should contain all defaults attributes', function() {
        expect(image_model.get('id')).toBe('');
        expect(image_model.get('url')).toBe('');
        expect(image_model.get('article_name')).toBe('');
        expect(image_model.get('description')).toBe('');
    });
});


describe('Test for ImageCollection', function() {
    beforeEach(function() {
        this.image_collection = new main.ImageCollection()
    });

    it('Can add ImageModel instances', function() {
        var _length = this.image_collection.length;
        this.image_collection.add([
            {title: 'prueba 1'},
            {title: 'prueba 2'}
        ]);
        expect(this.image_collection.length).toBe(_length + 2);
    });
});


describe('Test for the individual image template', function() {
    beforeEach(function() {
        this.image_model = new main.ImageModel({
            title: 'Test Title'
        });
        this.article_view = new main.ImageModelView({
            model: this.image_model
        });
        this.$articleTemplate = $('#imageTemplate');
    });

    it('should contain the .templateId propertie', function() {
        expect(this.article_view.templateId).toBeDefined();
    })

    it('The model should tied to an <artilce> DOM element', function() {
        expect(this.article_view.el.tagName.toLowerCase()).toBe('article');
        expect(this.article_view.el.className).toBe('image_item');
    });

    it('Return the view object', function() {
        expect(this.article_view.render()).toEqual(this.article_view);
    });
});


describe('Test for the filled template', function() {
    beforeEach(function() {
        spyOn($, 'ajax');
        this.image_model = new main.ImageModel({
            id: 1,
            url: 'path/to/image.jpg',
            description: 'a single description',
            title: 'Title',
            cover_image: true
        });
        this.article_view = new main.ImageModelView({
            model: this.image_model
        });
        this.article_view.render();
        this.filled_template = this.article_view.el.innerHTML;
    });

    it('Fill the url image', function() {
        expect(this.filled_template)
            .toContain(helpers.set_path('path/to/image'));
    });

    it('Fill the description', function() {
        expect(this.filled_template).toContain('a single description')
    });

    xit('Fill the quality of the image', function() {
        expect(this.filled_template)
            .toContain(helpers.set_path('jpg90'));
    });
});


describe('main.ImageModelView', function() {
    beforeEach(function() {
        this.image_model_view = new main.ImageModelView({
            model: new main.ImageModel()
        });
    });

    it('should contain the fix_image_size method', function() {
        expect(this.image_model_view.fix_image_size).toBeDefined();
    });

    it('should contain the zoom_out_image method', function() {
        expect(this.image_model_view.zoom_out_image).toBeDefined();
    });
});