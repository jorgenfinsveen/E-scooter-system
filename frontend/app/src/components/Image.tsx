// Define the props for the Image component

interface ImageProps {
  src: string;
  width?: string;
  height?: string;
}

export function Image({ src, width, height }: ImageProps) {
  return (
    <section
      className="image-section"
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Render the image with optional width and height */}
      <img
        src={src}
        alt="Scooter"
        style={{
          width: width || "auto",
          height: height || "auto",
        }}
      />
    </section>
  );
}
