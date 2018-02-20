from DriverlessTrain import *

cbd = DriverlessTrain("number_gen", 200, 0, 0)
cbd.run(3500)
print("The cost for the driverless train with parameters (200,0,0): " + str(cbd.getSignal("cost")[-1].value))

times = []
output = []
times2 = []
output2 = []

times3 = []
output3 = []
times4 = []
output4 = []

for timeValuePair in cbd.getSignal("Velocity"):
    times.append(timeValuePair.time)
    times2.append(timeValuePair.time)
    output.append(timeValuePair.value)
    if timeValuePair.time < 100:
        output2.append(0)
    elif timeValuePair.time < 1600:
        output2.append(10)
    elif timeValuePair.time < 2000:
        output2.append(4)
    elif timeValuePair.time < 2600:
        output2.append(14)
    else:
        output2.append(6)

for timeValuePair in cbd.getSignal("XPerson"):
    times3.append(timeValuePair.time)
    times4.append(timeValuePair.time)
    output3.append(timeValuePair.value)

for timeValuePair in cbd.getSignal("acceleration"):
    output4.append(timeValuePair.value)



#Plot
output_file("./Velocity.html", title="Kinetic Energy Calculations")
p = figure(title="Ideal and actual velocity of train(200,0,0)", x_axis_label='t', y_axis_label='m/s')
p.line(times, output , legend="Actual Velocity", line_color="blue")
p.line(times2, output2 , legend="Target Velocity", line_color="red")
show(p)

#Plot
output_file("./DeltaX.html", title="Kinetic Energy Calculations")
q = figure(title="Even Numbers", x_axis_label='t')
q.line(times3, output3, legend="People displacement(m)", line_color="red")
q.line(times4, output4, legend="Train acceleration(m/s^2)", line_color="blue")
show(q)