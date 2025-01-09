import React from "react";
import { Separator } from "~/components/ui/separator";

interface ProfileSectionProps extends React.PropsWithChildren {
  title: string;
}

export function ProfileSection(props: ProfileSectionProps) {
  return (
    <section>
      <div className="mb-2">
        <h1 className="text-xl font-semibold mb-1">{props.title}</h1>
        <Separator />
      </div>
      {props.children}
    </section>
  );
}
