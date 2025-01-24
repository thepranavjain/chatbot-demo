import React from "react";
import "./LoadingSpinner.scss";
import { ReactComponent as LoaderIcon } from "../../assets/loader.svg";

const LoadingSpinner = () => {
  return (
    <div className="spinner">
      <LoaderIcon height={"40px"} width={"40px"} className="loader-icon" />
    </div>
  );
};

export default LoadingSpinner;
