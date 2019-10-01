$(function () {
    $('#search').keyup(function () {
        // called when key is pressed and a ajax request will be called in url "admincall" with JSon object with nessary details for backend
        if ($('#search').val() != "") {
            $.ajax({
                type: "POST",
                url: "admincall",
                data: {
                    'search_text': $('#search').val(),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: searchSuccess,
                dataType: 'html'
            });
        }
        else
        {  
            //  if the search input is empty
            $('#search-results').html("");
        }
    });

});

//Response of the Ajax is rendered in html 
function searchSuccess(data, textStatus, jqXHR) {
    $('#search-results').html(data);
}