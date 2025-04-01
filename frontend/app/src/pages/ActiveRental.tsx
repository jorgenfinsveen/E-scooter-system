import { useEffect, useState } from 'react'
import { Image } from '../components/Image'
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom';
import { LockButton } from '../components/LockButton'

const ActiveRental = () => {

    const navigate = useNavigate();

    const { scooter_id } = useParams<{ scooter_id: string }>();
    const [ seconds, setSeconds ] = useState<number>(0);
    const [ userName, setUserName ] = useState<string>('');
    const [ userId, setUserId ] = useState<string>('');

    const scooter_id_num = parseInt(scooter_id || '0', 10);
    
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8080/api/v1/';

    useEffect(() => {
        if (userId === '') {
            const storedId = sessionStorage.getItem("user_id");
            if (storedId) {
                setUserId(storedId);
            }
            return; 
        }
    
        const controller = new AbortController(); 
        fetch(`${apiUrl}user/${userId}`, { signal: controller.signal })
            .then((response) => response.json())
            .then((res) => {
                if (res.message?.name) {
                    setUserName(res.message.name.split(' ')[0]);
                }
            })
            .catch((error) => {
                if (error.name !== 'AbortError') {
                    console.error('Error:', error);
                }
            });
    
        return () => controller.abort(); 
    }, [userId]);


    useEffect(() => {
        const timer = setInterval(() => {
            setSeconds((prevSeconds) => prevSeconds + 1);
        }, 1000);

        return () => clearInterval(timer);
    }, []);


    const handleButton = async () => {
        const resp = await fetch(
            `${apiUrl}scooter/${scooter_id_num}/single-lock?user_id=${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const data = await resp.json();

        if (resp.status === 200) {
            const rental_id = data.message.rental_id;
            sessionStorage.setItem("rental_id", rental_id)
            navigate(`/scooter/${scooter_id_num}/inactive`)
        } else {
            console.error('Lock failed: ' + data.message);
            alert('Lock failed');
        }
    };


    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60

    return (
        <>
            <h1 className='page-title'>Enjoy the Ride, {userName}!</h1>
            <p className='primary-paragraph'>
                Time: {hours.toString().padStart(2, '0')}:
                {minutes.toString().padStart(2, '0')}:
                {secs.toString().padStart(2, '0')}
            </p>
            <Image src="/static/scooter.gif" />
            <LockButton activeButton={true} handleButton={handleButton} />
        </>
    );
}

export default ActiveRental;
