export const formData = async (request: Request, multiKeys: string[] = []) => {
  const result: Record<string, any> = {};
  const fd = await request.formData();
  for (const key of fd.keys()) {
    result[key] = multiKeys.includes(key) ? fd.getAll(key) : fd.get(key);
  }
  return result;
};
