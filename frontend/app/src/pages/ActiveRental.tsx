import { useEffect, useState } from "react";
import { Image } from "../components/Image";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { LockButton } from "../components/LockButton";
import scooter from "../assets/img/scooter.gif";

const ActiveRental = () => {
  const navigate = useNavigate(); //Hook to navigate to different routes

  const { scooter_id } = useParams<{ scooter_id: string }>(); //Extract scooter_id from URL parameters
  const [seconds, setSeconds] = useState<number>(0); //State variable to keep track of elapsed time
  const [userName, setUserName] = useState<string>(""); //State variable to store the user's name
  const [userId, setUserId] = useState<string>(""); //State variable to store the user's ID

  const { scooter_id } = useParams<{ scooter_id: string }>();

  const [seconds, setSeconds] = useState<number>(0);
  const [userName, setUserName] = useState<string>("");
  const [userId, setUserId] = useState<string>("");
  const [rentalId, setRentalId] = useState<string>("");
  const [active, setActive] = useState<boolean>(false);

  const scooter_id_num = parseInt(scooter_id || "0", 10);

  const apiUrl =
    import.meta.env.VITE_API_URL || "http://192.168.10.247:8080/api/v1/";

  useEffect(() => {
    if (userId === "") {
      const storedId = sessionStorage.getItem("user_id");
      if (storedId) {
        setUserId(storedId);
      }
      return;
    }

    const controller = new AbortController();
    fetch(`${apiUrl}user/${userId}`, { signal: controller.signal })
      .then((response) => response.json())
      .then((res) => {
        if (res.message?.name) {
          setUserName(res.message.name.split(" ")[0]);
        }
      })
      .catch((error) => {
        if (error.name !== "AbortError") {
          console.error("Error:", error);
        }
      });

    fetch(`${apiUrl}rental?user_id=${userId}`)
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        if (Array.isArray(res.message) && res.message.length > 0) {
          updateRentalId(res.message[0]);
        } else {
          console.error("Unexpected response format:", res);
        }
      })
      .catch((error) => console.error("Error:", error));

    return () => controller.abort();
  }, [userId]);

  const updateRentalId = (id: string) => {
    console.log("Rental ID:", id);
    setRentalId(id);

    if (!active) {
      setActive(true);

      const intervalId = setInterval(() => {
        fetch(`${apiUrl}rental/ok/${id}`)
          .then((response) => response.json())
          .then((res) => {
            const redirect = res.message[1];
            console.log("message: ", res.message);

            if (res.message[0] === false) {
              console.log("redirect: ", redirect);
              console.log("rentalId: ", id);
              console.log("userId: ", userId);

              clearInterval(intervalId); // Stop the interval before redirecting
              navigate(`/abort/${redirect}/${id}/${userId}`);
            } else {
              console.log("not redirect");
            }
          })
          .catch((error) => console.error("Error:", error));
      }, 3000);

      // Clear the interval when the component unmounts
      return () => clearInterval(intervalId);
    }
  };

  useEffect(() => {
    const timer = setInterval(() => {
      setSeconds((prevSeconds) => prevSeconds + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleButton = async () => {
    const resp = await fetch(
      `${apiUrl}scooter/${scooter_id_num}/single-lock?user_id=${userId}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    const data = await resp.json();

    if (resp.status === 200) {
      const rental_id = data.message.rental_id; // Extract rental ID from the response
      sessionStorage.setItem("rental_id", rental_id); // Store rental ID in session storage
      navigate(`/scooter/${scooter_id_num}/inactive`); // Navigate to the inactive rental page
    } else {
      console.error("Lock failed: " + data.message); // Log error message
      alert("Lock failed"); // Show alert if lock fails
    }
  };

  // Calculate hours, minutes, and seconds from the elapsed time
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  return (
    <>
      <h1 className="page-title">Enjoy the Ride, {userName}!</h1>
      <p className="primary-paragraph">
        Time: {hours.toString().padStart(2, "0")}:
        {minutes.toString().padStart(2, "0")}:{secs.toString().padStart(2, "0")}
      </p>
      <Image src={scooter} />
      <LockButton activeButton={true} handleButton={handleButton} />
    </>
  );
};

export default ActiveRental;

// <Image src="/static/scooter.gif" />
