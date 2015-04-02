(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('LabCtrl', LabCtrl);

    /** LabCtrl @description displays labs */
    function LabCtrl(LabService) {
        var self = this;
        self.labs = LabService.query();
    }

})();
