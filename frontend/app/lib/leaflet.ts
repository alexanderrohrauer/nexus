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

const MARKER_SIZES = {
  "dot.svg": { iconSize: [24, 24], iconAnchor: [12, 16] },
  "marker-icon.png": { iconSize: [24, 36], iconAnchor: [12, 36] },
  "institution.png": { iconSize: [25, 38], iconAnchor: [12, 38] },
  "researcher.png": { iconSize: [25, 38], iconAnchor: [12, 38] },
};

const addMarkerSeries = (series: any, map: L.Map) => {
  const markers = [];
  const layerGroup = new L.LayerGroup();
  series.data.forEach((point: any) => {
    const latLng = L.latLng(point.position[1], point.position[0]);
    const icon = point.icon ?? "marker-icon.png";
    const marker = L.marker(latLng, {
      icon: new L.Icon({
        iconUrl: `/icons/maps/${icon}`,
        ...MARKER_SIZES[icon],
      }),
    });
    marker.on("mouseover", () => customTip(marker, point.name ?? point.id));
    marker.on("click", () => customPop(marker, point.$nexus));
    marker.addTo(layerGroup);
    markers.push(latLng);
  });
  const bounds = L.latLngBounds(markers);
  // @ts-ignore
  if (bounds.isValid() && !map.centered) {
    map.fitBounds(bounds);
    // @ts-ignore
    map.centered = true;
  }
  if (!series.showAtZoom || map.getZoom() >= series.showAtZoom) {
    layerGroup.addTo(map);
  } else {
    map.addEventListener("zoom", () => {
      if (map.getZoom() >= series.showAtZoom) {
        layerGroup.addTo(map);
      } else {
        layerGroup.remove();
      }
    });
  }
};

const addHeatmapSeries = (series: any, map: L.Map) => {
  const { data, ...config } = series.data;
  const markers = data.map((point) => L.latLng(point[0], point[1]));
  const bounds = L.latLngBounds(markers);
  // @ts-ignore
  if (bounds.isValid() && !map.centered) {
    map.fitBounds(bounds);
    // @ts-ignore
    map.centered = true;
  }

  // @ts-ignore
  L.heatLayer(data, config).addTo(map);
};
