import L from "leaflet";

export const applyLeafletOptions = (options: any, map: L.Map) => {
  let firstSkipped = false;
  map.eachLayer((layer) => {
    if (firstSkipped) {
      layer.remove();
    } else {
      firstSkipped = true;
    }
  });
  // parse series
  options.series.forEach((series: any) => {
    switch (series.type) {
      case "marker":
        addMarkerSeries(series, map);
        break;
    }
  });
};

const addMarkerSeries = (series: any, map: L.Map) => {
  // TODO add correct icons
  series.data.forEach((point: any) => {
    L.marker(
      { lng: point.position[0], lat: point.position[1] },
      {
        icon: new L.Icon({
          iconUrl: "/icons/marker-icon.png",
          iconSize: [24, 36],
          iconAnchor: [12, 36],
        }),
      },
    )
      .addTo(map)
      .bindPopup(point.name ?? point.id);
  });
};
