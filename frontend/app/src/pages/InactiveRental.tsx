import {  useEffect, useState } from 'react'
import { useParams } from 'react-router-dom';
import { Location } from '../components/Location';

type Scooter = {
    uuid: number  
    latitude: number
    longtitude: number
    status: string
}

type Rental = {
    rental_id: number
    user_id: number
    scooter_id: number
    active: boolean
    start_time: Date
    end_time: Date
    price: number
}

const InactiveRental = () => {

    const [data, setData] = useState<Scooter | null>(null)
    const [rental, setRental] = useState<Rental | null>(null)
    const [ userId, setUserId ] = useState<string>('');
    const [ rentalId, setRentalId ] = useState<string>('');

    const [ startTime, setStartTime ] = useState<string>('');
    const [ endTime, setEndTime ] = useState<string>('');

    const { scooter_id } = useParams<{ scooter_id: string }>();
    const scooter_id_num = parseInt(scooter_id || '0', 10);
    const [ hours, setHours ] = useState<string>('');
    const [ minutes, setMinutes ] = useState<string>('');
    const [ seconds, setSeconds ] = useState<string>('');
    const [ price, setPrice ] = useState<number>(0);
    const [ balance, setBalance ] = useState<number>(0);


    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8080/api/v1/';

    useEffect(() => {
        if (userId === '') {
            setUserId(sessionStorage.getItem("user_id") || '');
        } else {
            fetch(`${apiUrl}user/${userId}`)
            .then((response) => response.json())
            .then((res) => setBalance(res.message.funds)) 
            .catch((error) => console.error('Error:', error))
        }
    })

    useEffect(() => {
        if (userId === '') {
            const storedId = sessionStorage.getItem("user_id") || '';
            setUserId(storedId);
        } else {
            fetch(`${apiUrl}user/${userId}`)
                .then((response) => response.json())
                .then((res) => setBalance(res.message.balance)) 
                .catch((error) => console.error('Error:', error));
        }
    }, [userId, apiUrl]);


    useEffect(() => {
        fetch(`${apiUrl}scooter/${scooter_id_num}`)
          .then((response) => response.json())
          .then((res) => setData(res.message)) 
          .catch((error) => console.error('Error:', error))
    }, [apiUrl, scooter_id_num]);


    useEffect(() => {
        if (userId === '') {
            setUserId(sessionStorage.getItem("user_id") || '');
        }
        if (rentalId === '') {
            setRentalId(sessionStorage.getItem("rental_id") || '');
        }
    }, []);


    useEffect(() => {
        if (rentalId !== '') {
            fetch(`${apiUrl}rental/${rentalId}`)
                .then((response) => response.json())
                .then((res) => {
                    setRental(res.message); 
                    setStartTime(res.message[4]); 
                    setEndTime(res.message[5]);
                    setPrice(res.message[6]);
                }) 
                .catch((error) => console.error('Error:', error));
            console.log("time", rental?.start_time, 0)
        }
    }, [rentalId, apiUrl]);
    



    useEffect(() => {
        if (rental) {

            const clock_start = startTime.split('T')[1].split(':');
            const clock_end = endTime.split('T')[1].split(':');

            let hh_e_s = parseInt(clock_end[0], 10) -2 ; // GMT+2
            let mm_e_s = parseInt(clock_end[1], 10);
            let ss_e_s = parseInt(clock_end[2], 10);

            let hh_s_s = parseInt(clock_start[0], 10);
            let mm_s_s = parseInt(clock_start[1], 10);
            let ss_s_s = parseInt(clock_start[2], 10);

            let tot_e_s = (hh_e_s * 3600) + (mm_e_s * 60) + (ss_e_s * 1);
            let tot_s_s = (hh_s_s * 3600) + (mm_s_s * 60) + (ss_s_s * 1);
            let tot_s = Math.abs(tot_e_s - tot_s_s);

            let hh = (Math.floor(tot_s / 3600)).toString();
            let mm = (Math.floor((tot_s % 3600) / 60)).toString();
            let ss = (tot_s % 60).toString()

            if (parseInt(hh) < 10) {
                hh = `0${hh}`;
            } 
            if (parseInt(mm) < 10) {
                mm = `0${mm}`;
            }
            if (parseInt(ss) < 10) {
                ss = `0${ss}`;
            }

            console.log("price:", price)
    
            setHours(hh.toString());
            setMinutes(mm);
            setSeconds(ss);
        }
    });
    

    return (
        <>
            <h1 className='page-title'>Thank You!</h1>
            <div className="scooter-maps">
                { data ? (
                    <Location lat={data.latitude} lon={data.longtitude} />
                ) : (
                    <p>Loading...</p>)
                }
            </div>
            <h2 className='summary-header'>Rental Summary</h2>
            <p className='summary-paragraph'>Time: {hours}:{minutes}:{seconds}</p>
            <p className='summary-paragraph'>Price: NOK {price},-</p>
            <p className='summary-paragraph'>Balance: NOK {balance},-</p>
        </>
    );
}

export default InactiveRental