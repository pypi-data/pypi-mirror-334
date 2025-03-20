from runqdm import runqdm

for i in runqdm(range(10)):
    sum(x ** 2 for x in range(1, 10**7))  