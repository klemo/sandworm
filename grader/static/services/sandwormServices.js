var sandwormServices = angular.module('sandwormServices', [
    'ui.router',
    'ngResource',
    'ngCookies'
])
.constant('API', {
    user: 'api/v1',
    admin: 'api/v1/admin'
});