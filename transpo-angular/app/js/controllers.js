'use strict';

/* Controllers */

var transpoApp = angular.module('transpoApp', []);

transpoApp.controller('PhoneListCtrl', ['$scope', '$http', function($scope, $http) {
  $http.get('phones/phones.json').success(function(data) {
    $scope.phones = data;
  });

  $scope.orderProp = 'age';
}]);
