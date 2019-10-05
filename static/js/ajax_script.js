$(function () {
    $('#search').keyup(function () {
        console.log('key press');
        // called when key is pressed and a ajax request will be called in url "search" with JSon object with nessary details for backend
        if ($('#search').val() != "") {
            $.ajax({
                type: "POST",
                url: "search",
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
            $('#search-results').html("");
        }
    });

});

//Response of the Ajax is rendered in html 
function searchSuccess(data, textStatus, jqXHR) {
    $('#search-results').html(data);
}