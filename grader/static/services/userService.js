(function () {
  'use strict';

  angular
    .module('sandwormServices')
    .factory('UserService', UserService);

  /**
   * UserService is used as serve that knows how to work with impacts.
   */
  function UserService($resource, API, $http) {
    var functionalities = {
      getListOfLabs: getListOfLabs
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

    return functionalities;
  }

})();
