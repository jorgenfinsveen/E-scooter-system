import Button from "@mui/material/Button";

type CoRideButtonProps = {
  activeButton: boolean; // Determines if the button is active or disabled
  handleButton: () => void; // Callback for when the button is clicked
};

export function CoRideButton({
  activeButton,
  handleButton,
}: CoRideButtonProps) {
  const BUTTON_ACTIVE = (
    <Button
      variant="contained"
      color="secondary"
      onClick={handleButton}
      style={{ width: "90vw", height: "7vh", fontSize: "1.5rem" }}
      className="button-t"
    >
      Start Co-Ride
    </Button>
  );

  const BUTTON_DISABLED = (
    <Button
      variant="contained"
      color="secondary"
      disabled
      style={{ width: "90vw", height: "7vh", fontSize: "1.5rem" }}
      className="button"
    >
      Start Co-Ride
    </Button>
  );

  return (
    <div className="button-container">
      {activeButton ? BUTTON_ACTIVE : BUTTON_DISABLED}
    </div>
  );
}
