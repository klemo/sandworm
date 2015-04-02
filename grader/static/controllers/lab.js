(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('LabCtrl', LabCtrl);

    /** LabCtrl @description displays labs */
    function LabCtrl(LabService) {
        var self = this;
        self.labs = LabService.query();

//        var self = this;
//        //var now = angular.toJson(new Date());
//        self.labs = LabService.query(function(labs) {
//            labs = angular.forEach(labs, function(lab) {
//                //lab.isOver = lab.end < now;
//            });
//        });
    }

})();
