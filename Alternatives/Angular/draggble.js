angular.module('app', ['ngDraggable'])
  .controller('controller', function($scope) {

    $scope.listItems = [{
      name: "some name",
      title: "title1"
    }, {
      name: "some name2",
      title: "title2"
    }, {
      name: "some name3",
      title: "title3"
    }, ];

    $scope.droppedObjects = [];
    $scope.input = {};
  
    $scope.onDragComplete = function(data, evt) {
      console.log("drag success, data:", data);
      var index = $scope.droppedObjects.indexOf(data);
      if (index > -1) {
        $scope.droppedObjects.splice(index, 1);
      }
    }
    
    $scope.onDropComplete = function(data, evt) {
      console.log("drop success, data:", data);
      var index = $scope.droppedObjects.indexOf(data);
      if (index == -1)
        $scope.droppedObjects.push(data);
    }
    
    $scope.onDropCompleteInput = function(data, evt) {
      console.log("drop on input success, data:", data);
      $scope.input = data;
    }
    
    $scope.onDropCompleteRemove = function(data, evt) {
      console.log("drop success - remove, data:", data);
      var index = $scope.droppedObjects.indexOf(data);
      if (index != -1)
        $scope.droppedObjects.splice(index);
    }

    var onDraggableEvent = function(evt, data) {
      console.log("128", "onDraggableEvent", evt, data);
    }
    $scope.$on('draggable:start', onDraggableEvent);
    //$scope.$on('draggable:move', onDraggableEvent);
    $scope.$on('draggable:end', onDraggableEvent);
  
  });
