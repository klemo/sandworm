(function () {

  'use strict';

  angular
    .module('sandwormControllers')
    .controller('AdminLabCtrl', AdminLabCtrl);

  function AdminLabCtrl(adminService) {

    var self = this;
    self.editingData = {};

    function initController() {
      adminService.getListOfLabs().query(function(labs) {
        self.labs = labs;
        angular.forEach(self.labs, function (oneLab) {
          var data = {
            isEditing: false,
            buttonText: 'Uredi'
          };
          self.editingData[oneLab.id] = data;
        });
      });
    }


    /* JS Date helpers */
    var _n = new Date();
    var now = new Date(_n.getFullYear(), _n.getMonth(), _n.getDate());

    var plusMonth = function (t) {
      return new Date(t.getFullYear(), t.getMonth() + 1, t.getDate());
    };

    self.editLab = function (oneLab) {
      self.editingData[oneLab.id].isEditing = !self.editingData[oneLab.id].isEditing;
      self.editingData[oneLab.id].buttonText = self.editingData[oneLab.id].isEditing ? 'Spremi' : 'Uredi';
      if(!self.editingData[oneLab.id].isEditing) {
        console.log('ok');
      }

    };

    self.isEditLab = function (oneLab) {
      return self.editingData[oneLab.id].isEditing;
    };


    /* Handle form data */
    self.lab = {
      name: 'LAB 3',
      desc: 'test description',
      start: now,
      end: plusMonth(now)
    };
    self.updateEnd = function () {
      if (self.lab.start) {
        self.lab.end = plusMonth(self.lab.start);
      }
    };
    self.submit = function () {
      adminService.getListOfLabs().save({labId: ''}, self.lab).$promise.then(
        function (lab) {
          //self.labs.push(lab);
          self.labs = adminService.getListOfLabs().query();
          self.infoMessage = 'Lab created';
        },
        function (err) {
          self.errorMessage = err;
        });
    };

    initController();
  }

})();
