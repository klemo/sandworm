(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('LoginCtrl', LoginCtrl);

    /** AdminUsersCtrl @description displays users info on admin pages */
    function LoginCtrl($state, authentication) {
        var self = this;
        self.userService = authentication;
        self.user = {username: '', password: ''};
        self.login = function() {
            authentication.login(self.user).then(function(success) {
                $state.go('index');
            }, function(error) {
                self.errorMessage = error.data.err;
            })
        };
        self.logout = function() {
            authentication.logout().then(function(success) {
                $state.go('index');
            }, function(error) {
                self.errorMessage = error.data.err;
            })
        };
    }

})();
