def middle_square(seed, iterations):
    results = []
    current = seed

    for _ in range(iterations):
        #Square the current number
        squared = current ** 2
        
        #Turn it into a squared string 
        squared_str = str(squared).zfill(8)
        
        #Grab the middle 4 digits
        middle_str = squared_str[2:6]
        
        #Save it and make it the new seed
        current = int(middle_str)
        results.append(current)

    return results
my_numbers = middle_square(seed=1234, iterations=10)
print(my_numbers)