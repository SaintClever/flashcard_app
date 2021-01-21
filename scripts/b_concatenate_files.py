import csv


file_names = input('\nplease provide natal tongue and romanized txt files, no extension required [ex: filename filename]: ').split()
# ex: ../data/mandarin_natal ../data/mandarin_pinyin


with open(f'{file_names[0]}.txt', 'r') as file:
    file1 = [i.strip() for i in file.readlines()]

with open(f'{file_names[1]}.txt', 'r') as file:
    file2 = [i.strip() for i in file.readlines()]

output = [f'{a}\n{b}' for a, b in zip(file1, file2)]

with open(f'{file_names[0]}_concatenated.csv', 'w') as file:
    writer = csv.writer(file)
    for i in output:
        writer.writerow([i])