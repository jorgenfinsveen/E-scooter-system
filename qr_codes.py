import qrcode
import os
import shutil

def main():
    ip_address = input("Skriv inn IP-adressen til serveren: ")
    num_scooters = int(input("Hvor mange scootere skal det genereres QR-koder til? "))

    qr_dir = "./qr_codes"

    if os.path.exists(qr_dir): #Sletter mappen hvis den finnes fra før slik at man ikke får dobbelt opp av QR-koder
        shutil.rmtree(qr_dir)
    os.makedirs(qr_dir)

    for scooter_id in range(1, num_scooters + 1):
        url = f"http://{ip_address}:8080/scooter/{scooter_id}/"
        qr = qrcode.make(url)
        qr_path = os.path.join(qr_dir, f"scooter_{scooter_id}.png")
        qr.save(qr_path)
        print(f"Laget QR-kode for scooter {scooter_id} -> {url}")

    # Oppdater .gitignore
    #update_gitignore(qr_dir)

def update_gitignore(folder):
    gitignore_path = ".gitignore"
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            lines = f.read().splitlines()
    else:
        lines = []

    if folder not in lines:
        with open(gitignore_path, "a") as f:
            f.write(f"\n{folder}/\n")
        print(f"La til '{folder}/' i .gitignore")

if __name__ == "__main__":
    main()
