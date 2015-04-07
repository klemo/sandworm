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
    admin: 'api/v1/admin'
})


/*****************************************************************************/
/* User services */
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