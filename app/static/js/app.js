'use strict';

var app = angular.module('lilytask', ['angularModalService', 'ngRoute']);

app.config(function($routeProvider) {
    $routeProvider.
        when('/', {
            templateUrl: '../static/html/landing.html'
        }).
        when('/app', {
            templateUrl: '../static/html/app.html'
        }).
        otherwise({
            redirectTo: '/'
        }
    );
})

app.controller('ShowRegisterController', function($scope, ModalService) {
    $scope.show = function() {
        ModalService.showModal({
            templateUrl: 'register.html',
            controller: "RegisterController"
        }).then(function(modal) {
            modal.element.modal();
        });
    };
});

app.controller('RegisterController', ['$scope', '$element', 'close', function($scope, $element, close) {
    $scope.register = function(user) {
        var request = angular.copy(user);
        $.ajax({
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            url: $SCRIPT_ROOT + '/register',
            data: JSON.stringify({
                first_name: user.first_name,
                last_name: user.last_name,
                email: user.email,
                password: user.password
            }),
            success: function(result) {
                console.log(result);
                if (result.email_taken) {
                    var emailField = document.getElementById('email-field');
                    emailField.setCustomValidity('Email address already in use.');
                    emailField.reportValidity();
                }
                else if (result.success) {
                    // close, but give 500ms for bootstrap to animate
                    $element.modal('hide');
                 	close(null, 500);
                }
            }
        })
    };

    $scope.close = function(result) {
        // close, but give 500ms for bootstrap to animate
     	close(result, 500);
    };
}]);
