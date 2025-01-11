import React from "react";
import { clsx } from "clsx";

interface IconTextProps extends React.HTMLProps<HTMLDivElement> {
  icon: any;
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
      {React.createElement(icon, { size: 16, strokeWidth: 2.5 })}{" "}
      <span className="font-bold">{children}</span>
    </div>
  );
}
