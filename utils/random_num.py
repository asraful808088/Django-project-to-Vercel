import random
def getRandom16():
    random_number = f"{random.randint(0, 9999999999999999):016}"  
    formatted_number = " ".join(random_number[i:i+4] for i in range(0, 16, 4))
    return formatted_number


def getcvv():
    random_number = f"{random.randint(100,999)}"  
    return random_number
