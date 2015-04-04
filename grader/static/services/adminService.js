(function() {
    'use strict';

    angular
        .module('sandwormServices')
        .factory('adminService', AdminLabService);

    /**
     * ImpactUtils is used as service that knows how to work with impacts.
     */
    function AdminLabService($resource, API) {
        var functionalities = {
            getListOfLabs: getListOfLabs
        };

        /** @returns list of labs */
        function getListOfLabs() {
            return $resource(API.admin + '/labs/:labId', {}, {
                query: {method: 'GET',
                    params: {labId: ''},
                    isArray: true}
            });
        }

//    .factory('AdminLabService', ['$resource', 'API', function($resource, API) {
//            return $resource(API.admin + '/labs/:labId', {}, {
//                query: {method: 'GET',
//                    params: {labId: ''},
//                    isArray: true}
//            });
//        }])


        return functionalities;
    }

})();
