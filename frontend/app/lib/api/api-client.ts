import createClient from "openapi-fetch";
import type { paths } from "~/lib/api/types";

const baseUrl =
  typeof window === "undefined"
    ? "http://127.0.0.1:8000"
    : "http://192.168.3.128:8000";

// TODO config
export const client = createClient<paths>({
  baseUrl,
});
