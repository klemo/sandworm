(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('AdminUsersCtrl', AdminUsersCtrl);

    /** AdminUsersCtrl @description displays users info on admin pages */
    function AdminUsersCtrl(adminService) {
        var self = this;
        self.users = adminService.getAllUsers().query();
    }

})();
