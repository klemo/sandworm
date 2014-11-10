var sandworm = angular.module('sandworm', [
    'ngRoute',
    'ngResource',
])
.factory('LabService', ['$resource', function($resource){
    return $resource('labs/:labId.json', {}, {
        query: {method: 'GET',
                params: {labId: 'labs'},
                isArray: true}
    });
}])
.controller('LabCtrl', ['LabService', function(LabService) {
    var self = this;
    self.labs = LabService.query();
}])
.config(function($routeProvider) {
    $routeProvider.when('/', {
        templateUrl: 'views/labs.html',
        controller: 'LabCtrl as labCtrl'
    });
    $routeProvider.otherwise({
        redirectTo: '/'
    });
});