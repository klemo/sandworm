(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('AdminLabDetailsCtrl', AdminLabDetailsCtrl);

    function AdminLabDetailsCtrl(AdminLabService, $stateParams, $state) {

        var self = this;
        self.lab = AdminLabService.get({labId: $stateParams.labId});
        self.deleteLab = function () {
            if (confirm('Remove this lab?')) {
                AdminLabService.remove({labId: $stateParams.labId}).$promise.then(
                    function (lab) {
                        $state.go('admin-labs');
                    },
                    function (err) {
                        self.errorMessage = err;
                    });
            }
        }

    }

})();
