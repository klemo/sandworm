angular.module('sandworm', ['ngRoute'])
    .config(function($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: 'views/labs.html',
            controller: 'LabsCtrl as labsCtrl'
        });
        $routeProvider.otherwise({
            redirectTo: '/'
        });
    });