import libs.pong as pong
import matplotlib.pyplot as plt

pong.init_pong()

import pickle

with open("agent.pkl", "rb") as f:
    pong.agent = pickle.load(f)
with open("state_to_id.pkl", "rb") as f:
    pong.state_to_id = pickle.load(f)

# Most megfigyelhetjük, hogyan teljesít képzett Agent
rewards, epsilon_history = pong.play_episodes(10, max_epsilon=0, min_epsilon=0, decay_rate=0, gamma=0, learn=False, viz=True, log=True)

plt.plot(epsilon_history)
plt.show()
plt.plot(rewards)
plt.show()

pong.pygame.quit() 