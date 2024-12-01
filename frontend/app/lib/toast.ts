import { ExternalToast, toast } from "sonner";
import { ReactNode } from "react";

export const useToast = () => {
  return {
    success: (message: ReactNode, data?: ExternalToast) =>
      toast.success(message, { richColors: true, ...data }),
    error: (message: ReactNode, data?: ExternalToast) =>
      toast.error(message, { richColors: true, ...data }),
  };
};
