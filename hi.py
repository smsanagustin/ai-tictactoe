def alterList(list):
    # make a copy of the list to avoid altering the original
    new_list = []
    for i in range(len(list)):
        new_list.append(list[i]) 
    new_list.append(1)
    print(list)
    print(new_list)
    
my_list = [4,3,2]
alterList(my_list)
print(my_list)