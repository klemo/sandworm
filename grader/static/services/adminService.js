(function () {
    'use strict';

    angular
        .module('sandwormServices')
        .factory('adminService', AdminService);

    /**
     * ImpactUtils is used as service that knows how to work with impacts.
     */
    function AdminService($resource, API, $http) {
        var functionalities = {
            getListOfLabs: getListOfLabs,
            getAllScoresAndResults: getAllScoresAndResults,
            getAllUsers: getAllUsers,
            editLab: editLab
        };

        /** @returns list of labs */
        function getListOfLabs() {
            return $resource(API.admin + '/labs/:labId', {}, {
                query: {
                    method: 'GET',
                    params: {labId: ''},
                    isArray: true
                }
            });
        }

        /**  @returns all scores and results */
        function getAllScoresAndResults() {
            return $resource(API.admin + '/results', {}, {
                query: {
                    method: 'GET',
                    params: {},
                    isArray: false
                }
            });
        }

        /**  @returns all users */
        function getAllUsers() {
            return $resource(API.admin + '/users', {}, {
                query: {
                    method: 'GET',
                    params: {},
                    isArray: true
                }
            });
        }

        function editLab(lab) {
            console.log(lab);
            return $http.put(API.admin + '/labs', lab)
              .then(function(response){
                  console.log(response)
              });
            return $resource(API.admin + '/labs', {}, {
                query: {
                    method: 'PUT',
                    params: {lab: lab},
                    isArray: true
                }
            });
        }


        return functionalities;
    }

})();
