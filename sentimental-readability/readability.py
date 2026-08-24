from cs50 import get_string

def main():
    # Kullanıcıdan metni al
    text = get_string("Text: ")

    letters = 0
    words = 1  # İlk kelimeyi saymak için 1'den başlarız
    sentences = 0

    for char in text:
        # Harf sayımı
        if char.isalpha():
            letters += 1
        # Kelime sayımı (boşluklara göre)
        elif char == " ":
            words += 1
        # Cümle sayımı (. ! ?)
        elif char in [".", "!", "?"]:
            sentences += 1

    # L: 100 kelime başına düşen ortalama harf sayısı
    # S: 100 kelime başına düşen ortalama cümle sayısı
    L = (letters / words) * 100
    S = (sentences / words) * 100

    # Coleman-Liau Formülü
    index = 0.0588 * L - 0.296 * S - 15.8
    grade = round(index)

    # Sonucu yazdır
    if grade >= 16:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {grade}")

if __name__ == "__main__":
    main()
