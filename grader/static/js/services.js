/**
 * @module sandworm
 * @description sandworm services
 */

var sandwormServices = angular.module('sandwormServices', [
    'ui.router',
    'ngResource',
    'ngCookies'
])
.constant('API', {
    user: 'api/v1',
    admin: 'api/v1/admin',
})

/* Admin services */
/** AdminLabService @returns list of labs */
.factory('AdminLabService', ['$resource', 'API', function($resource, API) {
    return $resource(API.admin + '/labs/:labId', {}, {
        query: {method: 'GET',
                params: {labId: ''},
                isArray: true}
    });
}])
/** AdminResultsService @returns all scores and results */
.factory('AdminResultsService', ['$resource', 'API',  function($resource, API) {
    return $resource(API.admin + '/results', {}, {
        query: {method: 'GET',
                params: {},
                isArray: false}
    });
}])

/* User services */
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
/** UserService @description deals with user authentication */
.factory('UserService', ['$http', function($http) {
    var service = {
        isLoggedIn: false,
        currentUser: undefined,
        user: function() {
            return $http.get('/api/v1/user')
                .then(function(response) {
                    service.isLoggedIn = true;
                    service.currentUser = response.data;
                    return response;
                });
        },
        login: function(user) {
            return $http.post('/api/v1/login', user)
                .then(function(response) {
                    service.isLoggedIn = true;
                    service.currentUser = response.data;
                    return response;
                });
        },
        logout: function() {
            return $http.get('/api/v1/logout')
                .then(function(response) {
                    service.isLoggedIn = false;
                    service.currentUser = undefined;
                    return response;
                });
        }
    };
    return service;
}]);