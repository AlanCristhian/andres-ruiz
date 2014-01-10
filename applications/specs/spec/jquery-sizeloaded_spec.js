;describe('jQuery.sizeloaded', function() {
    beforeEach(function() {
        this.flag = false;
        setFixtures('<img class="image_size"></img>');
        this.$image = $('.image_size');
        spyOnEvent(this.$image, 'sizeloaded');
        this.$image
            .sizeloaded()
            .attr('src', 'applications/specs/static/casa-gr-EBwJcukXrehhuixkGvNH53.jpg?q=' + Math.random());
    });

    it('Should has the .sizeloaded() method', function() {
        expect(this.$image.sizeloaded).toBeDefined();
    });

    it('Should raise the sizeloaded event', function() {
        var _this = this;

        this.$image.on('sizeloaded', function() {
            _this.flag = true;
        });

        waitsFor(function() {
            return _this.flag
        }, 'the sizeloaded event should be triggered.', 5000);

        runs(function() {
            expect('sizeloaded').toHaveBeenTriggeredOn(_this.$image);
        });
    });
});