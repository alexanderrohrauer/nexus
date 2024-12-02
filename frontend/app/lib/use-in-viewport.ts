import { RefObject, useCallback, useEffect, useState } from "react";

export function isElementInViewport(el: Element) {
  const rect = el.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <=
      (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

export function useInViewport(ref: RefObject<Element>) {
  const [isVisible, setIsVisible] = useState(true);

  const update = useCallback(() => {
    if (ref.current) {
      setIsVisible(isElementInViewport(ref.current));
    }
  }, [ref]);

  useEffect(() => {
    ["scroll", "load", "DOMContentLoaded", "resize", "click"].forEach(
      (type) => {
        window.addEventListener(type, update);
      },
    );
    return () => {
      ["scroll", "load", "DOMContentLoaded", "resize", "click"].forEach(
        (type) => {
          window.removeEventListener(type, update);
        },
      );
    };
  }, [update]);
  return { isVisible, update };
}
