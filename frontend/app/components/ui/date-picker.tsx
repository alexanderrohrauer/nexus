"use client";

import * as React from "react";
import { format } from "date-fns";
import { CalendarIcon } from "lucide-react";

import { cn } from "~/lib/utils";
import { Button } from "~/components/ui/button";
import { Calendar } from "~/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "~/components/ui/popover";

interface DatePickerProps {
  value: Date;
  onChange: React.Dispatch<React.SetStateAction<Date>>;
  triggerClassName?: string;
  presets?: { label: string; date: Date }[];
  disabled?: boolean;
}

export function DatePicker({
  value: date,
  onChange: setDate,
  triggerClassName,
  disabled,
  ...props
}: DatePickerProps) {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant={"outline"}
          className={cn(
            "justify-start text-left font-normal",
            !date && "text-muted-foreground",
            triggerClassName,
          )}
          disabled={disabled}
        >
          <CalendarIcon />
          {date ? format(date, "PPP") : <span>Pick a date</span>}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0 flex">
        <div>
          {props.presets.map((preset, i) => (
            <div
              key={i}
              onClick={() => setDate(preset.date)}
              className="cursor-pointer hover:bg-muted p-2 m-1 rounded-md text-sm"
            >
              {preset.label}
            </div>
          ))}
        </div>
        <Calendar
          mode="single"
          selected={date}
          onSelect={setDate}
          initialFocus
        />
      </PopoverContent>
    </Popover>
  );
}
