import re, csv



file_names = input('\nInput single or multiple files, no extension required [ex: filename filename].\nConvert txt to csv file: ').split() # french.txt without txt 'french'

# extract characters
for file_name in file_names:
    with open(f'{file_name}.txt', 'r') as file:
        data = file.readlines()
        output = [re.sub('[0-9]', '', i).strip() for i in data]
        # print(output)


    # export characters to csv
    with open(f'{file_name}.csv', 'w') as file:
        writer = csv.writer(file)
        for i in output:
            writer.writerow([i])