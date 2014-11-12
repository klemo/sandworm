/**
 * @module sandworm
 * @description sandworm client based on angularjs
 */

var sandworm = angular.module('sandworm', [
    'ui.router',
    'ngResource'
])
/** LabService @returns list of labs */
.factory('LabService', ['$resource', function($resource){
    return $resource('api/labs/:labId.json', {}, {
        query: {method: 'GET',
                params: {labId: 'labs'},
                isArray: true}
    });
}])
/** LabResultsService @returns results for given lab */
.factory('LabResultsService', ['$resource', function($resource){
    return $resource('api/labs/:labId/results.json', {}, {
        query: {method: 'GET',
                params: {labId: 'labs'},
                isArray: true}
    });
}])
/** AdminResultsService @returns all scores and results */
.factory('AdminResultsService', ['$resource', function($resource){
    return $resource('api/results/results.json', {}, {
        query: {method: 'GET',
                params: {},
                isArray: false}
    });
}])
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
.config(function($stateProvider, $urlRouterProvider) {
    /* default (non-admin) pages */
    $stateProvider.state('labs', {
        url: '/labs',
        views: {
            'uir-view-nav': { templateUrl: 'views/nav.html' },
            'uir-view-content': {
                templateUrl: 'views/labs.html',
                controller: 'LabCtrl as labCtrl'}
        }
    }).state('lab', {
        url: '/labs/:labId',
        views: {
            'uir-view-nav': { templateUrl: 'views/nav.html' },
            'uir-view-content': {
                templateUrl: 'views/lab.html',
                controller: 'LabDetailsCtrl as ctrl'}
        }
    /* admin pages */
    }).state('admin-labs', {
        url: '/admin/labs',
        views: {
            'uir-view-nav': { templateUrl: 'views/admin_nav.html' },
            'uir-view-content': {
                templateUrl: 'views/admin_labs.html',
                controller: 'LabCtrl as labCtrl'}
        }
    }).state('admin-lab', {
        url: '/admin/labs/:labId',
        views: {
            'uir-view-nav': { templateUrl: 'views/admin_nav.html' },
            'uir-view-content': {
                templateUrl: 'views/admin_lab.html',
                controller: 'AdminLabDetailsCtrl as ctrl'}
        }
    }).state('admin-results', {
        url: '/admin/results',
        views: {
            'uir-view-nav': { templateUrl: 'views/admin_nav.html' },
            'uir-view-content': {
                templateUrl: 'views/admin_results.html',
                controller: 'AdminResultsCtrl as ctrl'}
        }        
    });
    $urlRouterProvider.when('/admin', '/admin/labs');
    $urlRouterProvider.otherwise('/labs');
});