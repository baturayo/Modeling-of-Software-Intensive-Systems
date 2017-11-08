from DriverlessTrain import DriverlessTrain
import random


bestSolution = [0,0,0]
currentSolution = [200, 0, 0]
bestScore = 10000000
count = 0

Kp = 200
Ki = 0
Kd = 0

while count < 2000:
    print(count)
    if count % 10 == 0:
        #Generate completely new initial solution
        Kp = random.randint(0, 400)
        Ki = random.randint(0, 400)
        Kd = random.randint(0, 400)
        currentSolution = [Kp, Ki, Kd]

    #Get random values to update current solution
    DeltaKp = random.randint(1, 10)
    DeltaKi = random.randint(1, 10)
    DeltaKd = random.randint(1, 10)

    #Update current solution
    currentSolution[0] += DeltaKp
    currentSolution[1] += DeltaKi
    currentSolution[2] += DeltaKd
    trainsim = DriverlessTrain("Train", currentSolution[0], currentSolution[1], currentSolution[2])
    try:
        trainsim.run(3500)
    except :
        #Deltax Too large or negative velocity
        count += 1
        Kp = random.randint(0, 400)
        Ki = random.randint(0, 400)
        Kd = random.randint(0, 400)
        currentSolution = [Kp, Ki, Kd]
        continue
    score = trainsim.getSignal("cost")[-1].value
    if score < bestScore:
        print(score)
        print(currentSolution)
        print("_____________")
        #Save new setup
        bestScore = score
        bestSolution = list(currentSolution)
    else:
        #Revert solution
        currentSolution[0] -= DeltaKp
        currentSolution[1] -= DeltaKi
        currentSolution[2] -= DeltaKd
    count += 1

print(bestSolution)
print(bestScore)