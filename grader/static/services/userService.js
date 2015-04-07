(function () {
    'use strict';

    angular
        .module('sandwormServices')
        .factory('uService', UserService);

    /**
     * ImpactUtils is used as service that knows how to work with impacts.
     */
    function UserService($resource, API, $http) {
        var functionalities = {
            getListOfLabs: getListOfLabs,
            authentication: authentication
        };

        /** @returns list of labs */
        function getListOfLabs() {
            return $resource(API.user + '/labs/:labId', {}, {
                query: {
                    method: 'GET',
                    params: {labId: ''},
                    isArray: true
                }
            });
        }

        /** @description deals with user authentication */
        function authentication() {
            var service = {
                isLoggedIn: false,
                currentUser: undefined,
                user: function () {
                    return $http.get('/api/v1/user')
                        .then(function (response) {
                            service.isLoggedIn = true;
                            service.currentUser = response.data;
                            return response;
                        });
                },
                login: function (user) {
                    return $http.post('/api/v1/login', user)
                        .then(function (response) {
                            service.isLoggedIn = true;
                            service.currentUser = response.data;
                            return response;
                        });
                },
                logout: function () {
                    return $http.get('/api/v1/logout')
                        .then(function (response) {
                            service.isLoggedIn = false;
                            service.currentUser = undefined;
                            return response;
                        });
                }
            };
            return service;
        }


        return functionalities;
    }

})();
