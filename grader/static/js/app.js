/**
 * @module sandworm
 * @description sandworm client based on angularjs
 */

var sandworm = angular.module('sandworm', [
    'ui.router',
    'ngResource',
    'ngCookies',
    'ng-socket',
    'ui.bootstrap',
    'angularFileUpload',
    'sandwormServices',
    'sandwormControllers'
]).config(function($stateProvider, $urlRouterProvider, $socketProvider) {
    /* default (non-admin) pages */
    $stateProvider.state('index', {
        url: '/',
        data: {
            isPublic: true,
            access: '*'
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
            access: '*'
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
            access: 'user'
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
            access: 'user'
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
            access: 'admin'
        },
        views: {
            'uir-view-nav': {
                templateUrl: 'static/views/admin_nav.html',
                controller: 'LoginCtrl as ctrl'
            },
            'uir-view-content': {
                templateUrl: 'static/views/admin_labs.html',
                controller: 'AdminLabCtrl as labCtrl'}
        }
    }).state('admin-lab', {
        url: '/admin/labs/:labId',
        data: {
            isPublic: false,
            access: 'admin'
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
            access: 'admin'
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
    }).state('admin-users', {
        url: '/admin/users',
        data: {
            isPublic: false,
            access: 'admin'
        },
        views: {
            'uir-view-nav': {
                templateUrl: 'static/views/admin_nav.html',
                controller: 'LoginCtrl as ctrl'
            },
            'uir-view-content': {
                templateUrl: 'static/views/admin_users.html',
                controller: 'AdminUsersCtrl as ctrl'}
        }        
    });
    $urlRouterProvider.when('/admin', '/admin/labs');
    $urlRouterProvider.otherwise('/');

    // set web sockets
    $socketProvider.configure({
        address: 'http://localhost:8080/api/v1/submitjob',
        logger: function(e) {
            console.log(e);
        }
    });
    
}).run(['$rootScope', '$location', '$http', '$cookies', '$state', '$q', '$socket', 'authentication',
        function($rootScope, $location, $http, $cookies, $state, $q, $socket, authentication) {

    /* set xsrf header */
    $http.defaults.headers['post']['X-XSRFToken'] = $cookies['_xsrf'];
    $http.defaults.headers['put']['X-XSRFToken'] = $cookies['_xsrf'];
    $http.defaults.headers['delete'] = $http.defaults.headers['post'];

    $rootScope.$on('$stateChangeStart', function (event, next) {
        /* prevent user from navigating to non-authorized or private resource
         * warn: client-side only! */
        var evv = event;
        authentication.user().then(
            function(success) {
                if (next.data.access !== '*' && next.data.access !== authentication.currentUser.role) {
                    $state.go('index');
                }
            },
            function(err) {
                if (!next.data.isPublic) {
                    $state.go('login');
                }
                return $q.reject(err);
            });
    });
    
}]);