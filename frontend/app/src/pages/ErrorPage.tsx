import { useState, useEffect } from "react";
import low_battery from "../assets/img/low_battery.png";
import bad_weather from "../assets/img/bad_weather.png";
import { Image } from "../components/Image";

const ErrorPage = ({ errorType }: { errorType: string }) => {
  const ErrorDict: Record<string, { message: string; image: string }> = {
    "Low Battery": {
      message:
        "The e-scooter has a low battery. Please change to another e-scooter.",
      image: low_battery,
    },
    "Bad Weather": {
      message:
        "The weather is not suitable for driving. Please try again later.",
      image: bad_weather,
    },
    "Insufficient Funds": {
      message: "You do not have enough funds to rent this e-scooter.",
      image: low_battery,
    },
    "Rental Error": {
      message:
        "There was an error while renting the e-scooter. Please try again.",
      image: low_battery,
    },
    "User Occupied": {
      message:
        "You are already renting an e-scooter. Please return it before renting another one.",
      image: low_battery,
    },
    "E-scooter Occupied": {
      message:
        "The e-scooter is currently occupied. Please try another e-scooter.",
      image: low_battery,
    },
    "E-scooter Inoperatable": {
      message: "The e-scooter is inoperable. Please try another e-scooter.",
      image: low_battery,
    },
    "User Not Found": {
      message: "The user was not found. Please try again.",
      image: low_battery,
    },
    "E-scooter Not Found": {
      message: "The e-scooter was not found. Please try again.",
      image: low_battery,
    },
    "Transaction Error": {
      message: "There was an error with the transaction. Please try again.",
      image: low_battery,
    },
  };

  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [errorImage, setErrorImage] = useState<string | null>(null);

  const setError = (type: string) => {
    if (ErrorDict[type]) {
      setErrorMessage(ErrorDict[type].message);
      setErrorImage(ErrorDict[type].image);
    } else {
      setErrorMessage("An unknown error occurred. Please try again.");
      setErrorImage(low_battery);
    }
  };

  useEffect(() => {
    setError(errorType);
  }, [errorType]);

  return (
    <div className="error-page">
      <h1 className="page-title">{errorType || "Unknown Error"}</h1>
      {errorImage && <Image src={errorImage} />}
      <p className="error-message">{errorMessage}</p>
    </div>
  );
};

export default ErrorPage;
