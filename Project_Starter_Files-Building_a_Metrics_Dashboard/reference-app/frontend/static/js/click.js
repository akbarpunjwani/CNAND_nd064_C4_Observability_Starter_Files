$(document).ready(function () {

    // all custom jQuery will go here
    // http://backend.observability.svc.cluster.local
    $("#firstbutton").click(function () {
        $.ajax({
            url: "http://localhost:3003", 
            dataType: 'jsonp',
            crossDomain: true,
            headers: {
                'Access-Control-Allow-Origin': '*'
                },
            success: function (result) {
                $("#firstbutton").toggleClass("btn-primary:focus");
                },
            error: function(XMLHttpRequest, textStatus, errorThrown) { 
                $("#firstbutton").toggleClass("btn-primary:focus");
                },
        });
    });

    //http://trial.observability.svc.cluster.local
    $("#secondbutton").click(function () {
        $.ajax({
            url: "http://localhost:3004", 
            dataType: 'jsonp',
            crossDomain: true,
            headers: {
                'Access-Control-Allow-Origin': '*'
                },
            success: function (result) {
                $("#secondbutton").toggleClass("btn-primary:focus");
                },
            error: function(XMLHttpRequest, textStatus, errorThrown) { 
                $("#secondbutton").toggleClass("btn-primary:focus");
                },
        });
    });    
});