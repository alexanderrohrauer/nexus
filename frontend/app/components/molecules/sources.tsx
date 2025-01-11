import React, { useMemo } from "react";
import { TextTooltip } from "~/components/molecules/text-tooltip";
import type { Entity } from "../../../custom-types";
import { clsx } from "clsx";

interface SourcesProps {
  item: Entity;
}

export function Sources({ item }: SourcesProps) {
  const sources = useMemo(
    () =>
      Object.keys(item)
        .filter((i) => i.endsWith("_meta") && item[i])
        .map((i) => i.replace("_meta", "")),
    [item],
  );
  return (
    <div className="text-xs flex space-x-1 items-center">
      {sources.map((source) => (
        <Source
          key={source}
          source={source}
          className="bg-muted rounded-sm border border-border"
        />
      ))}
    </div>
  );
}

export function Source({ source, className = "" }) {
  return (
    <TextTooltip text={source} key={source}>
      <img
        src={`/icons/sources/${source}.png`}
        className={clsx("h-4 w-4", className)}
      />
    </TextTooltip>
  );
}
