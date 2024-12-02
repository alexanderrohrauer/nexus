"use client";

import * as React from "react";
import { Check, ChevronsUpDown } from "lucide-react";

import { cn } from "~/lib/utils";
import { Button } from "~/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "~/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "~/components/ui/popover";
import { withFormikField } from "~/lib/withFormikField";

export interface ComboboxOption {
  label: string;
  value: string;
}

interface ComboboxProps {
  options: ComboboxOption[];
  placeholder?: string;
  onValueChange?: (value: string | null) => void;
  value?: string | null;
}

export function Combobox(props: ComboboxProps) {
  const [open, setOpen] = React.useState(false);

  // TODO fix combobox
  return (
    <Popover open={open} onOpenChange={setOpen}>
      <div className="relative">
        <PopoverTrigger asChild>
          <Button
            className={cn(
              "flex w-full justify-between",
              props.value === null && "text-muted-foreground",
            )}
            variant="outline"
            role="combobox"
            aria-expanded={open}
          >
            {props.value
              ? props.options.find((option) => option.value === props.value)
                  ?.label
              : props.placeholder}
            <ChevronsUpDown className="opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="p-0">
          <Command>
            <CommandInput placeholder="Search" />
            <CommandList>
              <CommandEmpty>No results found.</CommandEmpty>
              <CommandGroup>
                {props.options.map((option) => (
                  <CommandItem
                    key={option.value}
                    value={option.value}
                    keywords={[option.label]}
                    onSelect={() => {
                      props.onValueChange?.(option.value);
                      setOpen(false);
                    }}
                    className="cursor-pointer"
                  >
                    {option.label}
                    <Check
                      className={cn(
                        "ml-auto",
                        props.value === option.value
                          ? "opacity-100"
                          : "opacity-0",
                      )}
                    />
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </div>
    </Popover>
  );
}

export const ComboboxField = withFormikField(Combobox, ({ field, form }) => ({
  value: field.value,
  onValueChange: (value: ComboboxOption | null) =>
    form.setFieldValue(field.name, value),
}));
