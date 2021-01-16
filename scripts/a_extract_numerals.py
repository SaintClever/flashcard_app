import re


file_names = input('\ninput single or multiple files, no extension required [ex: filename filename].\nConvert txt to csv file: ').split()
# ex: ../data/mandarin_natal ../data/thai_natal

# extract characters
for file_name in file_names:
    with open(f'{file_name}.txt', 'r') as file:
        data = file.readlines()
        output = [re.sub('[0-9]', '', i).strip() for i in data]
        # print(output)


    # export characters to txt
    with open(f'{file_name}_extracted.txt', 'w') as file:
        for i in output:
            file.write(f'{i}\n')