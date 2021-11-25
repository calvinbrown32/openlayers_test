

// https://stackoverflow.com/questions/37259740/passing-variables-from-flask-to-javascript
function myFunc(vars) {
console.log(vars)
    return vars
 }

    console.log("Hello .. JS Initiated")


    var map = new ol.Map({
    target: 'map',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM()
      })
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat(),
      zoom: 8
    })
  });
