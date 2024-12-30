import React, { Fragment, useEffect } from "react";
import { useMap } from "react-leaflet";
import { OpenStreetMapProvider, SearchControl } from "leaflet-geosearch";
import L from "leaflet";

interface LeafletSearchProps {}

export const LeafletSearch = React.memo(function (props: LeafletSearchProps) {
  const map = useMap();
  useEffect(() => {
    // Docs: https://github.com/smeijer/leaflet-geosearch/blob/develop/src/SearchControl.ts
    // @ts-ignore
    const search = new SearchControl({
      provider: new OpenStreetMapProvider(),
      style: "bar",
      showMarker: false,
      marker: {
        icon: new L.Icon({ iconUrl: "/icons/marker-icon.png" }),
        draggable: false,
      },
    });
    map.addControl(search);
  }, [map]);
  return <Fragment></Fragment>;
});
