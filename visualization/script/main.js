$("#sidebar-hide-btn").click(function () {
  animateSidebar();
  $('.mini-submenu').fadeIn();
  return false;
});


$('.mini-submenu').on('click', function () {
  animateSidebar();
  $('.mini-submenu').hide();
})

function animateSidebar() {
  $("#sidebar").animate({
    width: "toggle"
  }, 350, function () {
    map.invalidateSize();
  });
}

function switchStatus(status, line) {
  switch (status) {
    case 0:
      line.zero_count++;

      break;

    case 1:
      line.one_count++;

      break;

    case 2:
      line.two_count++;

      break;

    default:
      line.miss_count++;
  }
  line.total_count++;
}


var baseLayer = L.esri.basemapLayer('Gray')
map = L.map("map", {
  zoom: 12.5,
  zoomSnap: 0.25,
  center: [40.011829189152486, -82.91261469998747],
  layers: [baseLayer],
  zoomControl: false,
  attributionControl: false,
  maxZoom: 18
});

new L.Control.Zoom({ position: 'topright' }).addTo(map);

var arrow = L.polyline([[57, -19], [60, -12]], {}).addTo(map);
/*
var arrowHead = L.polylineDecorator(arrow, {
  patterns: [
    { offset: '100%', repeat: 0, symbol: L.Symbol.arrowHead({ pixelSize: 15, polygon: false, pathOptions: { stroke: true } }) }
  ]
}).addTo(map);*/


$(document).ready(function () {
  $('#date-input').val(("2018-02-01"))
  $('#date-pr-input').val(("2018-02-01"))
})

map.on("dragend", function (e) {
  console.log(e)
})

map.on("click", function (e) {
  // console.log(e)
})

L.control.scale({ position: "bottomleft" }).addTo(map);
var north = L.control({ position: "topright" });
north.onAdd = function (map) {
  var div = L.DomUtil.create("div", "info");
  div.id = 'north_arrow'
  div.innerHTML = '<img style="height:120px;width:auto;" src="img/north_arrow.png">';
  return div;
}
north.addTo(map);



$(function () {
  $("form").submit(function () { return false; });
});

var tran;

function zoomIn(e) {
  if (event.key === 'Enter') {
    var zoomLevel = parseFloat(e.value)
    console.log(zoomLevel)
    map.setZoom(zoomLevel);

  }
}

L.control.browserPrint({
  printModes: ["Portrait", "Landscape", "Auto", "Custom"],
  position: "topright"
}).addTo(map);


$("#snap-btn").click(function () {
  $("#status").html("Running...")

});

$("#down-btn").click(function () {

});


$("#start-btn").click(function () {
  var todayDate = $("#date-input").val().replace('-', '').replace('-', '')
  console.log(todayDate)
  var tripID = $("#trip-input").val()
  var queryURL = "http://127.0.0.1:12121/panoramas" + '?where={ "year": null}'
  console.log(queryURL)

  $.ajax({
    url: queryURL,
    type: "GET",
    beforeSend: function (xhr) {
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('X-Content-Type-Options', 'nosniff');
    },
    success: function (rawstops) {
      var stops = rawstops._items
      console.log(stops)

      for (var i = 0; i < stops.length; i++) {
        var cir = L.circle([parseFloat(stops[i].lat), parseFloat(stops[i].lon)], {
          radius: 2,
          stroke: true,
          weight: 0.2,
          color: "#000000",
          fillOpacity: 1,
          info: stops[i],
          fillColor: "#000000"
        });

        // cir.on("mouseover", function (d) {
        //   var popup = L.popup()
        //     .setLatLng([parseFloat(d.target.options.info.lat), parseFloat(d.target.options.info.lon)])
        //     .setContent("<span>Panoid ID " + d.target.options.info["panoid"] + "</span></br><span>Year: " + (d.target.options.info["year"]) + "</span></br><span>Month: " + (d.target.options.info["month"]) + "s</span>")
        //     .openOn(map);
        // })
        cir.addTo(map);

      }
    }
  });

});


function createCORSRequest(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {
    xhr.open(method, url, true);

  } else if (typeof XDomainRequest != "undefined") {
    xhr = new XDomainRequest();
    xhr.open(method, url);

  } else {
    xhr = null;

  }
  return xhr;
}
