angular.module('sandworm')
    .factory(
        'LabsService',
        ['$http',
         function($http) {
             return {
                 getLabs: function() {
                     return $http.get('/api/labs');
                 }
             }
         }]);