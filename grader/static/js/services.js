/**
 * @module sandworm
 * @description sandworm services
 */

var sandwormServices = angular.module('sandwormServices', [
    'ui.router',
    'ngResource',
    'ngCookies'
])
/** LabService @returns list of labs */
.factory('LabService', ['$resource', function($resource){
    return $resource('static/api/labs/:labId.json', {}, {
        query: {method: 'GET',
                params: {labId: 'labs'},
                isArray: true}
    });
}])
/** LabResultsService @returns results for given lab */
.factory('LabResultsService', ['$resource', function($resource){
    return $resource('static/api/labs/:labId/results.json', {}, {
        query: {method: 'GET',
                params: {labId: 'labs'},
                isArray: true}
    });
}])
/** AdminResultsService @returns all scores and results */
.factory('AdminResultsService', ['$resource', function($resource){
    return $resource('static/api/results/results.json', {}, {
        query: {method: 'GET',
                params: {},
                isArray: false}
    });
}])
.constant('USER_ROLES', {
    all: '*',
    admin: 'admin',
    user: 'user'
})
/** UserService @description deals with user authentication */
.factory('UserService', ['$http', function($http) {
    var service = {
        isLoggedIn: false,
        user: null,
        user: function() {
            return $http.get('/api/v1/user')
                .then(function(response) {
                    service.isLoggedIn = true;
                    service.user = response.data;
                    return response;
                });
        },
        login: function(user) {
            return $http.post('/api/v1/login', user)
                .then(function(response) {
                    service.isLoggedIn = true;
                    service.user = response.data;
                    return response;
                });
        },
        logout: function() {
            return $http.get('/api/v1/logout')
                .then(function(response) {
                    service.isLoggedIn = false;
                    service.user = null;
                    return response;
                });
        }
    };
    return service;
}]);