(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('AdminUsersCtrl', AdminUsersCtrl);

    /** AdminUsersCtrl @description displays users info on admin pages */
    function AdminUsersCtrl(AdminUsersService) {
        var self = this;
        self.users = AdminUsersService.query();
    }

})();
