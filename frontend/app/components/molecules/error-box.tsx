import React from "react";

interface ErrorBoxProps {}

export function ErrorBox(props: ErrorBoxProps) {
  return (
    <div className="p-5 rounded-sm border-t-4 text-sm border-destructive m-3 bg-muted text-destructive">
      An error has occurred loading your data
    </div>
  );
}
