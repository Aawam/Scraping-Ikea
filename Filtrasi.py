#Membaca Data xlsx pakai panda, dibalikkan ke list of dictionaries
#Eksekusi Filtrasi Data

"""
numbers = [1,1,2,3,4,5]
check = []

for i in numbers:
    if i not in check:
        check.append(i)

numbers = [{"num" : i} for i in range(0, 10)]
numbers.append({"num": 1})
print(numbers)

output = []
for i in numbers:
    if i not in output:
    output.append(i)

print(output)
"""

numbers = [{"num": i} for i in range(0, 10)]
numbers.append({"num": 1})
print(numbers)
output = []
for i in numbers:
    if i["num"] not in output:
        output.append(i["num"])

print(output)