(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('LoginCtrl', LoginCtrl);

    /** AdminUsersCtrl @description displays users info on admin pages */
    function LoginCtrl(UserService, $state) {
        var self = this;
        self.userService = UserService;
        self.user = {username: '', password: ''};
        self.login = function() {
            UserService.login(self.user).then(function(success) {
                $state.go('index');
            }, function(error) {
                self.errorMessage = error.data.err;
            })
        };
        self.logout = function() {
            UserService.logout().then(function(success) {
                $state.go('index');
            }, function(error) {
                self.errorMessage = error.data.err;
            })
        };
    }

})();
