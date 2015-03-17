(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('AdminLabCtrl', AdminLabCtrl);

    function AdminLabCtrl(AdminLabService) {

        var self = this;
        console.log('about to call service query...');
        self.labs = AdminLabService.query();

        /* JS Date helpers */
        var _n = new Date();
        var now = new Date(_n.getFullYear(), _n.getMonth(), _n.getDate());

        var plusMonth = function(t) {
            return new Date(t.getFullYear(), t.getMonth() + 1, t.getDate());
        };

        /* Handle form data */
        self.lab = {
            name: 'LAB 3',
            desc: 'test description',
            start: now,
            end: plusMonth(now)
        };
        self.updateEnd = function() {
            if (self.lab.start) {
                self.lab.end = plusMonth(self.lab.start);
            }
        };
        self.submit = function() {
            LabService.save({labId: ''}, self.lab).$promise.then(
                function(lab) {
                    //self.labs.push(lab);
                    self.labs = LabService.query();
                    self.infoMessage = 'Lab created';
                },
                function(err) {
                    self.errorMessage = err;
                });
        };
    }

})();
