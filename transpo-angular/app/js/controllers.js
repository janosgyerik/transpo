'use strict';

/* Controllers */

var transpoApp = angular.module('transpoApp', []);

transpoApp.controller('PhoneListCtrl', ['$scope', '$http', function($scope, $http) {
  $http.get('phones/phones.json').success(function(data) {
    $scope.phones = data;
  });

  $scope.orderProp = 'age';
}]);

transpoApp.controller('StationListCtrl', ['$scope', '$http', function($scope, $http) {
  var url = 'http://127.0.0.1:8000/api/v1/stations/';
  $http.get(url).success(function(data) {
    $scope.stations = data;
  });
}]);
