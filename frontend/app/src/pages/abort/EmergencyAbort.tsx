import ambulance from "../../assets/img/ambulance.gif";

const EmergencyAbort = () => {

    return (
        <>
            <h1 className='page-title emergency'>Ambulance is on the way.</h1>
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
                    className='ambulance-image'
                />
            </section>
            <p className='primary-paragraph emergency' style={{ fontWeight: 'bolder' }}>
                Stay where you are. <br/> <br/>
                The emergency services has been informed of your whereabouts.
            </p>
        </>
    );
}

export default EmergencyAbort;