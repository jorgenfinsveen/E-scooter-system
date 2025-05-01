import ambulance from "../../assets/img/ambulance.gif";

const EmergencyAbort = () => {

    return (
        <>
            <h1 className='page-title'>Ambulance is on the way.</h1>
            <section 
                className='ambulance-section'
                style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}
            >
                <img
                    src={ambulance}
                    alt='Ambulance'
                />
            </section>
            <p className='primary-paragraph'>
                Stay where you are. 
                The emergency services has been informed of your whereabouts.
            </p>
        </>
    );
}

export default EmergencyAbort;