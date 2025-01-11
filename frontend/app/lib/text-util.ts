import countryCodes from "~/json/iso-country-codes.json";
import langCodes from "~/json/iso-language-codes.json";

export const getCountryName = (code: string) => {
  return countryCodes[code] ?? code;
};

export const getLanguageName = (code: string) => {
  return langCodes[code.toLowerCase()] ?? code;
};
