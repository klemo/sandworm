/**
 * @module sandworm
 * @description sandworm controllers
 */

var sandwormControllers = angular.module('sandwormControllers', [
    'ui.router',
    'ngResource',
    'ngCookies',
])

/* Admin controllers */
/** AdminLabCtrl @description displays labs */
.controller('AdminLabCtrl', ['AdminLabService', function(LabService) {
    var self = this;
    self.labs = LabService.query();
    
    /* JS Date helpers */
    var _n = new Date();
    var now = new Date(_n.getFullYear(), _n.getMonth(), _n.getDate());

    var plusMonth = function(t) {
        return new Date(t.getFullYear(), t.getMonth() + 1, t.getDate());
    };
    
    /* Handle form data */
    self.lab = {
        name: 'LAB 3',
        desc: 'test description',
        start: now,
        end: plusMonth(now)
    };
    self.updateEnd = function() {
        if (self.lab.start) {
            self.lab.end = plusMonth(self.lab.start);
        }
    };
    self.submit = function() {
        LabService.save({labId: ''}, self.lab).$promise.then(
            function(lab) {
                //self.labs.push(lab);
                self.labs = LabService.query();
                self.infoMessage = 'Lab created';
            },
            function(err) {
                self.errorMessage = err;
            });
    };
}])

/** LabResultsCtrl @description displays lab details for admin */
.controller('AdminLabDetailsCtrl', ['$stateParams', 'AdminLabService', '$state', function($stateParams, LabService, $state) {
    var self = this;
    self.lab = LabService.get({labId: $stateParams.labId});
    self.deleteLab = function() {
        if (confirm('Remove this lab?')) {
            LabService.remove({labId: $stateParams.labId}).$promise.then(
                function(lab) {
                    $state.go('admin-labs');
                },
                function(err) {
                    self.errorMessage = err;
                });
        };
    }
    
}])

/** AdminResultsCtrl @description displays all results on admin pages */
.controller('AdminResultsCtrl', ['$stateParams', 'AdminResultsService',
                                 function($stateParams, AdminResultsService) {
    var self = this;
    self.results = AdminResultsService.query();
}])

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
.controller('LabDetailsCtrl', ['$stateParams', 'LabService', 'FileUploader', '$cookies', '$socket', function($stateParams, LabService, FileUploader, $cookies, $socket) {
    var self = this;
    self.lab = LabService.get({labId: $stateParams.labId}, function(lab) {
        //lab.isOver = lab.end < Date.now();
    });
    // Handle file uploading
    self.uploader = new FileUploader({
        url: '/api/v1/labs',
        method: 'post',
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

    // Start sockjs connection and wait for messages
    $socket.start();

    $socket.on('start', function(e, data){
        console.log('Received: ', data);
    });

    $socket.send('start', []);
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