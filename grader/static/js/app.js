/**
 * @module sandworm
 * @description sandworm client based on angularjs
 */

var sandworm = angular.module('sandworm', [
    'ui.router',
    'ngResource',
    'ngCookies',
    'sandwormServices',
    'sandwormControllers'
]).config(function($stateProvider, $urlRouterProvider) {
    /* default (non-admin) pages */
    $stateProvider.state('index', {
        url: '/',
        data: {
            isPublic: true,
            access: '*',
        },
        views: {
            'uir-view-nav': {
                templateUrl: 'static/views/nav.html',
                controller: 'LoginCtrl as ctrl'
            },
            'uir-view-content': {
                templateUrl: 'static/views/index.html',
                controller: 'IndexCtrl as ctrl'
            }
        }
    }).state('login', {
        url: '/login',
        data: {
            isPublic: true,
            access: '*',
        },
        views: {
            'uir-view-nav': {
                templateUrl: 'static/views/nav.html',
                controller: 'LoginCtrl as ctrl'
            },
            'uir-view-content': {
                templateUrl: 'static/views/index.html',
                controller: 'LoginCtrl as ctrl'
            }
        }
    }).state('labs', {
        url: '/labs',
        data: {
            isPublic: false,
            access: 'user',
        },
        views: {
            'uir-view-nav': {
                templateUrl: 'static/views/nav.html',
                controller: 'LoginCtrl as ctrl'
            },
            'uir-view-content': {
                templateUrl: 'static/views/labs.html',
                controller: 'LabCtrl as labCtrl'}
        }
    }).state('lab', {
        url: '/labs/:labId',
        data: {
            isPublic: false,
            access: 'user',
        },
        views: {
            'uir-view-nav': {
                templateUrl: 'static/views/nav.html',
                controller: 'LoginCtrl as ctrl'
            },
            'uir-view-content': {
                templateUrl: 'static/views/lab.html',
                controller: 'LabDetailsCtrl as ctrl'}
        }
    /* admin pages */
    }).state('admin-labs', {
        url: '/admin/labs',
        data: {
            isPublic: false,
            access: 'admin',
        },
        views: {
            'uir-view-nav': {
                templateUrl: 'static/views/admin_nav.html',
                controller: 'LoginCtrl as ctrl'
            },
            'uir-view-content': {
                templateUrl: 'static/views/admin_labs.html',
                controller: 'LabCtrl as labCtrl'}
        }
    }).state('admin-lab', {
        url: '/admin/labs/:labId',
        data: {
            isPublic: false,
            access: 'admin',
        },
        views: {
            'uir-view-nav': {
                templateUrl: 'static/views/admin_nav.html',
                controller: 'LoginCtrl as ctrl'
            },
            'uir-view-content': {
                templateUrl: 'static/views/admin_lab.html',
                controller: 'AdminLabDetailsCtrl as ctrl'}
        }
    }).state('admin-results', {
        url: '/admin/results',
        data: {
            isPublic: false,
            access: 'admin',
        },
        views: {
            'uir-view-nav': {
                templateUrl: 'static/views/admin_nav.html',
                controller: 'LoginCtrl as ctrl'
            },
            'uir-view-content': {
                templateUrl: 'static/views/admin_results.html',
                controller: 'AdminResultsCtrl as ctrl'}
        }        
    });
    $urlRouterProvider.when('/admin', '/admin/labs');
    $urlRouterProvider.otherwise('/');
    
}).run(['$rootScope', '$location', '$http', '$cookies', '$state', 'UserService',
        function($rootScope, $location, $http, $cookies, $state, UserService) {

    /* set xsrf header */
    $http.defaults.headers.post['X-XSRFToken'] = $cookies['_xsrf'];

    UserService.user();

    $rootScope.$on('$stateChangeStart', function (event, next) {
        /* prevent user from navigating to non-authorized or private resource
         * warn: client-side only! */
        if (UserService.isLoggedIn) {
            if (next.data.access !== '*' && next.data.access !== UserService.currentUser.role) {
                event.preventDefault();
            }
        } else {
            if (!next.data.isPublic) {
                event.preventDefault();
                $state.go('login');
            }
        }
    });
    
}]);