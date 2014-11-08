describe('LabsCtrl', function() {
    beforeEach(module('sandoworm'));
    var ctrl, mockService;

    /*beforeEach(module(function($provide) {
        mockService = {
            getLabs: function() {
                return [{'title': 'LAB1'}];
            }
        };
        $provide.value('LabsService', mockService);
    }));*/

    beforeEach(inject(function($controller) {
        ctrl = $controller('LabsCtrl');
    }));

    it('should contain labs', function() {
        expect(ctrl.labs.length).toEqual(5);
    });
});