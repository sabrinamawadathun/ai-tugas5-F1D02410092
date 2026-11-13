import json
from pathlib import Path

FILE_KB = Path(__file__).with_name("kb_wifi.json")


def baca_basis_pengetahuan():
    """Membaca pertanyaan dan aturan dari file JSON."""
    with FILE_KB.open("r", encoding="utf-8") as file:
        return json.load(file)


def tanya_fakta(pertanyaan):
    """Mengumpulkan fakta awal dari jawaban ya/tidak pengguna."""
    fakta = set()
    print("\nJawab pertanyaan berikut dengan y (ya) atau t (tidak).")
    for item in pertanyaan:
        while True:
            jawaban = input(f"{item['tanya']} (y/t): ").strip().lower()
            if jawaban in ("y", "t"):
                if jawaban == "y":
                    fakta.add(item["fakta"])
                break
            print("Input tidak valid. Masukkan y atau t.")
    return fakta


def forward_chaining(aturan, fakta_awal):
    """Menjalankan aturan sampai tidak ada fakta/kesimpulan baru."""
    memori = set(fakta_awal)
    riwayat = []
    nomor_siklus = 1

    while True:
        ada_fakta_baru = False

        for aturan_item in aturan:
            hasil = aturan_item["maka"]

            # Aturan yang hasilnya sudah ada tidak dijalankan lagi.
            if hasil in memori:
                continue

            syarat = aturan_item["jika"]
            cocok = all(item in memori for item in syarat)

            if cocok:
                memori.add(hasil)
                riwayat.append({
                    "siklus": nomor_siklus,
                    "id": aturan_item["id"],
                    "hasil": hasil,
                    "syarat": syarat,
                    "alasan": aturan_item["alasan"],
                    "sumber": aturan_item["sumber"]
                })
                ada_fakta_baru = True

        if not ada_fakta_baru:
            break

        nomor_siklus += 1

    return memori, riwayat


def tampilkan_hasil(kb, fakta_awal, memori, riwayat):
    """Menampilkan kesimpulan beserta aturan yang menjadi alasannya."""
    hasil_aturan = {item["maka"] for item in kb["aturan"]}
    kesimpulan = [f for f in memori if f in hasil_aturan]

    print("\n" + "=" * 60)
    print(kb["judul"])
    print("=" * 60)
    print("\nFakta awal:")
    if fakta_awal:
        for fakta in sorted(fakta_awal):
            print(f"- {fakta.replace('_', ' ')}")
    else:
        print("- Tidak ada gejala yang dijawab ya.")

    print("\nProses penalaran:")
    if riwayat:
        for langkah in riwayat:
            print(f"Siklus {langkah['siklus']}: {langkah['id']} -> "
                  f"{langkah['hasil'].replace('_', ' ')}")
    else:
        print("- Tidak ada aturan yang terpenuhi.")

    print("\nKesimpulan:")
    if kesimpulan:
        for item in kesimpulan:
            print(f"- {item.replace('_', ' ').capitalize()}")
    else:
        print("- Belum ditemukan kesimpulan berdasarkan gejala yang diberikan.")

    print("\nAlasan:")
    if riwayat:
        for langkah in riwayat:
            syarat = ", ".join(x.replace("_", " ") for x in langkah["syarat"])
            print(f"- {langkah['hasil'].replace('_', ' ')} berasal dari "
                  f"{langkah['id']} (IF {syarat} THEN "
                  f"{langkah['hasil'].replace('_', ' ')}).")
            print(f"  Penjelasan: {langkah['alasan']}")
            print(f"  Sumber: {langkah['sumber']}")
    else:
        print("- Tidak ada aturan yang dapat digunakan.")

    print("\nCatatan batas keberlakuan:")
    print(kb["batas"])


def main():
    kb = baca_basis_pengetahuan()
    print("=" * 60)
    print(kb["judul"])
    print("=" * 60)
    fakta_awal = tanya_fakta(kb["pertanyaan"])
    memori, riwayat = forward_chaining(kb["aturan"], fakta_awal)
    tampilkan_hasil(kb, fakta_awal, memori, riwayat)


if __name__ == "__main__":
    main()
