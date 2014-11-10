var sandworm = angular.module('sandworm', [
    'ngRoute',
    'ngResource',
])
.factory('LabService', ['$resource', function($resource){
    return $resource('api/labs/:labId.json', {}, {
        query: {method: 'GET',
                params: {labId: 'labs'},
                isArray: true}
    });
}])
.controller('LabCtrl', ['LabService', function(LabService) {
    var self = this;
    var now = Date.now();
    self.labs = LabService.query(function(labs) {
        labs = angular.forEach(labs, function(lab) {
            lab.isOver = lab.end < now;
        });
    });
}])
.controller('LabDetailsCtrl', ['$routeParams', 'LabService', function($routeParams, LabService) {
    var self = this;
    self.lab = LabService.get({labId: $routeParams.labId}, function(lab) {
        lab.isOver = lab.end < Date.now();
    });
}])
.config(function($routeProvider) {
    $routeProvider.when('/labs', {
        templateUrl: 'views/labs.html',
        controller: 'LabCtrl as labCtrl'
    }).when('/labs/:labId', {
        templateUrl: 'views/lab.html',
        controller: 'LabDetailsCtrl as labDetailsCtrl'
    });
    $routeProvider.otherwise({
        redirectTo: '/labs'
    });
});