;describe('main.MultimediaModel', function() {
    beforeEach(function() {
        this.multimedia_model = new main.MultimediaModel();
    });

    it('can make an instance of ImageModel class', function() {
        expect(this.multimedia_model).toBeDefined();
    });

    it('should have the .defaults property', function() {
        expect(this.multimedia_model.defaults).toEqual({
            url: ''
            ,description: ''
            ,article_name: 'editarticletest'
            ,type: 'image_file'
            ,cover: false
        });
    });
});


describe('main.ImageDescriptionView', function() {
    beforeEach(function() {
        this.image_desc_view = new main.ImageDescriptionView();
    });

    it('should has <div> tag in the tagName property', function() {
        expect(this.image_desc_view.tagName).toEqual('div');
    });
});


describe('main.MultimediaView', function() {
    beforeEach(function() {
        setFixtures('<div id="main_ImageView"></div>');

        main.article_data_view = new main.ArticleDataView();
        this.multimedia_model = new main.MultimediaModel({
            shard: 1
            ,quality: 90
            ,width: 350
            ,type: 'image_file'
            ,title: 'Title'
            ,cover_image: false
        });
        this.image_view = new main.MultimediaView({
            model: this.multimedia_model
        });
        this.image_view.render();
        this.image_view.$el.appendTo($('#main_ImageView'));
    });

    it('can make an instance of ImageView class', function() {
        expect(this.image_view).toBeDefined();
    });

    it('your tagName property should be "article"', function() {
        expect(this.image_view.tagName).toEqual('article');
    });

    it('the .templateId property should be #image_file_template if' +
            '.options.type is "file"', function() {
        this.image_view = new main.MultimediaView({model: this.multimedia_model});
        expect(this.image_view.templateId).toEqual('#image_file_template');
    });

    it('the .templateId property should be #image_link_template if' +
            '.options.type is "image_link"', function() {
        this.multimedia_model.set('type', 'image_link');
        this.image_view = new main.MultimediaView({model: this.multimedia_model});
        expect(this.image_view.templateId).toEqual('#image_link_template');
    });

    it('the .tagName property should be .image_file_container if' +
            '.options.type is "file"', function() {
        this.image_view = new main.MultimediaView({model: this.multimedia_model});
        expect(this.image_view.className).toEqual('.image_file_container');
    });

    it('the .tagName property should be .image_link_container if' +
            '.options.type is "image_link"', function() {
        this.multimedia_model.set('type', 'image_link');
        this.image_view = new main.MultimediaView({model: this.multimedia_model});
        expect(this.image_view.className).toEqual('.image_link_container');
    });

    it('the model shuld have the cid property', function() {
        expect(this.image_view.model.get('cid')).toBeDefined();
    });

    it('should have the .Model class', function() {
        expect(this.image_view.Model).toBeDefined();
    });

    it('should have the .template property', function() {
        expect(this.image_view.template).toBeDefined();
    });

    it('should have the .events property', function() {
        expect(this.image_view.events).toEqual({
            'click .remove_image': 'remove_image'
            ,'mouseup .input_file': 'trigger_input_file_click'
            ,'click .input_link': 'add_image_link'
            ,'click .input_video': 'add_video_link'
            ,'click .cover_setter': 'set_as_cover'
        });
    });

    it('should have the .remove_image() method', function() {
        expect(this.image_view.remove_image).toBeDefined();
    });

    // I skipt that because I need find a way to render only the image.
    // See NOTE: 1: in the source file.
    xit('should have the ._update_image() method', function() {
        expect(this.image_view._update_image).toBeDefined();
    });

    it('should have the .$input_file property', function() {
        expect(this.image_view.$input_file.jquery).toBeDefined();
    });

    it('should have the .uploading_deferred property', function() {
        expect(this.image_view.uploading_deferred).toBeDefined;
    });

    it('should have the ._show_progress_bar() method', function() {
        expect(this.image_view._show_progress_bar).toBeDefined();
    });

    it('should have the ._show_error_flag() method', function() {
        expect(this.image_view._show_error_flag).toBeDefined();
    });

    it('should have the ._hide_status_flags() method', function() {
        expect(this.image_view._hide_status_flags).toBeDefined();
    });

    it('should have the ._hide_form_elements() method', function() {
        expect(this.image_view._hide_form_elements).toBeDefined();
    });

    it('should have the ._set_template() mehtod', function() {
        expect(this.image_view._set_template).toBeDefined();
    })

    describe('Image link uploading methods', function() {
        beforeEach(function() {
            this.image_view.add_image_link();
        });

        it('should have the .add_image_link() method', function() {
            expect(this.image_view.add_image_link).toBeDefined();
        });

        // maybe innecessary.
        xit('should make the ._$input_link_button property', function() {
            expect(this.image_view._$input_link_button.jquery).toBeDefined();
        });

        it('should make the ._$input_link_field property', function() {
            expect(this.image_view._$input_link_field.jquery).toBeDefined();
        });

        it('should make the ._$accept_link_button property', function() {
            expect(this.image_view._$accept_link_button.jquery).toBeDefined();
        });

        it('should make the ._$cancel_input_link property', function() {
            expect(this.image_view._$cancel_input_link.jquery).toBeDefined();
        });

        it('should have the .add_multimedia_link_accept() method', function() {
            expect(this.image_view.add_multimedia_link_accept).toBeDefined();
        })

        it('should make the ._deferred_image_link property', function() {
            this.image_view.add_multimedia_link_accept({
                type: 'image_link'
                ,url_handler: '/admin/save-image-link'
            });
            expect(this.image_view._deferred_image_link).toBeDefined();
        });
    });

    describe('.set_as_cover()', function() {
        beforeEach(function() {
            this.image_view.set_as_cover();
        });

        it('should make the ._set_cover_deferred property', function() {
            expect(this.image_view._set_cover_deferred).toBeDefined();
        });

        it('should make the ._cover_data property', function() {
            expect(this.image_view._cover_data).toBeDefined();
        });
    });
});


describe('main.ImageCollection', function() {
    beforeEach(function() {
        this.image_collection = new main.ImageCollection();
    });

    it('can make an instance of main.ImageCollection', function() {
        expect(this.image_collection).toBeDefined();
    });

    it('should have the correct url', function() {
        expect(this.image_collection.url)
            .toEqual(helpers.set_path('/admin/get-article-data'));
    });

    it('shold have the model property', function() {
        expect(this.image_collection.model).toEqual(main.MultimediaModel);
    });
});


describe('main.ImageCollectionView', function() {
    var value;

    beforeEach(function(done) {
        setTimeout(function() {
            value = 0;
            done();
        }, 20);

        setFixtures('<section id="multimedia_container"></section>');
        this.image_collect_view = new main.ImageCollectionView({
            ImageModel: main.MultimediaModel.extend({
                defaults: {
                    title: ''
                    ,cover_image: ''
                    ,description: ''
                }
            })
        });
        this.image_collect_view.render();
    });

    it('should have the .tagName property', function() {
        expect(this.image_collect_view.tagName).toEqual('article');
    });

    it('should have the .id property', function() {
        expect(this.image_collect_view.id)
            .toEqual('new_multimedia_container');
    });

    it('should have the .template property', function() {
        expect(this.image_collect_view.template).toBeDefined();
    });

    it('should have the .$add_multimedia_file property', function() {
        expect(this.image_collect_view.$add_multimedia_file.jquery)
            .toBeDefined();
    });

    it('should have the .collection property', function() {
        expect(this.image_collect_view.collection).toBeDefined();
    });

    it('should have the .defaults property', function() {
        expect(this.image_collect_view.defaults).toEqual({
            ImageModel: main.MultimediaModel
            ,ImageView: main.MultimediaView
            ,ImageCollection: main.ImageCollection
            ,container: '#content'
        });
    });

    it('should have the .render_one() method', function() {
        expect(this.image_collect_view.render_one).toBeDefined();
    });

    it('should have the .$container property', function() {
        expect(this.image_collect_view.$container.jquery).toBeDefined();
    });

    it('should have the .render_all property', function() {
        expect(this.image_collect_view.render_all).toBeDefined();
    });

    it('should have the .settings_deferred property', function() {
        expect(this.image_collect_view.settings_deferred)
            .toBeDefined();
    });

    it('should have the .fix_sizes() method', function() {
        expect(this.image_collect_view.fix_sizes).toBeDefined();
    });

    // Specs of all methods    

    describe('.add_multimedia_file()', function() {
        beforeEach(function(done) {
            main.article_data_view = new main.ArticleDataView();
            this.image_collect_view.add_multimedia_file();
            done();
        });

        it('should create an instance of main.MultimediaModel class',
                function() {
            expect(this.image_collect_view._multimedia_model
                instanceof main.MultimediaModel).toBeTruthy();
        });

        it('should create an instance of helpers.Breakpoints', function() {
            expect(this.image_collect_view._breakpoints
                instanceof helpers.Breakpoints).toBeTruthy();
        });

        it('should create an instance of main.MultimediaView class',
                function() {
            expect(this.image_collect_view._image_view
                instanceof main.MultimediaView).toBeTruthy();
        });

        it('should create the <input/> DOM element', function() {
            expect(this.image_collect_view._$input_file.jquery)
                .toBeDefined();
        });

        it('should create the container of the new image', function() {
            expect(this.image_collect_view._$image_container.jquery)
                .toBeDefined();
        });

        // can't found
        xit('should set the ._$image_container in the .$contaier', function() {
            expect(this.image_collect_view._$image_container)
                .toContainElement($('[name="input_image_'+ this.image_collect_view._multimedia_model.cid + '"]'));
        });

        it('should have the ._deferred_image_data property', function() {
            expect(this.image_collect_view._deferred_multimedia_data).toBeDefined();
        });
    });
});