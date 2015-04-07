(function() {

    'use strict';

    angular
        .module('sandwormControllers')
        .controller('LabDetailsCtrl', LabDetailsCtrl);

    /** LabDetailsCtrl @description displays lab details */
    function LabDetailsCtrl($stateParams, UserService, FileUploader, $scope, $cookies) {
        var self = this;
        self.lab = UserService.getListOfLabs().get({labId: $stateParams.labId}, function(lab) {
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
            }
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
            }
        };
        self.uploader.onAfterAddingFile = function(fileItem) {
            self.errorMessage = '';
        };
        self.uploader.onSuccessItem = function(fileItem) {
            self.errorMessage = '';
            self.updateProgress('Uploaded');
        };
    }

})();
