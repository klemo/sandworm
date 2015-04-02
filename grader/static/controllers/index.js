(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('LoginCtrl', LoginCtrl);

    /** AdminUsersCtrl @description displays users info on admin pages */
    function LoginCtrl(UserService, $state) {
        var self = this;
        self.userService = UserService;
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
