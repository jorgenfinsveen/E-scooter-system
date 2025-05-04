import { Image } from "../../components/Image";

interface WeatherAbortProps {
    hours:   string;
    minutes: string;
    seconds: string;
    price:   number;
    balance: number;
}

const WeatherAbort = ({ hours, minutes, seconds, price, balance }: WeatherAbortProps) => {

    return (
        <>
            <h1 className='page-title'>It's too cold to ride!</h1>
            <Image src="/static/bad_weather.png" />
            <h2 className='summary-header'>Rental Summary</h2>
            <p className='summary-paragraph'>Time: {hours}:{minutes}:{seconds}</p>
            <p className='summary-paragraph'>Price: NOK {price},-</p>
            <p className='summary-paragraph'>Balance: NOK {balance},-</p>
        </>
    );
}

export default WeatherAbort;