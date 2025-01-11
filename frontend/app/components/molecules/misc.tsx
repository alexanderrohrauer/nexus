import React from "react";
import { clsx } from "clsx";
import { TextTooltip } from "~/components/molecules/text-tooltip";
import { getCountryName } from "~/lib/text-util";

interface IconTextProps extends React.HTMLProps<HTMLDivElement> {
  icon?: any;
}

export function IconText({
  children,
  icon,
  className,
  ...props
}: IconTextProps) {
  return (
    <div
      className={clsx("flex space-x-1 items-center mb-1", className)}
      {...props}
    >
      {icon && React.createElement(icon, { size: 16, strokeWidth: 2.5 })}{" "}
      <span className="font-bold">{children}</span>
    </div>
  );
}

export function Flag({ code, className = "" }) {
  return (
    <TextTooltip text={getCountryName(code)}>
      <img
        src={`/public/flags/${code.toLowerCase()}.png`}
        className={clsx("h-5", className)}
      />
    </TextTooltip>
  );
}
