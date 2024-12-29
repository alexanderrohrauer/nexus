import { useInfiniteQuery } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import type { SchemaResearcher } from "~/lib/api/types";

interface ResearcherQuery {
  limit: number;
  q: string;
  search?: string;
}

export const useResearchersPagination = (query: ResearcherQuery) =>
  useInfiniteQuery<SchemaResearcher[]>({
    queryKey: ["researchers", query],
    queryFn: ({ pageParam = 0 }) =>
      client
        .GET("/researchers", {
          params: {
            query: {
              limit: query.limit,
              offset: pageParam,
              q: query.q,
              search: query.search,
            },
          },
        })
        .then((res) => res.data),
    initialPageParam: 0,
    getNextPageParam(lastPage, allPages) {
      return allPages.length * query.limit;
    },
  });
