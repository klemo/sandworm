(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('AdminLabDetailsCtrl', AdminLabDetailsCtrl);

    function AdminLabDetailsCtrl(adminService, $stateParams, $state) {

        var self = this;
        self.lab = adminService.getListOfLabs().get({labId: $stateParams.labId});
        self.deleteLab = function () {
            if (confirm('Remove this lab?')) {
                adminService.getListOfLabs().remove({labId: $stateParams.labId}).$promise.then(
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
