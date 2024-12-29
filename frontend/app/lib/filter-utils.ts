export function parseMongoFilter(mongoFilter) {
  const result = [];

  // Check if the root is $and
  if (mongoFilter["$and"]) {
    mongoFilter["$and"].forEach((subFilter) => {
      // Process each filter inside the $and array
      for (const field in subFilter) {
        if (subFilter.hasOwnProperty(field)) {
          const value = subFilter[field];
          if (typeof value === "object" && !Array.isArray(value)) {
            // Check for operators within the field's value
            for (const operator in value) {
              if (value.hasOwnProperty(operator)) {
                result.push({
                  field: field,
                  operator: operator,
                  value: value[operator],
                });
              }
            }
          } else {
            // If no operator is specified, default to $eq
            result.push({
              field: field,
              operator: "$eq", // Default operator when no operator is present
              value: value,
            });
          }
        }
      }
    });
  }

  console.log("result", result);

  return result;
}
