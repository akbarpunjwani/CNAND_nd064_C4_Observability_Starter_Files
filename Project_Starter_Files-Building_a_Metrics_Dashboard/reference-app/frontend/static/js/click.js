$(document).ready(function () {

    // all custom jQuery will go here
    // http://backend.observability.svc.cluster.local
    $("#firstbutton").click(function () {
        $.ajax({
            url: "http://localhost:3003", success: function (result) {
                $("#firstbutton").toggleClass("btn-primary:focus");
                }
        });
    });

    //http://trial.observability.svc.cluster.local
    $("#secondbutton").click(function () {
        $.ajax({
            url: "http://localhost:3004", success: function (result) {
                $("#secondbutton").toggleClass("btn-primary:focus");
            }
        });
    });    
});