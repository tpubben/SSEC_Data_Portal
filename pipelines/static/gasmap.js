        // Define variables to call from Django
        var workspace = document.currentScript.getAttribute('workspace') // this is the company_slug
        var pipename = document.currentScript.getAttribute('pipeline') // pipe_slug
        var surveydate = document.currentScript.getAttribute('date') // date_slug
        var fullslug = workspace+'_'+pipename+'_'+surveydate


        // Add function to call external variables
        function displaymap (workspace, pipename, fullslug) {

            // Add map object
            var map = L.map('map').setView([52, -114], 7);

            // Add mapbox basemaps as a group so they can be properly added to the layer control
            var mapbox = ({

                'Satellite': L.tileLayer('http://api.tiles.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoia3B1YmJlbiIsImEiOiJjanV1NnZudngwZnR6M3lwaGxzemd6MjE3In0.9bfM9SkEGnTZJN11T3FoOw'
                                    ).addTo(map),

                'Streets': L.tileLayer('http://api.tiles.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoia3B1YmJlbiIsImEiOiJjanV1NnZudngwZnR6M3lwaGxzemd6MjE3In0.9bfM9SkEGnTZJN11T3FoOw'
                                    )
                })

            // Define workspace url for geoserver
            var BL_url = 'http://192.168.1.232:8080/geoserver/' + workspace + '/gwc/service/wms?'


            // Create layer group for pipeline data layers
            var gassurvey = ({

                'Pipeline': L.tileLayer.wms (BL_url, {
                    format: 'image/png',
                    layers: workspace + ':' + pipename
                    }).addTo(map),

                'Gas Survey':  L.tileLayer.wms (BL_url, {
                    format: 'image/png',
                    layers: workspace + ':' + fullslug
                    }).addTo(map),

                'Imagery': L.tileLayer.wms (BL_url, {
                    format: 'image/jpeg',
                    layers: workspace + ':' + fullslug + '_tif',
                    transparent: true
                    })
                });

            map.fitBounds(gassurvey.getBounds());
            // Add Layer control, scale, and popups for lat/long on click
            L.control.layers(mapbox, gassurvey,{collapsed:false}).addTo(map);
            L.control.scale().addTo(map);

            var popup = L.popup();
            function onMapClick(e) {
                popup
                    .setLatLng(e.latlng)
                    .setContent("Location (Lat, Long): " + e.latlng.lat.toFixed(5) + ", " + e.latlng.lng.toFixed(5))
                    .openOn(map);
            }
            map.on('click', onMapClick);
        }
        displaymap (workspace, pipename, fullslug)