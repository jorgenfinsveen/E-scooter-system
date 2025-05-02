import { useEffect, useState } from "react";
import { Image } from "../components/Image";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { LockButton } from "../components/LockButton";

const ActiveRental = () => {
  const navigate = useNavigate(); //Hook to navigate to different routes

  const { scooter_id } = useParams<{ scooter_id: string }>(); //Extract scooter_id from URL parameters
  const [seconds, setSeconds] = useState<number>(0); //State variable to keep track of elapsed time
  const [userName, setUserName] = useState<string>(""); //State variable to store the user's name
  const [userId, setUserId] = useState<string>(""); //State variable to store the user's ID

  const scooter_id_num = parseInt(scooter_id || "0", 10); //Convert scooter_id to a number

  const apiUrl =
    import.meta.env.VITE_API_URL || "http://localhost:8080/api/v1/"; //API URL for fetching data

  // Fetch user information based on the user ID
  useEffect(() => {
    if (userId === "") {
      const storedId = sessionStorage.getItem("user_id");
      if (storedId) {
        setUserId(storedId);
      }
      return;
    }

    const controller = new AbortController(); // Controller to cancel the fetch request if needed
    fetch(`${apiUrl}user/${userId}`, { signal: controller.signal })
      .then((response) => response.json())
      .then((res) => {
        if (res.message?.name) {
          setUserName(res.message.name.split(" ")[0]); // Extract and set the user's first name
        }
      })
      .catch((error) => {
        if (error.name !== "AbortError") {
          console.error("Error:", error);
        }
      });

    return () => controller.abort();
  }, [userId]);

  // Timer to increment the elapsed time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setSeconds((prevSeconds) => prevSeconds + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Handle the lock button click
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
      {/* Display the page title with the user's name */}
      <h1 className="page-title">Enjoy the Ride, {userName}!</h1>

      {/* Display the elapsed time */}

      <p className="primary-paragraph">
        Time: {hours.toString().padStart(2, "0")}:
        {minutes.toString().padStart(2, "0")}:{secs.toString().padStart(2, "0")}
      </p>

      {/* Display an image of the scooter */}
      <Image src="/static/scooter.gif" />

      {/* Render the lock button */}
      <LockButton activeButton={true} handleButton={handleButton} />
    </>
  );
};

export default ActiveRental;
