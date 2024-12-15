import React, { useEffect, useMemo, useRef, useState } from "react";
import { VisualizationFrame } from "~/components/molecules/visualization-frame";
import type { SchemaVisualization } from "~/lib/api/types";
import "leaflet/dist/leaflet.css";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import L from "leaflet";
import "@luomus/leaflet-smooth-wheel-zoom";
import "leaflet-geosearch/dist/geosearch.css";
import { LeafletSearch } from "~/components/molecules/LeafletSearch";

interface VegaVisualizationProps {
  spec: any;
  data: any;
  visualization: SchemaVisualization;
}

export function LeafletVisualization(props: VegaVisualizationProps) {
  const position = [51.505, -0.09];
  const markerSeries = useMemo(
    () => props.data.filter((series) => series.type === "marker")[0],
    [props.data],
  );

  const divRef = useRef<HTMLDivElement | null>(null);
  const [height, setHeight] = useState(0);

  useEffect(() => {
    if (divRef.current) {
      setHeight(divRef.current.clientHeight);
    }
  }, [divRef]);

  return (
    <VisualizationFrame visualization={props.visualization} ref={divRef}>
      {height && (
        /* @ts-ignore*/
        <MapContainer
          center={{ lng: position[1], lat: position[0] }}
          zoom={13}
          scrollWheelZoom={false}
          // @ts-ignore
          smoothWheelZoom
          smoothSensitivity={1}
          className="w-full h-[96%]"
          style={{
            // height: props.visualization.rows * 10,
            // width: props.visualization.columns * 10,
            height,
            zIndex: 0,
          }}
        >
          <LeafletSearch />
          {/* @ts-ignore*/}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {markerSeries.data.map((marker) => (
            /* @ts-ignore*/
            <Marker
              key={marker.id}
              position={{ lng: marker.position[0], lat: marker.position[1] }}
              icon={new L.Icon({ iconUrl: "/icons/marker-icon.png" })}
            >
              {/* @ts-ignore*/}
              <Popup>{marker.name ?? marker.id}</Popup>
            </Marker>
          ))}
        </MapContainer>
      )}
    </VisualizationFrame>
  );
}
