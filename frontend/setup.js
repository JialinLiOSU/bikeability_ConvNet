
    /* initialize the map. 
    setView method: Sets the view of the map (geographical center and zoom) with the given animation options.
  
    setView( <LatLng> center, <Number> zoom?, <zoom/pan options> options? )
    */
   function pointToCircle(feature, latlng) {

    var fillColorVar = "";

    if (feature.properties.District === "1") {
      fillColorVar = "blue";
    } else if (feature.properties.District === "2") {
      fillColorVar = "red";
    } else if (feature.properties.District === "3") {
      fillColorVar = "yellow";
    } else {
      fillColorVar = "purple";
    }

    var geojsonMarkerOptions = {
      radius: 8,
      fillColor: fillColorVar,
      color: "#000",
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8
    };
    var circleMarker = L.circleMarker(latlng, geojsonMarkerOptions);
    return circleMarker;
  }
  function addPopups(feature, layer) {
    if (feature.properties && feature.properties.Location) {
      layer.bindPopup(feature.properties.Location);
    }
  }

  var map = L.map('mapId').setView([39.97, -83.0], 14);

  //replace the code below from the Plain JavaScript from the map style you choose
  //at http://leaflet-extras.github.io/leaflet-providers/preview/

  var OpenStreetMap_BlackAndWhite = L.tileLayer('http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  });

  //change the varialbe "OpenStreetMap_BlackAndWhite" according to the map style you choose
  //It is the varialbe between "var" and "= L.titleLayer(..."  in Line 27 in this script
  OpenStreetMap_BlackAndWhite.addTo(map);

  var bikesLayerGroup = L.geoJSON(bikeThefts, {
    onEachFeature: addPopups,
    pointToLayer: pointToCircle
  });
  map.addLayer(bikesLayerGroup);
  map.fitBounds(bikesLayerGroup.getBounds());