import React, { useEffect, useState } from "react";
import { Spinner } from "~/components/ui/spinner";

interface LoaderProps extends React.PropsWithChildren {
  task: any;
  once?: boolean;
}

function Loader(props: LoaderProps) {
  const [success, setSuccess] = useState(false);
  //   TODO implement error eventually
  useEffect(() => {
    if (props.task.isSuccess) {
      setSuccess(true);
    }
  }, []);
  return (
    <>
      {props.task.isLoading && props.once !== success ? (
        <Spinner className="my-4" />
      ) : (
        props.children
      )}
    </>
  );
}

export default Loader;
