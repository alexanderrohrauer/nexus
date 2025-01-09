import L from "leaflet";
import { getNexusLink } from "~/lib/link-util";

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
      case "heatmap":
        addHeatmapSeries(series, map);
        break;
    }
  });
};

function customTip(marker, content: string) {
  if (!marker.isPopupOpen()) marker.bindTooltip(content).openTooltip();
}

function customPop(marker, nexusMeta) {
  const url = getNexusLink(nexusMeta);
  if (url) window.open(url, "_blank");
}

const addMarkerSeries = (series: any, map: L.Map) => {
  // TODO add correct icons
  series.data.forEach((point: any) => {
    const marker = L.marker(
      { lng: point.position[0], lat: point.position[1] },
      {
        icon: new L.Icon({
          iconUrl: "/icons/marker-icon.png",
          iconSize: [24, 36],
          iconAnchor: [12, 36],
        }),
      },
    );
    marker.on("mouseover", () => customTip(marker, point.name ?? point.id));
    marker.on("click", () => customPop(marker, point.$nexus));
    marker.addTo(map);
  });
};

const addHeatmapSeries = (series: any, map: L.Map) => {
  const { data, ...config } = series.data;
  // @ts-ignore
  L.heatLayer(data, config).addTo(map);
};
