/**
 * Created by Gökçen on 7.4.2015.
 */


var map;
var layerGroup;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


var csrf_token;

function get_kml(date, vehicle) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    });

    data_sent = {"isodate": date.toISOString(), "vehicle_pk": vehicle};

    $.get("/routing/get_kml", data_sent,
        function (data) {
            console.log(data);
            myparser.hideDocument();
            console.log(data.processed_kml);

            if (data.state == "success") {
                console.log("Basarili!");
                //"http://localhost:8000" + data.processed_kml

                myparser = new geoXML3.parser({map: mymap});
                myparser.parse(data.processed_kml);

//               map.removeLayer(layerGroup);

                /*map.eachLayer(function (l) {
                 map.removeLayer(l);
                 });*/
//                layerGroup = L.layerGroup().addTo(map);
//                var runLayer = omnivore.kml(data.processed_kml)
//                    .on('ready', function () {
//                        map.fitBounds(runLayer.getBounds());
//                    })
//                    .addTo(layerGroup);


            }
            else {
//                alert(data.message);
            }
            csrf_token = getCookie('csrftoken')
        });
}


