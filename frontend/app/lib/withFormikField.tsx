import React from "react";
import { Field, FieldProps } from "formik";

interface FormikFieldProps {
  name?: string;
}

interface FormikNullableFieldProps extends FormikFieldProps {
  nullableLabel: string;
}

type InputPropsFunction = (field: FieldProps<any, unknown>) => any;

export const withFormikField = function <T, P>(
  component: React.FC<T & FormikFieldProps>,
  inputProps?: InputPropsFunction,
) {
  // @ts-ignore
  const FormikField: React.FC<T & FormikFieldProps> & {
    Nullable: React.FC<T & FormikNullableFieldProps>;
  } = React.forwardRef<
    T & FormikFieldProps
    // @ts-ignore
  >(function (props: T & FormikFieldProps, ref) {
    return (
      <Field name={props.name}>
        {(field: FieldProps) => {
          const fieldInput = Object.assign(field.field, inputProps?.(field));

          return React.createElement(component, {
            error: field.meta.touched ? field.meta.error : undefined,
            ref: ref,
            ...fieldInput,
            ...props,
          });
        }}
      </Field>
    );
  });

  return FormikField;
};
