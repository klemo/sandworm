(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('AdminResultsCtrl', AdminResultsCtrl);

    /** AdminResultsCtrl @description displays all results on admin pages */
    function AdminResultsCtrl(AdminResultsService) {

        var self = this;
        self.results = AdminResultsService.query()

    }

})();
