(function () {
  'use strict';

  angular
    .module('sandwormServices')
    .factory('authentication', function ($http) {
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
              console.log('kaj');
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
    });
})();