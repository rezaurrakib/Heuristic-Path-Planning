from heuristic_visualization import Visualization
from single_track_model import Single_track_model

visualization = Visualization()
model = Single_track_model(max_phi=45, L=3, velocity=20, timestep_size=0.5)

model.set_state(0, 0, 0)

while(True):
    x_new, y_new, theta_new = model.next_state(1)
    visualization.update(x_new, y_new, theta_new)