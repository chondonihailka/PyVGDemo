function play(id, demo){
    if(typeof demo == 'undefined') demo = '0';
    var postdata = {"id": id, "demo": demo};
    $.post('/ajax/play/', postdata, function(data) {
        console.log(data['reply']);
        //swal({ title: "Play demo", text: data['reply'], timer: 1000});
    });
    return false ;
}

function nowPlaying() {
    var payload = {}
    $.get('/ajax/nowplaying', payload, function(data) {
        if(data['id'] == "") {
            $("#nowPlaying")[0].href = "#";
            $("#nowPlaying").text("");
        }
        else {
            $("#nowPlaying")[0].href = "/card/" + data['id'];
            $("#nowPlaying").text("Now Playing: " + data['clip']);
        }
    });
    return false;
}

function gotoPage(){
    var pgno = $("#pgno").val();
    location.href = "/cards/" + pgno;
}

function shutdown(){
    swal(
        {
            title: "Are you sure?",
            text: "This is gonna shutdown the PyVGDemo server.",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, shut it down!",
            closeOnConfirm: false,
            closeOnCancel: true
        },
        function() {
            var postdata = {"command": "/shutdown"};
            $.post('/ajax/', postdata, function(data) {
                swal("Shutdown server", data['reply'], "success");
            });
        }
    );
}

function search(what){
    swal(
        {
            title: "Search model",
            text: "Enter the model " + what + ":",
            type: "input",
            showCancelButton: true,
            closeOnConfirm: false,
            animation: "slide-from-top"
        },
        function(inputValue){
            if (inputValue === false)
                return false;
            if (inputValue === "")
            {
                swal.showInputError("You need to write something!");
                return false;
            }
            location.href = "/search/?" + what + "=" + inputValue;
        });
}

window.addEventListener('load', function(){
    setInterval(nowPlaying, 2000);
}, false);
