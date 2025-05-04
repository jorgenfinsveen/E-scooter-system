import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { Location } from "../components/Location";
import { UserIdInput } from "../components/UserIdInput";
import { UnlockButton } from "../components/UnlockButton";
import { CoRideButton } from "../components/CoRideButton";

// Defines the props for the scooter data
type Scooter = {
  uuid: number;
  latitude: number;
  longtitude: number;
  status: string;
};

const RentScooter = () => {
  const [data, setData] = useState<Scooter | null>(null);
  const [activeButton, setActiveButton] = useState<boolean>(false);
  const [userId, setUserId] = useState<string>("");

  const navigate = useNavigate();
  const { scooter_id } = useParams<{ scooter_id: string }>();
  const scooter_id_num = parseInt(scooter_id || "0", 10);

  const apiUrl =
    import.meta.env.VITE_API_URL || "http://localhost:8080/api/v1/";

  /*
    useEffect(() => {
        console.log("Fetching scooter data...");
        fetch(`${apiUrl}scooter/${scooter_id_num}`)
          .then((response) => response.json())
          .then((res) => {setData(res.message); console.log("Scooter data fetched:", res);}) 
          .catch((error) => console.error('Error:', error))
    }, [apiUrl, scooter_id_num]);
    */

  useEffect(() => {
    console.log("Fetching scooter data...");

    fetch(`${apiUrl}scooter/${scooter_id_num}`)
      .then(async (response) => {
        console.log("Raw response:", response);

        const text = await response.text();
        console.log("Response as text:", text);

        try {
          const data = JSON.parse(text);
          console.log("Parsed JSON:", data);
          setData(data.message);
        } catch (err) {
          console.error("Failed to parse JSON:", err);
        }
      })
      .catch((error) => {
        console.error("Fetch failed:", error);
      });
  }, [apiUrl, scooter_id_num]);

  // Handle input changes in the UserIdInput component
  const onInputChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const cleaned = event.target.value.replace(/[^0-9]/g, "");
    setUserId(cleaned);

    // Enable the button if the input is valid
    if (cleaned.length > 0 && /^[1-9][0-9]*$/.test(cleaned)) {
      setActiveButton(true);
    } else {
      setActiveButton(false);
    }
  };

  // Handle the unlock button click
  const handleButton = async () => {
    const resp = await fetch(
      `${apiUrl}scooter/${scooter_id_num}/single-unlock?user_id=${userId}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    const data = await resp.json();

    if (resp.status === 200) {
      sessionStorage.setItem("user_id", userId);
      navigate(`/scooter/${scooter_id_num}/active`);
    } else {
      const error_type = data.redirect;
      navigate(`/error/${error_type}`);
    }
  };

  return (
    <>
      {/* Page title */}
      <h1 className="page-title">Rent this Scooter</h1>
      {/* Display the scooter's location on a map */}
      <div className="scooter-maps">
        {data ? (
          <Location lat={data.latitude} lon={data.longtitude} />
        ) : (
          <p>Loading...</p>
        )}
      </div>
      {/* Input field for the user ID */}
      <UserIdInput onInputChange={onInputChange} />
      <div className="button-section">
        <UnlockButton activeButton={activeButton} handleButton={handleButton} />
        <CoRideButton activeButton={activeButton} handleButton={handleButton} />
      </div>
    </>
  );
};

export default RentScooter;
