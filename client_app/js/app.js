var sandworm = angular.module('sandworm', [
    'ui.router',
    'ngResource'
])
.factory('LabService', ['$resource', function($resource){
    return $resource('api/labs/:labId.json', {}, {
        query: {method: 'GET',
                params: {labId: 'labs'},
                isArray: true}
    });
}])
.factory('LabResultsService', ['$resource', function($resource){
    return $resource('api/labs/:labId/results.json', {}, {
        query: {method: 'GET',
                params: {labId: 'labs'},
                isArray: true}
    });
}])
.factory('AdminResultsService', ['$resource', function($resource){
    return $resource('api/results/results.json', {}, {
        query: {method: 'GET',
                params: {},
                isArray: false}
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
.controller('LabDetailsCtrl', ['$stateParams', 'LabService', function($stateParams, LabService) {
    var self = this;
    self.lab = LabService.get({labId: $stateParams.labId}, function(lab) {
        lab.isOver = lab.end < Date.now();
    });
}])
.controller('LabResultsCtrl', ['$stateParams', 'LabResultsService', function($stateParams, LabResultsService) {
    var self = this;
    self.lab = LabResultsService.get({labId: $stateParams.labId}, function(lab) {});
}])
.controller('AdminResultsCtrl', ['$stateParams', 'AdminResultsService', function($stateParams, AdminResultsService) {
    var self = this;
    self.results = AdminResultsService.query();
}])
.config(function($stateProvider, $urlRouterProvider) {
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
                controller: 'LabDetailsCtrl as ctrl'}
        }        
    }).state('admin-lab-results', {
        url: '/admin/labs/:labId/results',
        views: {
            'uir-view-nav': { templateUrl: 'views/admin_nav.html' },
            'uir-view-content': {
                templateUrl: 'views/admin_lab_results.html',
                controller: 'LabResultsCtrl as ctrl'}
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
    $urlRouterProvider.otherwise('/labs');
    $urlRouterProvider.when('/admin', '/admin/labs');
});