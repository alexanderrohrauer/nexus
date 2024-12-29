// FilterContext.js
import React, { createContext, useContext, useState } from "react";
import { useSearchParams } from "@remix-run/react";

const FilterContext = createContext(null);

export const FilterProvider = ({ children, filters, setFilters }) => {
  const addFilter = (filter) => setFilters((prev) => [...prev, filter]);
  const updateFilter = (index, updatedFilter) => {
    setFilters((prev) => prev.map((f, i) => (i === index ? updatedFilter : f)));
  };
  const removeFilter = (index) =>
    setFilters((prev) => prev.filter((_, i) => i !== index));

  const value = { filters, addFilter, updateFilter, removeFilter };
  return (
    <FilterContext.Provider value={value}>{children}</FilterContext.Provider>
  );
};

export const useFilterState = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const qParam = searchParams.has("q")
    ? JSON.parse(decodeURIComponent(searchParams.get("q")))
    : [];
  const [filters, setFilters] = useState(qParam);
  const applyFilters = () => {
    if (filters.length > 0) {
      setSearchParams({
        ...searchParams,
        q: encodeURIComponent(JSON.stringify(filters)),
      });
    } else {
      searchParams.delete("q");
      setSearchParams(searchParams);
    }
  };
  return { filters, setFilters, applyFilters };
};

export const useFilterContext = () => useContext(FilterContext);
