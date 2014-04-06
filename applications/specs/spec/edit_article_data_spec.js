// disable jQuery animatios
;$.fx.off = !$.fx.off;


describe('Main module', function() {
    it('should has the ArticleDataModel class', function() {
        expect(main.ArticleDataModel).toBeDefined();
    });

    it('should has the ArticleDataView class', function() {
        expect(main.ArticleDataView).toBeDefined();
    });

    it('should has the .options property', function() {
        expect(new main.ArticleDataView().options).toEqual({
            Model: main.ArticleDataModel
        })
    })
});


describe('main.ArticleDataModel', function() {
    beforeEach(function() {
        this.article_data_model = new main.ArticleDataModel();
    });

    it('should has the correct url', function() {
        expect(this.article_data_model.url)
            .toEqual(helpers.set_path('/admin/get-article-data'))
    });
});


describe('main.ArticleDataView', function() {
    beforeEach(function() {
        this.article_data_view = new main.ArticleDataView();
    });

    it('should has the #article_data_template content', function() {
        expect(this.article_data_view.template).toBeDefined();
    });

    it('should has the .tagName property', function() {
        expect(this.article_data_view.tagName).toEqual('article');
    });

    it('should has the .id property', function() {
        expect(this.article_data_view.id).toEqual('article_data_container');
    });

    it('should has the .model property', function() {
        expect(this.article_data_view.model).toBeDefined();
    });

    it('should has the .show_info_and_buttons() method', function() {
        expect($.isFunction(this.article_data_view.show_info_and_buttons))
            .toBeTruthy();
    });

    it('should has the .hide_info_and_buttons() method', function() {
        expect($.isFunction(this.article_data_view.hide_info_and_buttons))
            .toBeTruthy();
    });

    it('should has the .save_info_fields() method', function() {
        expect($.isFunction(this.article_data_view.save_info_fields))
            .toBeTruthy();
    });
});


describe('main.ArticleDataView.template', function() {
    beforeEach(function() {
        this.template = $('#article_data_template').html();
    });

    it('should has the classification field', function() {
        expect(this.template).toContain('{{classification}}');
    });

    it('should has the country field', function() {
        expect(this.template).toContain('{{country}}');
    });

    it('should has the state field', function() {
        expect(this.template).toContain('{{state}}');
    });

    it('should has the city field', function() {
        expect(this.template).toContain('{{city}}');
    });

    it('should has the autor field', function() {
        expect(this.template).toContain('{{autor}}');
    });

    it('should has the colaborators field', function() {
        expect(this.template).toContain('{{colaborators}}');
    });

    it('should has the project_date field', function() {
        expect(this.template).toContain('{{project_date}}');
    });
});

describe('main.ArticleDataView DOM elements', function () {
    var async_flag;

    beforeEach(function(done) {
        this.article_data_view = new main.ArticleDataView();
        this.article_data_view.model.set({
            classification: 'void',
            country: 'void',
            state: 'void',
            city: 'void',
            autor: 'void',
            colaborators: 'void',
            project_date: 'void'
        });

        setTimeout(function() {
            async_flag = false;
            done();
        }, 40);
    });

    it('should has the .$input_text jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$input_text.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$classification jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$classification.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$country jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$country.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$state jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$state.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$city jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$city.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$autor jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$autor.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$colaborators jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$colaborators.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$project_date jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$project_date.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$edit_buttons jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$edit_buttons.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$edit_article_data jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$edit_article_data.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$article_data_status jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$article_data_status.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$article_status_done jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$article_status_done.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$article_status_error jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$article_status_error.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .$article_status_uploading jQuery object', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.$article_status_uploading.jquery)
            .toBeDefined()
        done();
    });

    it('should has the .article_visibility property', function(done) {
        this.article_data_view.settings_deferred.done(function() {
            async_flag = true
        });
        expect(this.article_data_view.article_visibility).toBeDefined();
        done();
    });
});


describe('main.SwitcherButton', function() {
    beforeEach(function() {
        jasmine.getFixtures().fixturesPath = helpers.set_path('');
        loadFixtures('applications/editArticle/views/' +
            'switch_button_template.html');
        this.switcher = new main.SwitcherButton();
    });

    it('to be defined', function() {
        expect(main.SwitcherButton).toBeDefined();
    });

    it('should has the .settings property', function() {
        expect(this.switcher.settings).toBeDefined();
    });

    it('should has the .$element property', function() {
        expect(this.switcher.$container).toBeDefined();
    });

    it('should has the .$switch_button property', function() {
        expect(this.switcher.$switch_button).toBeDefined();
    });

    it('should has the .$off_label property', function() {
        expect(this.switcher.$off_label).toBeDefined();
    });

    it('should has the .$on_label property', function() {
        expect(this.switcher.$on_label).toBeDefined();
    });

    it('should has the .$switch_slider property', function() {
        expect(this.switcher.$switch_slider).toBeDefined();
    });

    it('should has the ._switch_button_width property', function() {
        expect(this.switcher._switch_button_width).toBeDefined();
    });

    it('should has the ._container_width property', function() {
        expect(this.switcher._container_width).toBeDefined();
    });

    describe('._set_default_state() method', function() {
        it('should show the OFF label by default.', function() {
            this._switcher = new main.SwitcherButton();
            var left_str = this._switcher.$switch_slider.css('left'),
                left_num = parseInt(left_str.replace('px', ''));
            expect(left_num != 0).toBeTruthy();
        });

        it('should show the ON label.', function() {
            this._switcher = new main.SwitcherButton({on: true});
            var left_str = this._switcher.$switch_slider.css('left'),
                left_num = parseInt(left_str.replace('px', ''));
            expect(left_num == 0).toBeTruthy();
        });

        it('should show the OFF label.', function() {
            this._switcher = new main.SwitcherButton({on: false});
            var left_str = this._switcher.$switch_slider.css('left'),
                left_num = parseInt(left_str.replace('px', ''));
            expect(left_num != 0).toBeTruthy();
        });
    });

    it('should has the ._switch_state() method', function() {
        expect(this.switcher._switch_state).toBeDefined();
    });

    it('should change the value of the .settings.on property', function() {
        this._switcher = new main.SwitcherButton({on: false});
        this._switcher.$switch_button.trigger('click');
        expect(this._switcher.settings.on).toEqual(true);
    });

    it('should show the ON label when click.', function() {
        this._switcher = new main.SwitcherButton({on: false});
        this._switcher.$switch_button.trigger('click');
        var left_str = this._switcher.$switch_slider.css('left'),
            left_num = parseInt(left_str.replace('px', ''));
        expect(left_num == 0).toBeTruthy();
    });

    it('should has the ._click_callbacks property', function() {
        expect(this.switcher._click_callbacks instanceof Array).toBeTruthy();
    });

    it('should has the ._run_callbacks() method', function() {
        expect(this.switcher._run_callbacks).toBeDefined();
    });

    it('shuld has the .add_click_callback() method', function() {
        expect(this.switcher.add_click_callback).toBeDefined();
    })
});
