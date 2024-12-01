import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "~/components/ui/tooltip";
import React from "react";

interface TooltipDemoProps extends React.PropsWithChildren {
  text: string;
}

export function TextTooltip(props: TooltipDemoProps) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>{props.children}</TooltipTrigger>
        <TooltipContent>{props.text}</TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
