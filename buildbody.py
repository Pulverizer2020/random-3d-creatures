import numpy as np
import pyrosim.pyrosim as pyrosim
import os

from bodynode import BODY_NODE
from bodyedge import BODY_EDGE

from bodynode import build_body_array
from bodynode import build_brain_array



num_segments = np.random.randint(5,10)
print("num_segments:", num_segments)

# make recussive limit num_segments - 1
snake = BODY_NODE(
                  outgoing_edges=[
                  BODY_EDGE("is_recursive")
                  ], 
                  recursive_limit=num_segments,
                  )



# print(pyrosim.Send_Cube(name=f"{3}", pos=[1,2,3] , size=[1, 2, 3]))


snake.Recursively_Generate_Body(None, parent_node_id=None)






pyrosim.Start_URDF("body.urdf")

for bodypart in build_body_array:
    # build each cube / joint
    func = bodypart[0]
    args = bodypart[1:]
    func(*args)
pyrosim.End()


pyrosim.Start_NeuralNetwork("brain100.nndf")
sensors = []
motors = []
for brainpart in build_brain_array:
    # build each sensor / hidden / motor neuron
    func = brainpart[0]
    if func == pyrosim.Send_Sensor_Neuron:
        sensors.append(brainpart)
    elif func == pyrosim.Send_Motor_Neuron:
        motors.append(brainpart)

    args = brainpart[1:]
    func(*args)

numSensorNeurons = len(sensors)
numMotorNeurons = len(motors)


# create synapses between sensor and motor neurons, fully connected
# random weights
for sensor in sensors:
    for motor in motors:
        pyrosim.Send_Synapse( sourceNeuronName = sensor[1] , targetNeuronName = motor[1] , weight = np.random.rand()*2 - 1 )


pyrosim.End()

os.system(f"python3 simulate.py GUI 100 False")