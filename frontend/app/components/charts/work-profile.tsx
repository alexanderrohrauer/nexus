import React, { useMemo } from "react";
import type { SchemaWorkOutput } from "~/lib/api/types";
import { EntityType } from "~/lib/api/types";
import { Source, Sources } from "~/components/molecules/sources";
import { Badge } from "~/components/ui/badge";
import { getExternalUrl } from "~/lib/link-util";
import { TextTooltip } from "~/components/molecules/text-tooltip";
import {
  Box,
  Calendar,
  CircleCheck,
  Database,
  Languages,
  LockKeyhole,
  SquareArrowOutUpRight,
  Tags,
  XCircle,
} from "lucide-react";
import { IconText } from "~/components/molecules/misc";
import { getLanguageName } from "~/lib/text-util";
import { KeywordSection } from "~/components/molecules/keyword-section";

interface WorkProfileProps {
  work: SchemaWorkOutput;
}

export function WorkProfile({ work }: WorkProfileProps) {
  const externalIds = useMemo(() => Object.keys(work.external_id), [work]);
  const workTypes = useMemo(() => Object.keys(work.type), [work]);
  return (
    <div>
      <div className="space-y-5">
        <div className="flex justify-between items-center">
          <div className="max-w-2xl">
            <h1 className="font-bold">{work.title}</h1>
            <span className="text-muted-foreground">
              {work.publication_year}
            </span>
          </div>
          <TextTooltip text="Imported at">
            <span className="ml-auto text-xs" suppressHydrationWarning>
              {new Date(work.imported_at!).toLocaleString()}
            </span>
          </TextTooltip>
        </div>
        <div className="flex space-x-10">
          <div>
            <IconText icon={Database}>Sources</IconText>
            <Sources item={work} />
          </div>
          {work.open_access !== null && (
            <div>
              <IconText icon={LockKeyhole}>Open access</IconText>
              <div className="flex space-x-1 items-center">
                {work.open_access ? (
                  <CircleCheck
                    size={20}
                    strokeWidth={2.5}
                    className="text-green-500"
                  />
                ) : (
                  <XCircle
                    size={20}
                    strokeWidth={2.5}
                    className="text-red-500"
                  />
                )}
                <span>{work.open_access ? "Yes" : "No"}</span>
              </div>
            </div>
          )}
        </div>
        <div>
          <IconText icon={SquareArrowOutUpRight}>External IDs</IconText>
          <div className="space-x-2">
            {externalIds.map(
              (id) =>
                work.external_id[id] && (
                  <a
                    key={id}
                    href={getExternalUrl(
                      id,
                      work.external_id[id],
                      EntityType.WORK,
                    )}
                    target="_blank"
                    rel="noreferrer"
                  >
                    <Badge variant="outline" className="space-x-1">
                      <Source source={id} />
                      <span>
                        {work.external_id[id].startsWith("http")
                          ? id
                          : work.external_id[id]}
                      </span>
                    </Badge>
                  </a>
                ),
            )}
          </div>
        </div>
        <div className="flex space-x-10">
          <div>
            <IconText icon={Box}>Types</IconText>
            <div className="space-x-2">
              {workTypes.map(
                (type) =>
                  work.type[type] && (
                    <Badge variant="outline" className="space-x-1">
                      <Source source={type} />
                      <span>{work.type[type]}</span>
                    </Badge>
                  ),
              )}
            </div>
          </div>
          {work.publication_date && (
            <div>
              <IconText icon={Calendar}>Publication date</IconText>
              <span suppressHydrationWarning>
                {new Date(work.publication_date).toLocaleDateString()}
              </span>
            </div>
          )}

          {work.language && (
            <div>
              <IconText icon={Languages}>Language</IconText>
              <span>{getLanguageName(work.language)}</span>
            </div>
          )}
        </div>
        {work.keywords && (
          <div>
            <IconText icon={Tags}>Keywords</IconText>
            <KeywordSection
              keywords={work.keywords}
              type={EntityType.WORK}
              fieldName={"keywords"}
            />
          </div>
        )}
      </div>
    </div>
  );
}
