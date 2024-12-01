export function mapParams(path: string, params: Record<string, any>) {
  for (const param in params) {
    path = path.replace("{" + param + "}", encodeURIComponent(params[param]));
  }
  return path;
}
