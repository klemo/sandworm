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
    });
    $urlRouterProvider.otherwise('/labs');
    $urlRouterProvider.when('/admin', '/admin/labs');
});