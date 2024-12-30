import { useInfiniteQuery } from "@tanstack/react-query";
import { client } from "~/lib/api/api-client";
import type {
  SchemaInstitution,
  SchemaResearcher,
  SchemaWork,
} from "~/lib/api/types";

interface Query {
  limit: number;
  q: string;
  search?: string;
}

export const useWorksPagination = (query: Query) =>
  useInfiniteQuery<SchemaWork[]>({
    queryKey: ["works", query],
    queryFn: ({ pageParam = 0 }) =>
      client
        .GET("/works", {
          params: {
            query: {
              limit: query.limit,
              offset: pageParam as number,
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

export const useResearchersPagination = (query: Query) =>
  useInfiniteQuery<SchemaResearcher[]>({
    queryKey: ["researchers", query],
    queryFn: ({ pageParam = 0 }) =>
      client
        .GET("/researchers", {
          params: {
            query: {
              limit: query.limit,
              offset: pageParam as number,
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

export const useInstitutionsPagination = (query: Query) =>
  useInfiniteQuery<SchemaInstitution[]>({
    queryKey: ["institutions", query],
    queryFn: ({ pageParam = 0 }) =>
      client
        .GET("/institutions", {
          params: {
            query: {
              limit: query.limit,
              offset: pageParam as number,
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
