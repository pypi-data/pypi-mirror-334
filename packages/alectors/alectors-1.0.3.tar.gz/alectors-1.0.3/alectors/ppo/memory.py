import torch

class Memory:
    def __init__(
        self,
        batch_size
    ):
        self.batch_size = batch_size

        self.states = []
        self.actions= []
        self.probs = []
        self.vals = []
        self.rewards = []
        self.dones = []

    def recall(self):
        n_states = len(self.states)
        indices = torch.randperm(n_states)
        batches = [
            indices[i:i + self.batch_size]
            for i in range(0, n_states, self.batch_size)
        ]

        return self.states, \
            self.actions, \
            self.probs, \
            self.vals, \
            self.rewards, \
            self.dones, \
            batches[0]

    
    def store(
        self,
        state,
        action,
        prob,
        val,
        reward,
        done
    ):
        self.states.append(state)
        self.actions.append(action)
        self.probs.append(prob)
        self.vals.append(val)
        self.rewards.append(reward)
        self.dones.append(done)

    def clear(self):
        self.states = []
        self.actions
        self.probs = []
        self.vals = []
        self.rewards = []
        self.dones = []
