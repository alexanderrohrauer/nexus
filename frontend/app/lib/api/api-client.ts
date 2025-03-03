import createClient from "openapi-fetch";
import type { paths } from "~/lib/api/types";

const baseUrl =
  typeof window === "undefined"
    ? (process.env.BACKEND_URL ?? "http://127.0.0.1:8000")
    : "http://127.0.0.1:8000";

export const client = createClient<paths>({
  baseUrl,
});
