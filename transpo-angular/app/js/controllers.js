'use strict';

/* Services */

var BASE_URL = 'http://127.0.0.1:8000';
var URL_LINES = BASE_URL + '/api/v1/lines/';
var URL_STATIONS = BASE_URL + '/api/v1/stations/';

angular
  .module('StationService', [])
  .factory('stations', ['$http', function ($http) {
    return {
      list: function () {
        return $http.get(URL_STATIONS);
      }
    };
  }]);

angular
  .module('LineService', [])
  .factory('lines', ['$http', function ($http) {
    return {
      list: function () {
        return $http.get(URL_LINES);
      }
    };
  }]);

/* Controllers */

var transpoApp = angular.module('transpoApp', ['ngMaterial', 'StationService', 'LineService']);
var baseUrl = 'http://127.0.0.1:8000';

function twoDigits(x) {
  return x < 10 ? '0' + x : x;
}

function toDateString(date) {
  return (1900 + date.getYear()) + '-' + twoDigits(date.getMonth() + 1) + '-' + twoDigits(date.getDate());
}

function toTimeString(date) {
  return twoDigits(date.getHours()) + ':' + twoDigits(date.getMinutes());
}

function toDateTimeString(date) {
  return toDateString(date) + ' ' + toTimeString(date);
}

transpoApp.controller('DateCtrl', function($scope) {
  $scope.scheduleDate = toDateTimeString(new Date());
});

function mapByAttr(arr, attr) {
  function mapper(acc, value) {
    acc[value[attr]] = value;
    return acc;
  }
  return arr.reduce(mapper, {});
}

function toMap(data) {
  return mapByAttr(data, 'url');
}

transpoApp.controller('StationListCtrl', ['$scope', 'stations', 'lines', function($scope, stations, lines) {
  lines.list().then(function(response) {
    $scope.lines = response.data;
    return stations.list();
  }).then(function(response) {
    $scope.stations = response.data;
    $scope.linesMap = toMap($scope.lines);
  });
}]);

transpoApp.controller('StationTimesListCtrl', ['$scope', '$http', function($scope, $http) {
  var url = baseUrl + '/api/v1/stations/1/times/?date=';
  $http.get(url).success(function(data) {
    $scope.stationTimes = data;
  });
}]);

transpoApp.controller('LocationTimesListCtrl', ['$scope', '$http', 'stations', 'lines', function($scope, $http, stations, lines) {
  var url = baseUrl + '/api/v1/locations/3/times/?date=2016-01-17&time=10:00';
  $http.get(url).success(function(data) {
    $scope.locationTimes = data;

    lines.list().then(function(response) {
      $scope.lines = response.data;
      return stations.list();
    }).then(function(response) {
      $scope.stations = response.data;
      $scope.linesMap = toMap($scope.lines);
      $scope.stationsMap = toMap($scope.stations);
    });
  });
}]);
