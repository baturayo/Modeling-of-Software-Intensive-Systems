# Import code for model simulation:
from pypdevs.simulator import Simulator

# Import the model to be simulated
from TrainNetwork import *
import plotly
import plotly.graph_objs as go
from tqdm import tqdm

'''Initialize train here:
TrainNetwork(name, numTracks, trackLength, numTrains, a, iat, vmax)
Name = name
numTracks = #lights (equivalent to #tracks)
trackLength = length of a single track
numTrains = The amount of trains to generate
a = (a_min, a_max) -> tuple with range for amax for trains
iat = (iat_min, iat_max) -> tuple with range for iat
vmax = maximum velocity, used in the formula's'''

def terminate_whenStateIsReached(clock, model):
    global numTrains
    if model.collector.numTrains == numTrains:
        return True
    else:
        return False


# Total Length of track is 25,000km and it is FIXED
totalTrack = 25000
numTrains = 300
x1_axis = []
y1_axis = []
x2_axis = []
y2_axis = []
x3_axis = []
y3_axis = []

# Simulate Number of Tracks
for i in tqdm(range(6, 30)):
    x1_axis.append(i)
    x2_axis.append(i)
    x3_axis.append(i)
    temp_y1 = []
    temp_y2 = []
    temp_y3 = []

    for j in range(1, 10):
        # =======================
        # Simulate with fixed set with IAT=(50, 75)
        numTracks = i
        trackLength = int(totalTrack / numTracks)
        trainnetwork = TrainNetwork(name= 'trainnetwork', numTracks=numTracks, trackLength=trackLength,
                                    numTrains=numTrains, iat=(50, 75))
        sim = Simulator(trainnetwork)
        sim.setTerminationCondition(terminate_whenStateIsReached)
        sim.setClassicDEVS()
        sim.simulate()

        # Save Simulation Data
        temp_y1.append(trainnetwork.getStatistics())

        # =======================
        # Simulate with fixed set with IAT=(25, 50)
        numTracks = i
        trackLength = int(totalTrack / numTracks)
        trainnetwork = TrainNetwork(name= 'trainnetwork', numTracks=numTracks, trackLength=trackLength,
                                    numTrains=numTrains, iat=(25, 50))
        sim = Simulator(trainnetwork)
        sim.setTerminationCondition(terminate_whenStateIsReached)
        sim.setClassicDEVS()
        sim.simulate()

        # Save Simulation Data
        temp_y2.append(trainnetwork.getStatistics())

        # =======================
        # Simulate with fixed set with IAT=(12, 25)
        numTracks = i
        trackLength = int(totalTrack / numTracks)
        trainnetwork = TrainNetwork(name= 'trainnetwork', numTracks=numTracks, trackLength=trackLength,
                                    numTrains=numTrains, iat=(12, 25))
        sim = Simulator(trainnetwork)
        sim.setTerminationCondition(terminate_whenStateIsReached)
        sim.setClassicDEVS()
        sim.simulate()

        # Save Simulation Data
        temp_y3.append(trainnetwork.getStatistics())
    y1_axis.append(temp_y1)
    y2_axis.append(temp_y2)
    y3_axis.append(temp_y3)

traces = []
print(x1_axis)
print(y1_axis)
a = True
for i in range(len(x1_axis)):

    traces.append(go.Box(
        y=y1_axis[i],
        x=[x1_axis[i]] * len(y1_axis[i]),
        showlegend=a,
        name='IAT=(50, 75)',
        marker=dict(
            color='#3D9970'
        )
    ))

    traces.append(go.Box(
        y=y2_axis[i],
        x=[x2_axis[i]] * len(y2_axis[i]),
        showlegend=a,
        name='IAT=(25, 50)',
        marker=dict(
            color='#FF4136'
        )
    ))

    traces.append(go.Box(
        y=y3_axis[i],
        x=[x3_axis[i]] * len(y3_axis[i]),
        showlegend=a,
        name='IAT=(12, 25)',
        marker=dict(
            color='#FF851B'
        )
    ))
    a = False

layout = go.Layout(
    title='Number of Track Segments Simulation Results',
    xaxis=dict(
        title='#Track Segments',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Cost',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = dict(data=traces, layout = layout)
plotly.offline.plot(fig, filename='simulation_'+str(numTrains) +'.html')
