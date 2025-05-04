import Button from "@mui/material/Button";

// Render the button based on the activeButton prop
type ButtonProps = {
  activeButton: boolean;
  handleButton: () => void;
};

export function UnlockButton({ activeButton, handleButton }: ButtonProps) {
  // Define the active button
  const BUTTON_ACTIVE = (
    <Button
      variant="contained"
      color="secondary"
      onClick={handleButton}
      style={{ width: "90vw", height: "7vh", fontSize: "1.5rem" }}
      className="button-t"
    >
      Start Ride
    </Button>
  );

  // Define the disabled button
  const BUTTON_DISABLED = (
    <Button
      variant="contained"
      color="secondary"
      disabled
      style={{ width: "90vw", height: "7vh", fontSize: "1.5rem" }}
      className="button"
    >
      Start Ride
    </Button>
  );

  // Render the button based on the activeButton prop
  return (
    <div className="button-container">
      {activeButton ? BUTTON_ACTIVE : BUTTON_DISABLED}
    </div>
  );
}
