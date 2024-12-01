import { useEffect, useState } from "react";

export const useTheme = () => {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    const mql = window.matchMedia("(prefers-color-scheme: dark)");
    setTheme(mql.matches ? "dark" : "light");

    mql.addEventListener("change", () => {
      setTheme(mql.matches ? "dark" : "light");
    });
  }, []);

  return { theme };
};
