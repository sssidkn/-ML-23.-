import os

n = int(input())
input_file = open("input.txt", "w", encoding="utf-8")
counter = 0
for root, subFolder, files in os.walk("test/files"):
    for file in files:
        counter += 2
        input_file.write("test/files/" + file + " " + "test/plagiat1/" + file + "\n")
        input_file.write("test/files/" + file + " " + "test/plagiat2/" + file + "\n")
        if counter >= n:
            input_file.close()
            break
input_file.close()
