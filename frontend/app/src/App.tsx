import { Routes, Route } from "react-router-dom";
import RentScooter from "./pages/RentScooter";
import ActiveRental from "./pages/ActiveRental";
import InactiveRental from "./pages/InactiveRental";
import ErrorPage from "./pages/ErrorPage";

function App() {
  return (
    <Routes>
      {/* Route for renting a scooter */}
      <Route path="/scooter/:scooter_id" element={<RentScooter />} />

      {/* Route for an active rental */}
      <Route path="/scooter/:scooter_id/active" element={<ActiveRental />} />

      {/* Route for an inactive rental */}
      <Route
        path="/scooter/:scooter_id/inactive"
        element={<InactiveRental />}
      />
      <Route path="/error/:error_type" element={<ErrorPage />} />
    </Routes>
  );
}

export default App;
