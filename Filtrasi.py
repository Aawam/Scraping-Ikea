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


numbers = [{"num": i} for i in range(0, 10)]
numbers.append({"num": 1})
print(numbers)
output = []
for i in numbers:
    if i["num"] not in output:
        output.append(i["num"])

print(output)
"""
final_result = [
    {"No": 1, "Name": 'A'},
    {"No": 2, "Name": 'B'},
    {"No": 3, "Name": 'C'},
    {"No": 3, "Name": 'D'},
    {"No": 4, "Name": 'D'}
]

final_products = []

for z in final_result:
    if z["Name"] not in [item["Name"] for item in final_products]:
        final_products.append(z)
    else:
        print("This content is already written")

print(final_products)