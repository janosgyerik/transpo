'use strict';

/* Controllers */

var transpoApp = angular.module('transpoApp', []);
var baseUrl = 'http://127.0.0.1:8000';

transpoApp.controller('PhoneListCtrl', ['$scope', '$http', function($scope, $http) {
  $http.get('phones/phones.json').success(function(data) {
    $scope.phones = data;
  });

  $scope.orderProp = 'age';
}]);

transpoApp.controller('StationListCtrl', ['$scope', '$http', function($scope, $http) {
  var url = baseUrl + '/api/v1/stations/';
  $http.get(url).success(function(data) {
    $scope.stations = data;
  });
}]);

transpoApp.controller('StationTimesListCtrl', ['$scope', '$http', function($scope, $http) {
  var url = baseUrl + '/api/v1/stations/1/times/?date=';
  $http.get(url).success(function(data) {
    $scope.stationTimes = data;
  });
}]);

transpoApp.controller('LocationTimesListCtrl', ['$scope', '$http', function($scope, $http) {
  var url = baseUrl + '/api/v1/locations/3/times/?date=2016-01-17&time=10:00';
  $http.get(url).success(function(data) {
    $scope.locationTimes = data;
  });
}]);
