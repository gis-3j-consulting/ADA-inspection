require([
    "esri/Map",
    "esri/views/MapView",
    "esri/layers/FeatureLayer",
    "esri/layers/GeoJSONLayer",
    "esri/symbols/SimpleMarkerSymbol",
    "esri/symbols/SimpleFillSymbol", 
    "esri/renderers/SimpleRenderer",
    "esri/geometry/Point",
    "esri/geometry/geometryEngine",
    "esri/geometry/projection",
    "esri/Graphic",
    "esri/Basemap"
], function(Map, MapView, FeatureLayer, GeoJSONLayer, SimpleMarkerSymbol, SimpleFillSymbol, SimpleRenderer, Point, geometryEngine, projection, nearestCoordinate, Graphic, Basemap) {
    projection.load().then(function() {
        var map = new Map({
            basemap: "topo-vector"
        });

        var view = new MapView({
            container: "map",
            map: map,
            center: [-122.99184422273991, 45.596667353862095],
            zoom: 15 
        });

        function printProjection(layer) {
            console.log(`${layer.title} projection: ${layer.spatialReference.wkid}`);
        }

        var geojsonLayer = new GeoJSONLayer({
            url: "intersections.json",
            renderer: new SimpleRenderer({
                symbol: new SimpleMarkerSymbol({
                    size: 1,
                    color: "white"
                })
            })
        });

        map.add(geojsonLayer);
        geojsonLayer.when(() => printProjection(geojsonLayer));
        
        var featureLayerUrl = "https://services3.arcgis.com/pZZTDhBBLO3B9dnl/arcgis/rest/services/survey123_64d4f78251234606b2b8bfd0e29ffde6/FeatureServer/0";

        var featureLayer = new FeatureLayer({
            url: featureLayerUrl,
            outFields: ["*"],
            editable: true
        });

        map.add(featureLayer);
        featureLayer.when(() => printProjection(featureLayer));

        featureLayer.queryObjectIds().then(function(ids) {
            var maxId = Math.max(...ids);
            var nextObjectId = maxId + 1;
            document.getElementById('nextObjectId').innerText = nextObjectId;
            document.getElementById('maxId').innerText = maxId;
        });

        view.on("double-click", function(event) {
            event.stopPropagation();

            var point = new Point({
                longitude: event.mapPoint.longitude,
                latitude: event.mapPoint.latitude,
                spatialReference: { wkid: 4326 }  // WGS84
            });

            var graphic = new Graphic({
                geometry: point,
                symbol: new SimpleMarkerSymbol({
                    color: [226, 119, 40],
                    outline: {
                        color: [255, 255, 255],
                        width: 2
                    }
                })
            });

            view.graphics.add(graphic);

            geojsonLayer.queryFeatures().then(function(results) {
                if (results.features.length > 0) {
                    nearestCoordinate(results.features, point)
                        .then(function(nearestInt) {
                            if (nearestInt && nearestInt.coordinate) {
                                console.log("Nearest intersection point:", nearestInt.coordinate);
                                
                                var nearestGraphic = new Graphic({
                                    geometry: nearestInt.coordinate,
                                    symbol: {
                                        type: "simple-marker",
                                        color: [0, 255, 0],
                                        size: "10px"
                                    }
                                });
                                view.graphics.add(nearestGraphic);

                                var nearestFeature = results.features[nearestInt.index];
                                console.log("Nearest feature attributes:", nearestFeature.attributes);
                            } else {
                                console.log("No nearest intersection found");
                            }
                        })
                        .catch(function(error) {
                            console.error("Error finding nearest coordinate:", error);
                        });
                } else {
                    console.log("No features found in the layer");
                }
            }).catch(function(error) {
                console.error("Error querying features:", error);
            });
        });
    });
});
