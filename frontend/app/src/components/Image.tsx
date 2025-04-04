interface ImageProps {
  src: string;
}

export function Image({ src }: ImageProps) {
  return (
    <section
      className="image-section"
      style={{ display: "flex", justifyContent: "center" }}
    >
      <img src={src} alt="Scooter" className="image" />
    </section>
  );
}
