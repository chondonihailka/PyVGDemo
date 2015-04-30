js_default = r"""
function play(id, demo){
    if(typeof demo == 'undefined') demo = '0';
    var postdata = {"id": id, "demo": demo};
    $.post('/ajax/play/', postdata, function(data) {
        console.log(data['reply']);
    });
    return false ;
}

function findModel(){
    var id = prompt("Enter model id: ", "");
    location.href = "/card/" + id;
}

function gotoPage(){
    var pgno = $("#pgno").val();
    location.href = "/cards/" + pgno;
}

"""

cherryjs = r"""
"""

settingsjs = r"""
function CheckPath(path){
    var postdata = {"path": path};
    var res = false;
    $.ajax({
        type: "POST",
        url: "/settings/checkpath",
        data: postdata,
        success: function(data){
            if(data['reply'] == "true")
                res = true;
        },
        async:false
    });
    return res;
}

function CheckRegKey(key){
    var postdata = {"key": key};
    var res = false;
    $.ajax({
        type: "POST",
        url: "/settings/checkregkey",
        data: postdata,
        success: function(data){
            if(data['reply'] == "true")
                res = true;
        },
        async:false
    });
    return res;
}

$(function() {
    $("#settingsForm").submit(function() {
        var vgdata = $("#vgdata").val();
        if(CheckPath(vgdata) === false){
            $("#reply").text("Error in VGHD data directory path.");
            return false;
        }

        var vgmodels = $("#vgmodels").val();
        if(CheckPath(vgmodels) === false){
            $("#reply").text("Error in VGHD models directory path.");
            return false;
        }

        var vgexe = $("#vgexe").val();
        if(CheckPath(vgexe) === false){
            $("#reply").text("Error in VGHD executable path.");
            return false;
        }

        var winid = $("#winid").val();
        if(CheckRegKey(winid) === false){
            $("#reply").text("Error in Windows user id. Check again.");
            return false;
        }

        var postdata = {"vgdata": vgdata, "vgmodels": vgmodels, "vgexe": vgexe, "winid": winid};
        $.post('/settings/save', postdata, function(data) {
            $("#reply").html(data['reply']);
        });
        return false ;
    });
});

"""