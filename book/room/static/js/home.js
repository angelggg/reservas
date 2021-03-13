
function checkAvailability(){
    start = $("#start").val();
    end = $("#end").val();
    guests = $("#guests").val();
    $.get("check-availability?start=" + start + "&end=" + end + "&guests=" + guests, function(data, status){
    html = '<table class="table">'
    for (const property in data) {
       url = "/book-form?start=" + start + "&end=" + end + "&guests=" + guests + "&type=" + property;
       if (!data[property].available){
            html += property + " Unavailable<br>";
       } else {
            html += '<th scope="row">' + property + ": " + data[property].available + " rooms available, price " + data[property].total_price +
                ' - <a href="'+ url +'">Book</a></th>';
       }
    }
    html += "</table>"
    $("#results").empty()
    $("#results").html(html)
       }
    );
  }