describe('main.ArticleDescriptionModel', function() {
    beforeEach(function() {
        this.article_desc_model = new main.ArticleDescriptionModel();
    });

    it('can make an instance of main.ArticleDescriptionModel', function() {
        expect(this.article_desc_model).toBeDefined();
    });

    it('have the .url property', function() {
        expect(this.article_desc_model.url)
            .toEqual(helpers.set_path('/admin/get-article-data'));
    });
});

describe('main.ArticleDescriptionView', function() {
    beforeEach(function() {
        this.article_desc_view = new main.ArticleDescriptionView();
        this.article_desc_view.model.set('description', '')
    });

    it('can make an instance of main.ArticleDescriptionView', function() {
        expect(this.article_desc_view).toBeDefined();
    });

    it('should have the .tagName property', function() {
        expect(this.article_desc_view.tagName).toEqual('article');
    });

    it('should have the .id property', function() {
        expect(this.article_desc_view.className)
            .toEqual('article_description_container');
    });

    it('should have a default .options.Model() class', function() {
        expect(this.article_desc_view.options.Model)
            .toBeDefined();
    });

    it('should instantiate the .model property from the .options.Model()' +
            ' class', function() {
        expect(this.article_desc_view.model).toBeDefined();
    });

    it('should have the .show_info_and_buttons() method', function(){
        expect(this.article_desc_view.show_info_and_buttons).toBeDefined()
    });

    it('should have the .hide_info_and_buttons() method', function(){
        expect(this.article_desc_view.hide_info_and_buttons).toBeDefined()
    });

    it('should have the .save_description() method', function(){
        expect(this.article_desc_view.save_description).toBeDefined()
    });

    it('should have the .fix_textarea_size() method', function() {
        expect(this.article_desc_view.fix_textarea_size).toBeDefined();
    });

    describe('main.ArticleDescriptionView.template', function() {
        it('have defined the .template property', function() {
            expect(this.article_desc_view.template).toBeDefined();
        });

        it('have the description field', function() {
            expect($('#article_description_template').html())
                .toContain('{{description}}');
        });
    });
});

describe('main.ArticleDescriptionView DOM elements', function() {
    var async_flag;

    beforeEach(function(done) {
        this.article_desc_view = new main.ArticleDescriptionView();
        this.article_desc_view.model.set('description', '');

        setTimeout(function() {
            async_flag = false;
            done();
        }, 20);
    });

    it('should have the .$edit_buttons property',
            function(done) {
        this.article_desc_view.settings_deferred.done(function() {
            async_flag = true;
        });
        expect(this.article_desc_view.$edit_buttons.jquery).toBeDefined();
        done();
    });

    it('should have the .$edit_article_description property',
            function(done) {
        this.article_desc_view.settings_deferred.done(function() {
            async_flag = true;
        });
        expect(this.article_desc_view.$edit_article_description.jquery)
            .toBeDefined();
        done();
    });

    it('should have the .$article_description_status property',
            function(done) {
        this.article_desc_view.settings_deferred.done(function() {
            async_flag = true;
        });
        expect(this.article_desc_view.$article_description_status.jquery)
            .toBeDefined();
        done();
    });

    it('should have the .$article_description_done property',
            function(done) {
        this.article_desc_view.settings_deferred.done(function() {
            async_flag = true;
        });
        expect(this.article_desc_view.$article_description_done.jquery)
            .toBeDefined();
        done();
    });

    it('should have the .$article_description_error property',
            function(done) {
        this.article_desc_view.settings_deferred.done(function() {
            async_flag = true;
        });
        expect(this.article_desc_view.$article_description_error.jquery)
            .toBeDefined();
        done();
    });

    it('should have the .$article_description_uploading property',
            function(done) {
        this.article_desc_view.settings_deferred.done(function() {
            async_flag = true;
        });
        expect(this.article_desc_view.$article_description_uploading.jquery)
            .toBeDefined();
        done();
    });

    it('should have the .$article_description property',
            function(done) {
        this.article_desc_view.settings_deferred.done(function() {
            async_flag = true;
        });
        expect(this.article_desc_view.$article_description.jquery)
            .toBeDefined();
        done();
    });

    it('should have the .$textarea_description property',
            function(done) {
        this.article_desc_view.settings_deferred.done(function() {
            async_flag = true;
        });
        expect(this.article_desc_view.$textarea_description.jquery)
            .toBeDefined();
        done();
    });
});