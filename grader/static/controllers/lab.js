(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('LabCtrl', LabCtrl);

    /** LabCtrl @description displays labs */
    function LabCtrl(UserService) {

        var self = this;
        //var now = angular.toJson(new Date());
        self.labs = UserService.getListOfLabs().query(function(labs) {
            labs = angular.forEach(labs, function(lab) {
                //lab.isOver = lab.end < now;
            });
        });
    }

})();
