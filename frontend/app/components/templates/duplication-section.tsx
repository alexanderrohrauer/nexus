import React, { useState } from "react";
import type {
  SchemaInstitution,
  SchemaResearcher,
  SchemaWorkOutput,
} from "~/lib/api/types";
import { Switch } from "~/components/ui/switch";
import { Label } from "~/components/ui/label";
import { mapParams } from "~/lib/links";
import { NavLink, useSearchParams } from "@remix-run/react";
import { Button } from "~/components/ui/button";
import { useMutation } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import { useToast } from "~/lib/toast";
import type { Routes } from "~/routes";

interface DuplicationSectionProps {
  entity: SchemaResearcher | SchemaWorkOutput | SchemaInstitution;
  duplicates: (SchemaResearcher | SchemaWorkOutput | SchemaInstitution)[];
  mutateUrl: string;
  renderName: (
    entity: SchemaResearcher | SchemaWorkOutput | SchemaInstitution,
  ) => string;
  route: Routes;
}

export function DuplicationSection(props: DuplicationSectionProps) {
  const defaults = props.duplicates
    .filter((e) => e.marked_for_removal)
    .map((e) => e.uuid);
  const [uuids, setUuids] = useState(defaults);
  const [searchParams] = useSearchParams();
  const toast = useToast();

  const saveMutation = useMutation({
    mutationFn: () =>
      client.PUT(props.mutateUrl as any, {
        params: { path: { uuid: props.entity.uuid } },
        body: { uuids },
      }),
    onSuccess() {
      toast.success("Successfully saved");
    },
    onError() {
      toast.error("Save failed");
    },
  });

  return (
    <div className="space-y-2">
      <div className="max-h-52 overflow-y-auto">
        {props.duplicates.map((duplicate) => (
          <div key={duplicate.uuid} className="flex">
            <div
              key={duplicate.uuid}
              className="flex flex-col items-start gap-2 whitespace-nowrap border-b p-4 text-sm leading-tight last:border-b-0 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
            >
              <div className="flex space-x-3 items-center">
                <NavLink
                  to={
                    mapParams(props.route, { uuid: duplicate.uuid }) +
                    `?${searchParams}`
                  }
                  className="font-medium"
                  target="_blank"
                >
                  {props.renderName(duplicate)}
                </NavLink>
                <div className="flex items-center space-x-2">
                  <Switch
                    checked={uuids.includes(duplicate.uuid)}
                    onCheckedChange={(checked) =>
                      checked
                        ? setUuids([...uuids, duplicate.uuid])
                        : setUuids(
                            uuids.filter((uuid) => duplicate.uuid !== uuid),
                          )
                    }
                  />
                  <Label>Duplicate?</Label>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      <Button onClick={() => saveMutation.mutateAsync()}>Save</Button>
    </div>
  );
}
