import React, { useMemo } from "react";
import type { SchemaInstitution } from "~/lib/api/types";
import { EntityType } from "~/lib/api/types";
import { Source, Sources } from "~/components/molecules/sources";
import { Badge } from "~/components/ui/badge";
import { getExternalUrl } from "~/lib/link-util";
import { TextTooltip } from "~/components/molecules/text-tooltip";
import {
  Box,
  CaseSensitive,
  Database,
  Globe,
  MapPinned,
  SquareArrowOutUpRight,
  Tags,
} from "lucide-react";
import { Flag, IconText } from "~/components/molecules/misc";
import { getCountryName } from "~/lib/text-util";
import { KeywordSection } from "~/components/molecules/keyword-section";

interface InstitutionProfileProps {
  institution: SchemaInstitution;
}

export function InstitutionProfile({ institution }: InstitutionProfileProps) {
  const externalIds = useMemo(
    () => Object.keys(institution.external_id),
    [institution],
  );
  return (
    <div>
      <div className="space-y-5">
        <div className="flex justify-between items-center">
          <div className="flex space-x-2 items-center">
            {institution.image_url && (
              <img className="w-24" src={institution.image_url} />
            )}
            <div>
              <h1 className="text-3xl font-bold">{institution.name}</h1>
              {institution.acronyms && (
                <span className="text-muted-foreground">
                  {institution.acronyms.join(", ")}
                </span>
              )}
            </div>
          </div>
          <TextTooltip text="Imported at">
            <span className="ml-auto text-xs" suppressHydrationWarning>
              {new Date(institution.imported_at!).toLocaleString()}
            </span>
          </TextTooltip>
        </div>
        {institution.alternative_names && (
          <div>
            {/*TODO maybe get better icon*/}
            <IconText icon={CaseSensitive}>Alternative names</IconText>
            <ul className="pl-4">
              {institution.alternative_names.map((name) => (
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
            <Sources item={institution} />
          </div>
          <div>
            <IconText icon={Box}>Type</IconText>
            {institution.type}
          </div>
          {institution.homepage_url && (
            <div>
              <IconText icon={Globe}>Website</IconText>
              <a
                href={institution.homepage_url}
                target="_blank"
                className="link"
                rel="noreferrer"
              >
                {institution.homepage_url}
              </a>
            </div>
          )}
        </div>
        <div>
          <IconText icon={SquareArrowOutUpRight}>External IDs</IconText>
          <div className="space-x-2">
            {externalIds.map(
              (id) =>
                institution.external_id[id] && (
                  <a
                    key={id}
                    href={getExternalUrl(id, institution.external_id[id])}
                    target="_blank"
                    rel="noreferrer"
                  >
                    <Badge variant="outline" className="space-x-1">
                      <Source source={id} />
                      <span>
                        {institution.external_id[id].startsWith("http")
                          ? id
                          : institution.external_id[id]}
                      </span>
                    </Badge>
                  </a>
                ),
            )}
          </div>
        </div>
        <div className="flex space-x-10">
          {institution.country && (
            <div>
              <IconText>Country</IconText>
              <div className="flex space-x-1 items-center">
                <Flag code={institution.country} />
                <span>{getCountryName(institution.country)}</span>
              </div>
            </div>
          )}
          {institution.city && (
            <div>
              <IconText>City</IconText>
              <span>{getCountryName(institution.city)}</span>
            </div>
          )}
          {institution.region && (
            <div>
              <IconText icon={MapPinned}>City</IconText>
              <span>{getCountryName(institution.region)}</span>
            </div>
          )}
        </div>
        {institution.topic_keywords && (
          <div>
            <IconText icon={Tags}>Keywords</IconText>
            <KeywordSection
              keywords={institution.topic_keywords}
              type={EntityType.INSTITUTION}
              fieldName={"topic_keywords"}
            />
          </div>
        )}
      </div>
    </div>
  );
}
