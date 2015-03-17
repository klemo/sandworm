/* jshint ignore:start */
'use strict';
/* jshint ignore:end */

/* Models */

angular.module('sandwormControllers', ['ui.router',
    'ngResource',
    'ngCookies',
    'sandwormServices'])
    .value('version', '0.1');
