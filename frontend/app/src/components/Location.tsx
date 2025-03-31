type Coordinates = {
    lat: number
    lon: number
  }

  export function Location({ lat, lon }: Coordinates) {
    const src = `https://maps.google.com/maps?q=${encodeURIComponent(lat)},${encodeURIComponent(lon)}&z=15&output=embed`;
  
    console.log("Map src:", src);
  
    return (
      <section className="location-section">
        <iframe
          src={src}
          className="location-map"
          width="100%"
          height="300"
          loading="lazy"
          style={{ borderRadius: "5%", border: "0", filter: "invert(90%)" }}
          referrerPolicy="no-referrer-when-downgrade"
        />
      </section>
    );
  }
  