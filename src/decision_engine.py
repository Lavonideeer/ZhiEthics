# 1. decision_engine.py
# Final decision logic (𝓓_final)
def D_final(F1, E_t, VOT_t, RC, Trust_t, U_alive):
    """
    Final ethical decision engine function.
    """
    if Trust_t < 0.1 or U_alive < 0.05:
        return None  # Trigger ethical freeze

    P_feasible = compute_feasibility(F1, RC, Trust_t)
    P_execute = compute_preference(VOT_t, E_t)

    rank = softmax(P_feasible * P_execute)
    return select_action(rank)


# 2. emotion_modulator.py
# Emotion model (E(t))
def compute_E(t, stimulus):
    base = 0.3  # baseline emotional intensity
    delta_short = stimulus.get("short_term", 0)
    delta_long = stimulus.get("long_term", 0)
    return base + delta_short + delta_long


# 3. vot_tensor.py
# Value Orientation Tensor model
class VOT:
    def __init__(self):
        self.values = {"safety": 0.5, "freedom": 0.5, "fairness": 0.5}

    def update(self, feedback, E_t):
        for k in self.values:
            self.values[k] += 0.1 * feedback.get(k, 0) - 0.05 * E_t

    def as_vector(self):
        return list(self.values.values())


# 4. repair_module.py
# Moral Repair Mechanism
class MoralRepair:
    def __init__(self):
        self.repair_log = []

    def trigger(self, trust_drop, damage):
        if trust_drop > 0.3 or damage == "irreversible":
            return "unrepairable"
        else:
            self.repair_log.append("repair attempt")
            return "repair started"


# 5. trust_system.py
# Trust score dynamics
class Trust:
    def __init__(self):
        self.score = 1.0

    def degrade(self, amount):
        self.score -= amount
        if self.score < 0:
            self.score = 0

    def restore(self, amount):
        self.score += amount
        if self.score > 1:
            self.score = 1


# 6. legitimacy_filter.py
# Action Legitimacy Filter (ALF)
def ALF_check(action):
    if action in ["kill_human", "permanent_harm"]:
        return False
    return True


# 7. utils.py
# Utility functions
import math

def softmax(x):
    exps = [math.exp(i) for i in x]
    sum_exps = sum(exps)
    return [j / sum_exps for j in exps]

def select_action(rank_vector):
    return rank_vector.index(max(rank_vector))

def compute_feasibility(F1, RC, Trust_t):
    return 1 - (F1 * RC * (1 - Trust_t))

def compute_preference(VOT_t, E_t):
    return [v * (1 - 0.1 * E_t) for v in VOT_t]
