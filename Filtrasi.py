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
result = [
    {"No": 1, "Name": 'A', 'Class': 2},
    {"No": 2, "Name": 'B', 'Class': 1},
    {"No": 3, "Name": 'C', 'Class': 3}
]

result2 = [
    {"No": 3, "Name": 'D', 'Class': 2},
    {"No": 4, "Name": 'D', 'Class': 3},
    {"No": 5, "Name": 'A', 'Class': 4}
]

result.extend(result2)  # Merging result and result2 into final_result

final_products = []

for z in result:
    if z["Class"] not in [item["Class"] for item in final_products]:
        final_products.append(z)
        print("This Content will be written")
    else:
        print("This content is already written")

print(final_products)
