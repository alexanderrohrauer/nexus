import React, { useMemo } from "react";
import type { SchemaResearcher } from "~/lib/api/types";
import { Source, Sources } from "~/components/molecules/sources";
import { Badge } from "~/components/ui/badge";
import { getExternalUrl } from "~/lib/link-util";
import { TextTooltip } from "~/components/molecules/text-tooltip";
import {
  CaseSensitive,
  Database,
  Landmark,
  SquareArrowOutUpRight,
  Tags,
} from "lucide-react";
import { IconText } from "~/components/molecules/misc";
import { NavLink } from "@remix-run/react";
import { mapParams } from "~/lib/links";
import { Routes } from "~/routes";

interface ProfileVisualizationProps {
  researcher: SchemaResearcher;
}

export function ResearcherProfile({ researcher }: ProfileVisualizationProps) {
  const externalIds = useMemo(
    () => Object.keys(researcher.external_id),
    [researcher],
  );
  return (
    <div>
      <div className="space-y-5">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">{researcher.full_name}</h1>
          <TextTooltip text="Imported at">
            <span className="ml-auto text-xs" suppressHydrationWarning>
              {new Date(researcher.imported_at!).toLocaleString()}
            </span>
          </TextTooltip>
        </div>
        {researcher.alternative_names && (
          <div>
            {/*TODO maybe get better icon*/}
            <IconText icon={CaseSensitive}>Alternative names</IconText>
            <ul className="pl-4">
              {researcher.alternative_names.map((name) => (
                <li key={name} className="list-disc">
                  {name}
                </li>
              ))}
            </ul>
          </div>
        )}
        <div className="flex space-x-10">
          <div>
            <IconText icon={Database}>Sources</IconText>
            <Sources item={researcher} />
          </div>
          {researcher.institution && (
            <div>
              <IconText icon={Landmark}>Institution</IconText>
              <NavLink
                className="link"
                to={mapParams(Routes.Institution, {
                  uuid: researcher.institution.uuid,
                })}
                target="_blank"
              >
                {researcher.institution.name}
              </NavLink>
            </div>
          )}
        </div>
        <div>
          <IconText icon={SquareArrowOutUpRight}>External IDs</IconText>
          <div className="space-x-2">
            {externalIds.map(
              (id) =>
                researcher.external_id[id] && (
                  <a
                    href={getExternalUrl(id, researcher.external_id[id])}
                    target="_blank"
                    rel="noreferrer"
                  >
                    <Badge variant="outline" className="space-x-1">
                      <Source source={id} />
                      <span>{researcher.external_id[id]}</span>
                    </Badge>
                  </a>
                ),
            )}
          </div>
        </div>
        {researcher.topic_keywords && (
          <div>
            <IconText icon={Tags}>Keywords</IconText>
            {/*  TODO maybe add link to search after keywords*/}
            <span>
              {researcher.topic_keywords.map((kw) => (
                <React.Fragment key={kw}>
                  <span>{kw}</span>
                  {", "}
                </React.Fragment>
              ))}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
