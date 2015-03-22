/**
 * @module sandworm
 * @description sandworm controllers
 */

var sandwormControllers = angular.module('sandwormControllers', [
    'ui.router',
    'ngResource',
    'ngCookies',
])

/** AdminResultsCtrl @description displays all results on admin pages */
.controller('AdminResultsCtrl', ['$stateParams', 'AdminResultsService',
                                 function($stateParams, AdminResultsService) {
    var self = this;
    self.results = AdminResultsService.query();
}])

/** AdminUsersCtrl @description displays users info on admin pages */
.controller('AdminUsersCtrl', ['$stateParams', 'AdminUsersService', function($stateParams, AdminUsersService) {
    var self = this;
    self.users = AdminUsersService.query();
}])

/*****************************************************************************/
/* User controllers */
/** LabCtrl @description displays labs */
.controller('LabCtrl', ['LabService', function(LabService) {
    var self = this;
    //var now = angular.toJson(new Date());
    self.labs = LabService.query(function(labs) {
        labs = angular.forEach(labs, function(lab) {
            //lab.isOver = lab.end < now;
        });
    });
}])
/** LabDetailsCtrl @description displays lab details */
.controller('LabDetailsCtrl', ['$stateParams', 'LabService', 'UserService', 'FileUploader', '$scope', '$cookies', '$socket', function($stateParams, LabService, UserService, FileUploader, $scope, $cookies, $socket) {
    var self = this;
    self.lab = LabService.get({labId: $stateParams.labId}, function(lab) {
        //lab.isOver = lab.end < Date.now();
    });

    self.jobStatus = '';
    self.jobStatusProgress = 0;

    self.updateProgress = function(status) {
        console.log('-- ', status);
        self.jobStatus = status;
        self.jobStatusProgress += 30;
    };

    var ws = new WebSocket('ws://localhost:8080/api/v1/submitjob');
    ws.onopen = function() {};
    ws.onmessage = function (evt) {
        var msg = JSON.parse(evt.data);
        if (msg.length !== 2) {
            console.log('WS invalid message format', msg);
        } else {
            var event = msg[0];
            var data = msg[1];
            switch(event) {
            case 'job-status':
                $scope.$apply(function () {
                    self.updateProgress(data);
                });
                break;
            default:
                console.log('WS unknown event', msg);
            }
        };
    };
    
    // Handle file uploading
    self.uploader = new FileUploader({
        url: '/api/v1/labs',
        method: 'post',
        removeAfterUpload: true,
        queue: [],
        headers: {'X-XSRFToken': $cookies['_xsrf']}
    });
    self.uploader.filters.push({
        name: 'zipFilter',
        fn: function(item /*{File|FileLikeObject}*/, options) {
            var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
            return '|zip|'.indexOf(type) !== -1;
        }
    });
    self.uploader.onWhenAddingFileFailed = function(item, filter, options) {
        if (filter.name === 'queueLimit') {
            //self.uploader.clearQueue();
            //self.uploader.addToQueue( );
        } else if (filter.name === 'zipFilter') {
            self.errorMessage = 'Must be zip archive!';
        };
    };
    self.uploader.onAfterAddingFile = function(fileItem) {
        self.errorMessage = '';
    };
    self.uploader.onSuccessItem = function(fileItem) {
        self.errorMessage = '';
        self.updateProgress('Uploaded');
    };
}])
.controller('LoginCtrl', ['UserService', '$state', function(UserService, $state) {
    var self = this;
    self.userService = UserService;
    self.user = {username: '', password: ''};
    self.login = function() {
        UserService.login(self.user).then(function(success) {
            $state.go('index');
        }, function(error) {
            self.errorMessage = error.data.err;
        })
    };
    self.logout = function() {
        UserService.logout().then(function(success) {
            $state.go('index');
        }, function(error) {
            self.errorMessage = error.data.err;
        })
    };
}])
.controller('IndexCtrl', ['UserService', '$state', function(UserService, $state) {
    var self = this;
    self.userService = UserService;
    if (self.userService.isLoggedIn) {
        if (self.userService.currentUser.role == 'admin') {
            $state.go('admin-labs');
        } else {
            $state.go('labs');
        }
    } else {
        $state.go('login');
    };
}]);