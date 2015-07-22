function play(id, demo){
    if(typeof demo == 'undefined') demo = '0';
    var postdata = {"id": id, "demo": demo};
    $.post('/ajax/play/', postdata, function(data) {
        console.log(data['reply']);
        //swal({ title: "Play demo", text: data['reply'], timer: 1000});
    });
    return false ;
}

var pl = {
    DO: 0,
    play: 0,
    addclip: 1,
    addData: {card:null, clip:null},
    nowData: {card:null, clip:null},

    Func: function(plid, plname) {
        if (pl.DO == pl.addclip) {
            var payload = {"pl": plid, "id": pl.addData.card, "name": pl.addData.clip};
            $.post('/playlist/addclip', payload, function(data) {
                console.log(data['reply']);
                swal({ title: "Add clip", text: data['reply'], timer: 500});
            });

            var funcs = document.getElementsByClassName('plFunc');
            for(var i=0; i<funcs.length; i++) {
                $("#plFunc-"+i).text(">");
            }
            pl.DO = null;
            return false;
        }
        else {
            var payload = {"idx": plid};
            $.post('/playlist/play', payload, function(data) {
                console.log(data['reply']);
                swal({ title: "Play list", text: data['reply']});
            });

            pl.DO = pl.play;
            return false;
        }
    },

    Play: function(plid, plname) {
            var payload = {"idx": plid};
            $.post('/playlist/play', payload, function(data) {
                swal({ title: "Play list", text: data['reply'],  timer: 500});
            });
    },

    AddClip: function(card, clip) {
        var funcs = document.getElementsByClassName('plFunc');
        for(var i=0; i<funcs.length; i++) {
            $("#plFunc-"+i).text("+");
        }
        pl.DO = pl.addclip;
        pl.addData.card = card;
        pl.addData.clip = clip;
    },

    NowPlaying: function() {
        var funcs = document.getElementsByClassName('plFunc');
        for(var i=0; i<funcs.length; i++) {
            $("#plFunc-"+i).text("+");
        }
        pl.DO = pl.addclip;
        pl.addData.card = pl.nowData.card;
        pl.addData.clip = pl.nowData.clip;
    },

    RemoveClip: function(pl, crd, cl) {
        var payload = {"pl": pl, "id": crd, "name": cl};
        $.post('/playlist/removeclip', payload, function(data) {
            console.log(data['reply']);
            swal({ title: "Remove Clip", text: data['reply']});
            location.reload();
        });
    },

    DeleteList: function(pl) {
        swal(
            {
                title: "Delete Playlist",
                text: "Are you sure?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete!",
                closeOnConfirm: false,
                closeOnCancel: true
            },
            function() {
                var payload = {"pl": pl};
                $.post('/playlist/deletelist', payload, function(data) {
                    console.log(data['reply']);
                    swal({ title: "Delete List", text: data['reply']});
                    location.href = "/";
            });
        });

    },

    Description: function(plid, name) {
        var payload = {"d": $("#plDesc").val(), "idx": plid};
        $.post('/playlist/desc', payload, function(data) {
            swal({ title: "Description", text: data['reply']});
        });


    },

    Create: function() {
        swal(
            {
                title: "Create Playlist",
                text: "Name: ",
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

                var payload = {"name": inputValue};
                $.post('/playlist/create', payload, function(data) {
                    console.log(data['reply']);
                    swal({ title: "Create Playlist", text: data['reply']});
                    location.reload();
                });

        });
    },

    Rename: function(plid, oldname) {
        swal(
            {
                title: "Rename Playlist " + oldname,
                text: "Name: ",
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

                var payload = {"name": inputValue, "idx": plid};
                $.post('/playlist/rename', payload, function(data) {
                    swal({ title: "Rename Playlist", text: data['reply']});
                    location.reload();
                });

        });
    },

    SaveOrder: function() {
        var payload = "";
        $('#plListContainer li').each(function () {
            payload += this.id + "&";
        });
        $.ajax({
            url: '/playlist/updateorder',
            data: {
                ids: payload,
                idx: $("#plistid").val()
            },
            type: 'POST',
            success: function (result) {
                console.log(result);
            },
            error: function (result) {
                console.log(result);
            }
        }); //end ajax
    }
}



function nowPlaying() {
    var payload = {}
    $.get('/ajax/nowplaying', payload, function(data) {
        if(data['id'] == "") {
            $("#nowPlaying")[0].href = "#";
            $("#nowPlaying").text("");
            $("#nowPlayingFunc").text("");
        }
        else {
            $("#nowPlaying")[0].href = "/card/" + data['id'];
            $("#nowPlaying").text("Now Playing: " + data['clip']);
            pl.nowData.card = data['id'];
            pl.nowData.clip = data['clip'];
            if(document.getElementsByClassName("plLink").length > 0)
                $("#nowPlayingFunc").text("[+]");
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

    $('[class^=reorder]').on('click', function(){
        var t   = $(this),
            row = t.closest('li');
        t.is('.reorder-up') ? row.insertBefore(row.prev()) : row.insertAfter(row.next());
        pl.SaveOrder();
    });

    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });

    $('.scrollup').click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });

}, false);

