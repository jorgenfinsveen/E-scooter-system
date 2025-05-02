//Defines the types for the coordinates
type Coordinates = {
  lat: number;
  lon: number;
};

export function Location({ lat, lon }: Coordinates) {
  // Construct the Google Maps embed URL using the provided latitude and longitude
  const src = `https://maps.google.com/maps?q=${encodeURIComponent(
    lat
  )},${encodeURIComponent(lon)}&z=15&output=embed`;

  console.log("Map src:", src);

  return (
    <section className="location-section">
      {/* Render an iframe to display the Google Map */}
      <iframe
        src={src}
        className="location-map"
        width="100%"
        height="300"
        loading="lazy"
        style={{ borderRadius: "5%", border: "0" }}
        referrerPolicy="no-referrer-when-downgrade"
      />
    </section>
  );
}
