import React, { useEffect, useRef, useState } from "react";
import { EntityType } from "~/lib/api/types";
import { Routes } from "~/routes";
import { NavLink } from "@remix-run/react";
import { clsx } from "clsx";

interface KeywordSectionProps {
  keywords: string[];
  type: EntityType;
  fieldName: string;
}

const getLink = (keyword: string, type: EntityType, fieldName: string) => {
  const filters = [{ field: fieldName, operator: "$eq", value: keyword }];
  const query = `?q=${encodeURIComponent(JSON.stringify(filters))}`;
  if (type === EntityType.WORK) {
    return Routes.Works + query;
  } else if (type === EntityType.RESEARCHER) {
    return Routes.Researchers + query;
  } else if (type === EntityType.INSTITUTION) {
    return Routes.Institutions + query;
  }
};

export function KeywordSection(props: KeywordSectionProps) {
  const [expand, setExpand] = useState(false);
  const [shouldExpand, setShouldExpand] = useState(false);
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (ref.current) {
      setShouldExpand(ref.current.scrollHeight > ref.current.clientHeight);
    }
  }, [ref, props.keywords]);

  const toggleExpand = () => setExpand(!expand);

  return (
    <div className="relative">
      {props.keywords.length ? (
        <>
          <div className={clsx(!expand && "line-clamp-5")} ref={ref}>
            {props.keywords.map((kw) => (
              <span key={kw}>
                <NavLink
                  className="link"
                  target="_blank"
                  to={getLink(kw, props.type, props.fieldName)!}
                >
                  {kw}
                </NavLink>
                {", "}
              </span>
            ))}
          </div>
          {shouldExpand && (
            <div
              className={clsx(
                "flex justify-center w-full",
                expand
                  ? "mt-2"
                  : "bg-gradient-to-t from-background pt-10 to-transparent absolute bottom-0 left-0",
              )}
            >
              <span
                className="underline hover:no-underline cursor-pointer"
                onClick={toggleExpand}
              >
                {`Show ${expand ? "less" : `all (${props.keywords.length})`}`}
              </span>
            </div>
          )}
        </>
      ) : (
        <span className="empty-state">No keywords found</span>
      )}
    </div>
  );
}
