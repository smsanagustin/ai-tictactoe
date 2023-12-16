original_list = [1,2,3,4, ""]
list_copy = []
for i in range(len(original_list)):
    list_copy.append(original_list[i])
    
original_list[0] = 5
print(original_list)
print(list_copy)