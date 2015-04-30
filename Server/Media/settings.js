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
            swal("Error", "Error in VGHD data directory path.", "error");
            return false;
        }

        var vgmodels = $("#vgmodels").val();
        if(CheckPath(vgmodels) === false){
            swal("Error", "Error in VGHD models directory path.", "error");
            return false;
        }

        var vgexe = $("#vgexe").val();
        if(CheckPath(vgexe) === false){
            swal("Error", "Error in VGHD executable path.", "error");
            return false;
        }

        var winid = $("#winid").val();
        if(CheckRegKey(winid) === false){
            swal("Error", "Error in Windows user id. Run 'regedit.exe' and find the first child of HKEY_USERS", "error");
            return false;
        }

        var postdata = {"vgdata": vgdata, "vgmodels": vgmodels, "vgexe": vgexe, "winid": winid};
        $.post('/settings/save', postdata, function(data) {
            swal("Settings", data['reply'], "success");
        });
        return false ;
    });
});

