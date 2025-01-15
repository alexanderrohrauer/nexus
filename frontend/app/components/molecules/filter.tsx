import React, { useMemo } from "react";
import {
  BooleanInput,
  DateInput,
  InstitutionPicker,
  NumberInput,
  ResearcherPicker,
  StringInput,
  WorkPicker,
} from "~/components/molecules/filters";
import {
  FilterProvider,
  useFilterContext,
} from "~/components/context/filter-context";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuPortal,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "~/components/ui/dropdown-menu";
import { Button } from "~/components/ui/button";
import { Trash } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select";

interface DynamicFilterProps {
  fields: any[];
}
const primitives = ["string", "number", "date"];
const operators = [
  {
    value: "$eq",
    label: "Equals",
    applicableTo: [...primitives, "boolean"],
  },
  {
    value: "$ne",
    label: "Not Equals",
    applicableTo: primitives,
  },
  {
    value: "$gt",
    label: "Greater Than",
    applicableTo: primitives,
  },
  {
    value: "$lt",
    label: "Less Than",
    applicableTo: primitives,
  },
  {
    value: "$gte",
    label: "Greater Than or Equal",
    applicableTo: primitives,
  },
  {
    value: "$lte",
    label: "Less Than or Equal",
    applicableTo: primitives,
  },
  {
    value: "$in",
    label: "In",
    applicableTo: ["researcher", "institution", "work"],
  },
  { value: "$regex", label: "Matches (Regex)", applicableTo: ["string"] },
];

const flattenFields = (fields: any[], prefix = "", depth = 2) => {
  return fields.flatMap((option) => {
    if ((option.isRelation && depth > 0) || option.type === "multi") {
      return flattenFields(
        typeof option.children === "function"
          ? option.children()
          : option.children,
        prefix + option.name + ".",
        option.isRelation ? depth - 1 : depth,
      ).flat();
    } else if (!option.isRelation) {
      return { ...option, name: prefix + option.name };
    } else {
      return option;
    }
  });
};

const DynamicFilter = ({ fields }: DynamicFilterProps) => {
  const { filters, addFilter, updateFilter, removeFilter } = useFilterContext();
  const flatFields = useMemo(() => flattenFields(fields), [fields]);

  const getFieldType = (fieldName) =>
    flatFields.find((field) => field.name === fieldName)?.type || "string";
  const getApplicableOperators = (fieldType) =>
    operators.filter(
      (op) => !op.applicableTo || op.applicableTo.includes(fieldType),
    );

  const renderInputByType = (fieldType, value, onChange) => {
    switch (fieldType) {
      case "number":
        return <NumberInput value={value} onChange={onChange} />;
      case "boolean":
        return <BooleanInput value={value} onChange={onChange} />;
      case "date":
        return <DateInput value={value} onChange={onChange} />;
      case "work":
        return <WorkPicker value={value} onChange={onChange} />;
      case "researcher":
        return <ResearcherPicker value={value} onChange={onChange} />;
      case "institution":
        return <InstitutionPicker value={value} onChange={onChange} />;
      default:
        return <StringInput value={value} onChange={onChange} />;
    }
  };

  const renderAddItems = (options: any[], prefix = "", depth = 2) => {
    return options.map((option) => {
      if ((option.isRelation && depth > 0) || option.type === "multi") {
        return (
          <DropdownMenuSub key={`menu-${option.name}.${depth}`}>
            <DropdownMenuSubTrigger>{option.label}</DropdownMenuSubTrigger>
            <DropdownMenuPortal>
              <DropdownMenuSubContent className="max-h-96 overflow-y-auto">
                {renderAddItems(
                  typeof option.children === "function"
                    ? option.children()
                    : option.children,
                  prefix + option.name + ".",
                  option.isRelation ? depth - 1 : depth,
                )}
              </DropdownMenuSubContent>
            </DropdownMenuPortal>
          </DropdownMenuSub>
        );
      } else if (!option.isRelation) {
        return (
          <DropdownMenuItem
            key={`item-${option.name}.${depth}`}
            onClick={() =>
              addFilter({
                field: prefix + option.name,
                operator: null,
                value: "",
              })
            }
          >
            {option.label}
          </DropdownMenuItem>
        );
      } else {
        return null;
      }
    });
  };

  return (
    <div className="min-w-[800px] max-h-96 overflow-y-auto">
      {filters.map((filter, index) => {
        const fieldType = getFieldType(filter.field);
        const applicableOperators = getApplicableOperators(fieldType);
        filter.operator = filter.operator ?? applicableOperators[0].value;

        return (
          <div key={index} className="flex items-center mb-3 space-x-2">
            <span className="flex-1">{filter.field}</span>
            <Select
              value={filter.operator}
              onValueChange={(value) =>
                updateFilter(index, { ...filter, operator: value })
              }
            >
              <SelectTrigger className="max-w-[200px]">
                <SelectValue placeholder="Operator" />
              </SelectTrigger>
              <SelectContent>
                {applicableOperators.map((op) => (
                  <SelectItem key={op.value} value={op.value}>
                    {op.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <div>
              {renderInputByType(fieldType, filter.value, (value) =>
                updateFilter(index, { ...filter, value }),
              )}
            </div>
            <Button
              onClick={() => removeFilter(index)}
              variant="outline"
              size="icon"
            >
              <Trash />
            </Button>
          </div>
        );
      })}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="secondary">Add filter</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="max-h-96 overflow-y-auto">
          {renderAddItems(fields)}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};

interface FilterProps extends DynamicFilterProps {
  filters: any[];
  setFilters: React.Dispatch<React.SetStateAction<any[]>>;
}

const Filter = ({ filters, setFilters, ...props }: FilterProps) => (
  <FilterProvider filters={filters} setFilters={setFilters}>
    <DynamicFilter {...props} />
  </FilterProvider>
);

export default Filter;
