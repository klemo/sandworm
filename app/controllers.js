angular.module('sandworm')
    .controller(
        'LabsCtrl',
        ['LabsService',
         function(LabsService) {
             var self = this;
             self.labs =  [{'title': 'LAB1'},
                           {'title': 'LAB2'},
                           {'title': 'LAB3'},
                           {'title': 'LAB4'},
                           {'title': 'LAB5'}];
             /* self.activities = [];
             LabsService.getLabs().then(function(resp) {
                 self.labs = resp.data;
             });*/
         }]);