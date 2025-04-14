# epr_engine.py — Ethical Priority Reweighting Engine
# Author: Juntao WANG

import math

class EthicalPriorityEngine:
    def __init__(self):
        # Initial static priorities
        self.priority = {
            "safety": 0.4,
            "fairness": 0.3,
            "freedom": 0.3
        }
        self.sensitivity = {
            "safety": 1.0,
            "fairness": 0.8,
            "freedom": 0.6
        }
        self.last_updated = {
            "safety": 0,
            "fairness": 0,
            "freedom": 0
        }
        self.decay_rate = 0.03  # temporal decay

    def compute_effective_weight(self, name, t_now):
        w = self.priority[name]
        σ = self.sensitivity[name]
        Δt = t_now - self.last_updated[name]
        τ = self.decay_rate
        return w * σ * math.exp(-τ * Δt)

    def reweight_all(self, t_now):
        return {k: self.compute_effective_weight(k, t_now) for k in self.priority}

    def update(self, name, new_priority, t_now):
        self.priority[name] = new_priority
        self.last_updated[name] = t_now
