;describe('jQuery.created', function() {
    beforeEach(function() {
        setFixtures('<div id="created_element_container"></div>');
        this.$container = $('#created_element_container');
    });

    it('should has the .created() method', function() {
        expect(this.$container.created).toBeDefined();
    });
});