import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import WeatherAbort from "./abort/WeatherAbort";
import EmergencyAbort from "./abort/EmergencyAbort";

type Rental = {
    rental_id: number
    user_id: number
    scooter_id: number
    active: boolean
    start_time: Date
    end_time: Date
    price: number
}

export function AbortPage() {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://192.168.10.247:8080/api/v1/';

    const [ rental,    setRental ]    = useState<Rental | null>(null);
    const [ startTime, setStartTime ] = useState<string>('');
    const [ endTime,   setEndTime ]   = useState<string>('');
    const [ hours,     setHours ]     = useState<string>('');
    const [ minutes,   setMinutes ]   = useState<string>('');
    const [ seconds,   setSeconds ]   = useState<string>('');
    const [ price,     setPrice ]     = useState<number>(0);
    const [ balance,   setBalance ]   = useState<number>(0);

    const { redirect }  = useParams<{ redirect: string }>();
    const { rental_id } = useParams<{ rental_id: string }>();
    const { user_id }   = useParams<{ user_id: string }>();

    useEffect(() => {
        console.log("redirect: ", redirect)
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
    
            setHours(hh.toString());
            setMinutes(mm);
            setSeconds(ss);
        }
    });


    if (rental) {
        fetch(`${apiUrl}rental/${rental_id}`)
            .then((response) => response.json())
            .then((res) => {
                setRental(res.message);
                setStartTime(res.message[4]);
                setEndTime(res.message[5]);
                setPrice(res.message[6]);
            })
            .catch((error) => console.error('Error:', error));

        fetch(`${apiUrl}user/${user_id}`)
            .then((response) => response.json())
            .then((res)      => setBalance(res.message.balance))
            .catch((error)   => console.error('Error:', error));
    }

    return (
        <>
            { redirect == 'distress' ? 
                (
                    <EmergencyAbort />
                ) : (
                    <WeatherAbort 
                        hours={hours} 
                        minutes={minutes}
                        seconds={seconds}
                        price={price}
                        balance={balance}
                    />
                )
            }
        </>
    );
}
