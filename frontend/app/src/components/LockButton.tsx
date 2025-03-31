import Button from '@mui/material/Button';

type ButtonProps = {
	activeButton: boolean;
	handleButton: () => void;
}


export function LockButton({activeButton, handleButton}: ButtonProps) {
    
    const BUTTON_ACTIVE = (
        <Button
          variant="contained"
          color="secondary"
          onClick={handleButton}
          style={{ width: '90vw', height: '7vh', fontSize: '1.5rem' }}
          className='button'
        >Stop Ride
        </Button>
    );

    const BUTTON_DISABLED = (
        <Button
          variant="contained"
          color="secondary"
          className='button'
          style={{ width: '90vw', height: '7vh', fontSize: '1.5rem', backgroundColor: '#ccc' }}
          
        >Stop Ride
        </Button>
    );

  return (
    <div className="button-container">
        { activeButton ? (BUTTON_ACTIVE) : (BUTTON_DISABLED) }
    </div>
  );
}