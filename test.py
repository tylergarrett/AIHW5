import hw5, random 

pulls = 10001
for i in range(0,1000):
	cost = random.randrange(0,1000,1)
	for j in range(0,10):
		print(pulls)
		pulls -= 1
		state = {
		"team-code": "eef8976e",
		"game": "phase_1",
		"pulls-left": pulls,
		"last-cost": cost,
		"last-payoff": random.randrange(0,1000,1),
		"last-metadata":0,
		}
		print(hw5.get_move(state))


state = {
"team-code": "eef8976e",
"game": "phase_2_a",
}
print(hw5.get_move(state))