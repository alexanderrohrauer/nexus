import langCodes from "~/json/iso-country-codes.json";

export const getCountryName = (code: string) => {
  return langCodes[code] ?? code;
};
