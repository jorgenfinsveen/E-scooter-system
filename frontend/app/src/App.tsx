import { Routes, Route } from 'react-router-dom'
import RentScooter from './pages/RentScooter'
import ActiveRental from './pages/ActiveRental'
import InactiveRental from './pages/InactiveRental'

function App() {

	return (

    	<Routes>
    		<Route path="/scooter/:scooter_id" element={<RentScooter />} />
			<Route path="/scooter/:scooter_id/active" element={<ActiveRental />} />
			<Route path="/scooter/:scooter_id/inactive" element={<InactiveRental />} />
      	</Routes>
    )
}

export default App
