(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('IndexCtrl', IndexCtrl);

    /** AdminUsersCtrl @description displays users info on admin pages */
    function IndexCtrl($state, authentication) {
        var self = this;
        self.userService = authentication;
        if (self.userService.isLoggedIn) {
            if (self.userService.currentUser.role == 'admin') {
                $state.go('admin-labs');
            } else {
                $state.go('labs');
            }
        } else {
            $state.go('login');
        }
    }

})();
