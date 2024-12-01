import { toast } from "sonner";

export const handleError = (e: Error | Response) => {
  if (e instanceof Error) {
    toast.error("A client error has occurred!", { richColors: true });
  } else {
    toast.error("A server error has occurred!", { richColors: true });
  }
};
