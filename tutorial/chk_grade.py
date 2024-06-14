score_str = input("กรอกคะแนนที่ได้: ")

# print(type(score))
score = int(score_str)

if score > 80:
    print("A")
elif score >= 75:
    print("B+")
elif score >= 70:
    print("B")
elif score >= 65:
    print("C+")
elif score >= 60:
    print("C")
else:
    print("D")
