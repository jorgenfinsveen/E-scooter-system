

export function Image({ src }: { src: string }) {
    return (
        <section className="image-section">
            <img
                src={src}
                alt="Scooter"
                className="image"
            />
        </section>
    );
}