import csv
import sys


def main():

    # 1. Komut satırı argümanlarını kontrol et (Kullanım hatası varsa uyar)
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # 2. CSV dosyasını (veritabanını) bir listeye oku
    database = []
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)
        # STR isimlerini (AGAT, AATG vb.) sütun başlıklarından al (ilk sütun 'name' olduğu için atla)
        str_list = reader.fieldnames[1:]

    # 3. DNA dizisi (txt) dosyasını bir değişkene oku
    with open(sys.argv[2], "r") as file:
        dna_sequence = file.read()

    # 4. DNA dizisindeki her bir STR'nin en uzun ardışık tekrar sayısını bul
    # Sonuçları 'results' adlı bir sözlükte (dict) sakla
    results = {}
    for s in str_list:
        results[s] = longest_match(dna_sequence, s)

    # 5. Veritabanındaki profilleri bulunan sonuçlarla karşılaştır
    for person in database:
        match = True
        for s in str_list:
            # CSV'den gelen veriler metindir (str), sayıya (int) çevirerek karşılaştır
            if int(person[s]) != results[s]:
                match = False
                break

        # Eğer tüm STR değerleri eşleşirse ismi yazdır ve programı bitir
        if match:
            print(person["name"])
            return

    # Eğer hiçbir eşleşme bulunamazsa
    print("No match")


def longest_match(sequence, subsequence):
    """Sequence içinde subsequence'ın en uzun ardışık tekrar sayısını döndürür."""

    # Değişkenleri başlat
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Her karakteri kontrol ederek en uzun ardışık tekrarı bul
    for i in range(sequence_length):

        # Ardışık tekrar sayısını başlat
        count = 0

        # Bir eşleşme bulduğunda peş peşe kaç tane olduğunu say
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length

            if sequence[start:end] == subsequence:
                count += 1
            else:
                break

        # Bulunan en uzun değeri güncelle
        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()
