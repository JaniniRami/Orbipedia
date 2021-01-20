// Author GitHub: JaniniRami
var i, dt;
var marker_vector;
var satrec, positionAndVelocity, positionEci, gmst;
var positionGd, longitude, latitude, longitudeStr, latitudeStr;

var tle1 = document.getElementById('tle1').innerText;
var tle2 = document.getElementById('tle2').innerText;

var current_position = processTLE(tle1, tle2);
var points = predPoints(tle1, tle2);
var map = drawMap();
var shadow = drawShadow();

var orbit = drawOrbit(points);
var interval = setInterval(locationInterval, 1000);

function locationInterval(){
  current_position = processTLE(tle1, tle2);
  if (position != false){
    map.removeLayer(marker_vector)
    drawLiveLocation(current_position)
  }else{
    clearInterval(interval)
  }

}

// Getting live location using TLE lines.
function processTLE(tle1, tle2){
  satrec = satellite.twoline2satrec(tle1, tle2);

  positionAndVelocity = satellite.propagate(satrec, new Date());
  positionEci = positionAndVelocity.position;

  gmst = satellite.gstime(new Date());

  // Converting ECI coordinates to geodetic coordinates
  positionGd = satellite.eciToGeodetic(positionEci, gmst);

  longitude = positionGd.longitude;
  latitude  = positionGd.latitude;
  longitudeStr = satellite.degreesLong(longitude);
  latitudeStr  = satellite.degreesLat(latitude);


  if (isNaN(longitudeStr) == false || isNaN(latitudeStr) == false){
    return [longitudeStr, latitudeStr];

  }else{
    var div = document.getElementById("danger-alert");
    div.style.display = '';
    $("#danger-alert").fadeTo(6000, 500).slideUp(500, function(){
    $("#danger-alert").slideUp(500);
  });
    return false
  };
};

function predPoints(tle1, tle2){
  var points = [];
  satrec = satellite.twoline2satrec(tle1, tle2);
  // orbit for the next 90m (5400s == 90m)

  for (i = 0; i < 5400  ; i++){
    dt = new Date()
    dt.setMinutes(0)
    dt.setSeconds(dt.getSeconds() + i);
  //  console.log(dt)
    positionAndVelocity = satellite.propagate(satrec, dt);
    positionEci = positionAndVelocity.position;

    gmst = satellite.gstime(dt);
    positionGd = satellite.eciToGeodetic(positionEci, gmst);
    longitude = positionGd.longitude,
    latitude  = positionGd.latitude;

    longitudeStr = satellite.degreesLong(longitude),
    latitudeStr  = satellite.degreesLat(latitude);


    position = [longitudeStr, latitudeStr]
    points.push(position);
  }

  return points;
};

function drawLiveLocation(position){
  var features = new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.transform(position, 'EPSG:4326', 'EPSG:3857')),
    name: 'Orbital Object'
  });

  var style = new ol.style.Style({
    image: new ol.style.Icon({
      anchor: [.5, 30],
      anchorXUnits: 'fraction',
      anchorYUnits: 'pixels',
      src: "../static/img/marker.png",
    }),
  });

  features.setStyle(style);

  var vector_source = new ol.source.Vector({
    features: [features],
  });

  marker_vector = new ol.layer.Vector({
    source: vector_source,
  });
  map.addLayer(marker_vector);
}

function drawShadow(){
  var geoJSON = new GeoJSONTerminator();
  var timeLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
      features: (new ol.format.GeoJSON()).readFeatures(geoJSON, {
        featureProjection: 'EPSG:3857'
      })
    }),
    style: new ol.style.Style({
      fill: new ol.style.Fill({
        color: 'rgb(0, 0, 0)'
      }),
      stroke: null
    }),
    opacity: 0.5
  });
  map.addLayer(timeLayer);

}

function drawOrbit(points){
  var vector_source = new ol.source.Vector();
  vector_source.addFeature(createFeature(points));

  var vectorLayer = new ol.layer.Vector({
  source: vector_source,
  style: new ol.style.Style({
    stroke: new ol.style.Stroke({
      width: 4,
      color: '#1357be'
    })
  })
});
map.addLayer(vectorLayer)
}

function createFeature(points) {
  var pointsSplitted = [];
  var pointsArray = [];
  pointsSplitted.push(points[0]);
  var lastLambda = points[0][0];

  for (var i = 1; i < points.length; i++) {
    var lastPoint = points[i - 1];
    var nextPoint = points[i];
    if (Math.abs(nextPoint[0] - lastLambda) > 180) {
      var deltaX = xToValueRange(nextPoint[0] - lastPoint[0]);
      var deltaY = nextPoint[1] - lastPoint[1];
      var deltaXS = xToValueRange(180 - nextPoint[0]);
      var deltaYS;
      if (deltaX === 0) {
        deltaYS = 0;
      } else {
        deltaYS = deltaY / deltaX * deltaXS;
      }
      var sign = lastPoint[0] < 0 ? -1 : 1;
      pointsSplitted.push([180 * sign, nextPoint[1] + deltaYS]);
      pointsArray.push(pointsSplitted);
      pointsSplitted = [];
      pointsSplitted.push([-180 * sign, nextPoint[1] + deltaYS]);
    }
    pointsSplitted.push(nextPoint);
    lastLambda = nextPoint[0];
  }

  pointsArray.push(pointsSplitted);
  var geom = new ol.geom.MultiLineString(pointsArray);
  geom.transform("EPSG:4326", "EPSG:3857");
  var feature = new ol.Feature({
    geometry: geom
  });
  return feature;
}

function xToValueRange(x) {
  if (Math.abs(x) > 180) {
    var sign = x < 0 ? -1 : 1;
    return x - 2 * 180 * sign;
  } else {
    return x;
  }
}


function drawMap(){
  map = new ol.Map({
        controls: [],
        target: 'map',
        renderer: 'canvas',
        layers: [
            new ol.layer.Tile({
              source: new ol.source.OSM({
                url:'http://{a-c}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'
              })
            }),
          ],
          view: new ol.View({
            center: ol.proj.fromLonLat([0,0]),
            zoom: 2
          })
        });
  return map;
};
