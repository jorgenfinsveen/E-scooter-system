import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";

// Define the props for the UserIdInput component
type UserIdInputProps = {
  onInputChange: (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => void;
};

export function UserIdInput({ onInputChange }: UserIdInputProps) {
  return (
    <div className="user-id-input-container">
      {/*Component to structure the user-id form */}
      <Box
        component="form"
        sx={{ "& > :not(style)": { m: 1, width: "25ch" } }}
        noValidate
        autoComplete="off"
        className="user-id-input"
      >
        {/*Component to structure the user input */}
        <TextField
          id="outlined-basic"
          label="Enter User ID"
          variant="outlined"
          type="number"
          color="secondary"
          style={{ width: "90vw", height: "7vh", fontSize: "1.5rem" }}
          onChange={(event) => onInputChange(event)}
        />
      </Box>
    </div>
  );
}
