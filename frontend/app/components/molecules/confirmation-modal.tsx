import React, { useImperativeHandle, useRef, useState } from "react";
import { buttonVariants } from "~/components/ui/button";
import { VariantProps } from "class-variance-authority";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "~/components/ui/alert-dialog";

interface ConfirmationModalProps
  extends VariantProps<typeof buttonVariants>,
    React.PropsWithChildren {
  title?: React.ReactNode;
  description?: React.ReactNode;
  ok?: (data: any) => any;
  okText?: string;
}

export interface ConfirmationModalRef {
  trigger: (data: any) => any;
}

export const ConfirmationModal = React.forwardRef<
  ConfirmationModalRef,
  ConfirmationModalProps
>(
  (
    {
      title = "Delete",
      description,
      ok,
      variant = "default",
      okText = "OK",
      children = <div />,
    }: ConfirmationModalProps,
    ref,
  ) => {
    const [data, setData] = useState<any>(null);
    const triggerBtnRef = useRef<HTMLButtonElement | null>(null);
    const onClick = (data: any) => {
      return ok?.(data);
    };

    useImperativeHandle(ref, () => ({
      trigger: (data) => {
        setData(data);
        triggerBtnRef.current?.click();
      },
    }));

    return (
      <AlertDialog>
        <AlertDialogTrigger ref={triggerBtnRef}>{children}</AlertDialogTrigger>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{title}</AlertDialogTitle>
            <AlertDialogDescription>{description}</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={() => onClick(data)} variant={variant}>
              {okText}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    );
  },
);
