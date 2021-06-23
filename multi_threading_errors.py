import threading

deposit = 100
N = 10000
k = 0
n = 100
J = 0


# Function to add profit to the deposit
def add_profit():
    global deposit
    for i in range(N):
        deposit = deposit + 10


# Function to deduct money from the deposit
def pay_bill():
    global deposit
    for i in range(N):
        deposit = deposit - 10


# Creating threads
for j in range(n):
    threads = []
    for unit in range(1000):
        threads.append(threading.Thread(target=add_profit))
        threads.append(threading.Thread(target=pay_bill))
     #   threads.append(threading.Timer(interval=0, function=add_profit))
     #   threads.append(threading.Timer(interval=0, function=pay_bill))
    for job in threads:
        job.start()
    for job in threads:
        job.join()
    k += deposit
    if deposit != 100:
     #   print(deposit)
        J += 1
print(f'depo = {k / n}')
print(f'from {n} iterations {J} were broken')
