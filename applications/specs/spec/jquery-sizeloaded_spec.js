;describe('jQuery.sizeloaded', function() {
    beforeEach(function(done) {
        setFixtures('<img class="image_size"></img>');
        this.$image = $('.image_size');
        spyOnEvent(this.$image, 'sizeloaded');
        this.$image
            .sizeloaded()
            .attr('src', 'applications/specs/static/casa-gr-EBwJcukXrehhuixkGvNH53.jpg?q=' + Math.random());

        setTimeout(function() {
            this.flag = false;
            done();
        }, 500);
    });

    it('Should has the .sizeloaded() method', function() {
        expect(this.$image.sizeloaded).toBeDefined();
    });

    xit('Should raise the sizeloaded event', function(done) {
        var _this = this;

        this.$image.on('sizeloaded', function() {
            _this.flag = true;
        });

        expect('sizeloaded').toHaveBeenTriggeredOn(_this.$image);
        done()
    });
});