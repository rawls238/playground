from random import random
import numpy as np
from itertools import permutations

def answer_correctly(threshold):
	return random() <= threshold

def next_turn(round_num, num_teams, answered_last_correctly, ty = 'rotate'):
	if ty == 'rotate':
		return round_num % num_teams
	elif ty == 'last_correct':
		next_team = (answered_last_correctly + 1) if answered_last_correctly is not None else 0
		return next_team % num_teams


def shift(l, n):
	return l[n:] + l[:n]

def swap(arr, i, j):
	tmp = arr[i]
	arr[i] = arr[j]
	arr[j] = tmp
	return arr

teams = 8
rounds = 48
points_from_correct_answer = 1

def simulate_once(probs):
	scores = [0 for i in range(teams)]
	steal_points = [0 for i in range(teams)]
	cur_team = 0
	answered_last_correctly = None
	for i in range(rounds):
		cur_team = next_turn(i, teams, answered_last_correctly, 'rotate')
		steal = False
		while True:
			if answer_correctly(probs[cur_team]):
				answered_last_correctly = cur_team
				scores[cur_team] += points_from_correct_answer
				if steal:
					steal_points[cur_team] += points_from_correct_answer
				break
			else:
				steal = True
				cur_team = (cur_team + 1) % teams
	return np.argmax(scores)

def simulate_many(probs, num_simulations):
	winning_count = [0 for i in range(teams)]
	for i in range(num_simulations):
		winning_count[simulate_once(probs)] += 1
	dist = [float(winning_count[i]) / num_simulations for i in range(teams)]
	return dist

def insert_and_shift_with_drop(arr, idx, val):
	arr[(idx+1):] = arr[idx:(len(arr)-1)]
	arr[idx] = val
	return arr

def collect_top_winning_probabilities(probs, num_simulations, num_collect = None):
	if num_collect is None:
		num_collect = len(probs)
	top_m = [0 for i in range(num_collect)]
	top_probs = [[] for i in range(num_collect)]
	for p in probs:
		strong_team_idx = np.argmax(p)
		pr = simulate_many(p, num_simulations)[strong_team_idx]
		for i in range(len(top_m)):
			m = top_m[i]
			if pr > m:
				top_m = insert_and_shift_with_drop(top_m, i, pr)
				top_probs = insert_and_shift_with_drop(top_probs, i, p)
				break
	return (top_m, top_probs)

def optimal_ordering(arr):
	arr.sort()
	return arr[::-1]


prob_delta = 0.05
probs = [.3 + prob_delta * i for i in range(teams)]
probs = optimal_ordering(probs)
probs[1] = probs[0] - .01
probs[2] = probs[1] - .01
probs[3] = probs[2]
probs[4] = probs[3]
#print(probs)
probs = swap(probs, 1, len(probs)-1)
res = simulate_many(probs, 10000)
print(res)
#(top_m, top_probs) = collect_top_winning_probabilities(all_probs, 100, 50)
#(top_m_final, top_probs_2) = collect_top_winning_probabilities(top_probs, 10000)

