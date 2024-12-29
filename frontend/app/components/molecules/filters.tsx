import { Input } from "~/components/ui/input";

export const StringInput = ({ value, onChange }) => (
  <Input
    type="text"
    value={value}
    onChange={(e) => onChange(e.target.value)}
    placeholder="Value"
  />
);

export const NumberInput = ({ value, onChange }) => (
  <Input
    type="number"
    value={value}
    onChange={(e) => onChange(Number(e.target.value))}
    placeholder="Value"
  />
);

export const DateInput = ({ value, onChange }) => (
  <input
    type="date"
    value={value}
    onChange={(e) => onChange(e.target.value)}
    className="p-2 border rounded w-1/4"
  />
);
