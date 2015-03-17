(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('AdminLabCtrl', AdminLabDetailsCtrl);

    function AdminLabDetailsCtrl(AdminLabService, $stateParams, $state) {

        var self = this;
        console.log($stateParams);
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
            };
        }

    }

})();
