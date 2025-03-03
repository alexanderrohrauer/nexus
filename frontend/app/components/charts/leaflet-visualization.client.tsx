import React, { useEffect, useRef } from "react";
import type {
  SchemaVisualization,
  SchemaVisualizationData,
} from "~/lib/api/types";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "@luomus/leaflet-smooth-wheel-zoom";
import "leaflet-geosearch/dist/geosearch.css";
import "leaflet.fullscreen/Control.FullScreen";
import "leaflet.fullscreen/Control.FullScreen.css";
import "leaflet.heat";
import { applyLeafletOptions } from "~/lib/leaflet";
import { OpenStreetMapProvider, SearchControl } from "leaflet-geosearch";
import { useTheme } from "~/lib/theme";

interface LeafletVisualizationProps {
  visualization: SchemaVisualization;
  options: any | undefined;
  response: SchemaVisualizationData;
}

export const LeafletVisualization = React.forwardRef(function (
  props: LeafletVisualizationProps,
  ref: React.ForwardedRef<HTMLDivElement>,
) {
  const mapRef = useRef<L.Map>();
  const { theme } = useTheme();

  useEffect(() => {
    if (ref.current && props.options && !mapRef.current) {
      const defaultOptions = {
        center: { lng: -0.09, lat: 51.505 },
        zoom: 1,
      };
      const mapOptions = props.options.map ?? defaultOptions;
      mapRef.current = new L.Map(ref.current, {
        ...mapOptions,
        scrollWheelZoom: false,
        // @ts-ignore
        smoothWheelZoom: true,
        smoothSensitivity: 1,
        fullscreenControl: true,
        fullscreenControlOptions: {
          position: "topleft",
        },
      });

      L.tileLayer(
        theme === "dark"
          ? "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}.png"
          : "https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}.png",
        {
          attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        },
      ).addTo(mapRef.current);

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
      mapRef.current.addControl(search);
    }
  }, [ref, props.options]);

  useEffect(() => {
    if (mapRef.current && props.options) {
      applyLeafletOptions(props.options, mapRef.current);
    }
  }, [mapRef, props.options]);

  return (
    <div
      ref={ref}
      className="w-full h-[96%]"
      style={{
        zIndex: 0,
      }}
    />
  );
});
