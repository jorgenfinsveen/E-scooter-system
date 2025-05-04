import Button from "@mui/material/Button";

// Define the props for the LockButton component
type ButtonProps = {
  activeButton: boolean; // Determines if the button is active or disabled
  handleButton: () => void; // Callback function to handle button clicks
};

export function LockButton({ activeButton, handleButton }: ButtonProps) {
  // Define the active button
  const BUTTON_ACTIVE = (
    <Button
      variant="contained"
      color="secondary"
      onClick={handleButton}
      style={{ width: "90vw", height: "7vh", fontSize: "1.5rem" }}
      className="button"
    >
      Stop Ride
    </Button>
  );

  // Define the disabled button
  const BUTTON_DISABLED = (
    <Button
      variant="contained"
      color="secondary"
      className="button"
      style={{
        width: "90vw",
        height: "7vh",
        fontSize: "1.5rem",
        backgroundColor: "#ccc",
      }}
    >
      Stop Ride
    </Button>
  );

  // Render the button based on the activeButton prop
  return (
    <div className="button-container">
      {activeButton ? BUTTON_ACTIVE : BUTTON_DISABLED}
    </div>
  );
}
