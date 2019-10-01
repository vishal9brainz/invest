// this funtion is called when user hit delete / approve or unapprove button
function ajaxFun(id, curr_status, file_type) {
    // is curr_status is null then it is approve or unapprove button
    if (curr_status == "") {
        // ??getting current state of the card using jqery
        curr_status = $("".concat("#", String(id), "status")).val()
        // calling the AJAX with all nessary data
        $.ajax({
            type: "POST",
            url: "status",
            data: {
                'id': id,
                'status': curr_status,
                'file_type': file_type,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: searchSuccess,
            dataType: 'html'
        });

        // toggler of the state
        if (curr_status == "Approved") { new_curr_status = "UnApproved" }
        if (curr_status == "UnApproved") { new_curr_status = "Approved" }
        $("".concat("#", String(id), "status")).val(new_curr_status)
    }
    //  is it was a delete signal 
    if (curr_status == "Delete") {
        var txt;
        // asking for confirmation
        if (confirm("Are You Sure You want to delete...")) {
            // if confirmed call the using ajax  calling status funtion of bckend
            $.ajax({
                type: "POST",
                url: "status",
                data: {
                    'id': id,
                    'status': curr_status,
                    'file_type': file_type,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: searchSuccess,
                dataType: 'html'
            });
            // hidding it as it runs
            $("".concat("#", String(id), "card")).hide();
            $("".concat("#", String(id), "card")).remove();
        }

    }

};


// Response of the Ajax call 
function searchSuccess(data, textStatus, jqXHR) {
    // # data got from the response in the form of JSON 
    data = JSON.parse(data)

    // if it was a record type then redirect to previous link
    if (data["file_type"] == "record") {
        curr_url = (window.location.href).split("/");
        curr_url = curr_url.slice(0, curr_url.length - 2).join("/");
        window.location.replace(curr_url);
    }

}