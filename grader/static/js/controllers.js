/**
 * @module sandworm
 * @description sandworm controllers
 */

var sandwormControllers = angular.module('sandwormControllers', [
    'ui.router',
    'ngResource',
    'ngCookies',
])
/** LabCtrl @description displays labs */
.controller('LabCtrl', ['LabService', function(LabService) {
    var self = this;
    var now = Date.now();
    self.labs = LabService.query(function(labs) {
        labs = angular.forEach(labs, function(lab) {
            lab.isOver = lab.end < now;
        });
    });
    self.lab = {
        name: '',
        desc: '',
        start: new Date(),
        end: new Date()
    };
    self.submit = function() {
        console.log('Submit with ', self.lab);
    };
}])
/** LabDetailsCtrl @description displays lab details */
.controller('LabDetailsCtrl', ['$stateParams', 'LabService', function($stateParams, LabService) {
    var self = this;
    self.lab = LabService.get({labId: $stateParams.labId}, function(lab) {
        lab.isOver = lab.end < Date.now();
    });
}])
/** LabResultsCtrl @description displays lab details for admin */
.controller('AdminLabDetailsCtrl', ['$stateParams', 'LabResultsService', function($stateParams, LabResultsService) {
    var self = this;
    self.lab = LabResultsService.get({labId: $stateParams.labId}, function(lab) {});
}])
/** AdminResultsCtrl @description displays all results on admin pages */
.controller('AdminResultsCtrl', ['$stateParams', 'AdminResultsService', function($stateParams, AdminResultsService) {
    var self = this;
    self.results = AdminResultsService.query();
}])
.controller('LoginCtrl', ['UserService', '$location', function(UserService, $location) {
    var self = this;
    self.userService = UserService;
    self.user = {username: '', password: ''};
    self.login = function() {
        UserService.login(self.user).then(function(success) {
            /* login success; navigate to labs */
            $location.path('/labs');
        }, function(error) {
            self.errorMessage = error.data.msg;
        })
    };
    self.logout = function() {
        UserService.logout().then(function(success) {
            $location.path('/');
        }, function(error) {
            self.errorMessage = error.data.msg;
        })
    };
}])