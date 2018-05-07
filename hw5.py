# Tyler Garrett and Ben Kellogg
# hw5.py

# Imports
import json
import random,copy,math,decimal,statistics
import scipy.stats

# Team declaration
TEAM_NAME = "Better_Than_Alexa" #Pick a team name
MEMBERS = ["tjg3ea","brk7vu"] #Include a list of your members’ UVA IDs

# Load and Save data for use later
def load_data():
    f_name = TEAM_NAME + ".json"
    try:
        return json.loads(open(f_name).read())
    except:
        return {}

def save_data(info):
    f_name = TEAM_NAME + ".json"
    f = open(f_name,"w")
    f.write(json.dumps(info))
    f.flush()
    f.close()

def get_best(info):
	ratio = []

	# Get average payoff ratio for each slot
	for i in range(0,100):
		ratio.append( (sum(info['payoffs'][str(i)])/len(info['payoffs'][str(i)])) / (info["costs"][str(i)] if info['costs'][str(i)] != 0 else .1))
	# Need to get top 10 ratios
	slot_list= sorted(range(len(ratio)), key=lambda i: ratio[i])[-15:]
	slot_list.reverse()
	return slot_list

# Phase One - Testing the slot machines
# Strategy: Test each slot 10 times since we have 1,000,000 credits
def play_test_slots(state):

	# Load in data
	info = load_data()

	# First time
	if len(info) == 0:
		info['state'] = 'initial'
		info['current_slot'] = '0'
		info['trials'] = 0
		info['money'] = 1000000
		# Dictionary of slots with list of payoffs
		info["payoffs"] = {}
		# Dict of slots with costs
		info["costs"] = {}
		save_data(info)
		return {"team-code":state["team-code"], 
				"game":state["game"],
				"pull":0
		}
	if(info['money'] < 700000 and len(info['payoffs']) == 100):
		return {"team-code":state["team-code"], 
			"game":state["game"],
			"pull":None
		}
	

	info['trials'] +=1
	if info['current_slot'] in info['payoffs']:
		info["payoffs"][info['current_slot']].append(state["last-payoff"])
	else:
		info["payoffs"][info['current_slot']] = [state["last-payoff"]]
	info['costs'][info['current_slot']] = state['last-cost']
	info['money'] = info['money'] - state['last-cost'] + state['last-payoff']
	

	if(info['trials'] == 49 or (info['costs'][info['current_slot']] * info['trials'] - sum(info['payoffs'][info['current_slot']]) ) > 5000):
		info['trials'] =0
		info['current_slot'] = str(int(info['current_slot']) + 1)

	save_data(info)
	if (int(info['current_slot']) > 99 or info['state'] == 'max'):
		info['state'] = 'max'
		best = get_best(info)[0]
		info['current_slot'] = str(best)
		save_data(info)
		return {"team-code":state["team-code"], 
			"game":state["game"],
			"pull":int(best)
		}


	# Return statement
	return {"team-code":state["team-code"], 
			"game":state["game"],
			"pull":int(info['current_slot'])
	}




# Pick best slots from testing phase
def choose_slots():
	slot_list = []
	# Load data
	info = load_data()
	slot_list = get_best(info)
		
	
	
	info['top_30'] = slot_list[:25]
	slot_list = slot_list[5:]
	info['slot_list'] = slot_list
	save_data(info)	
	return slot_list


# Phase 2A - Choosing slots to auction
# We get to choose 10
def play_auction(state):
	info = load_data()


	# Load slots chosen prior
	slot_list = choose_slots()

	# Return
	return {"team-code":state["team-code"],
			"game":state["game"],
			"auctions":slot_list
	}


def bid(state,info):
	if info['money'] < 0:
		info['money'] = 1
	if state['auction-number'] in info['slot_list']:
		index = info['slot_list'].index(state['auction-number'])
		if index < 5:
			x = .11
		else:
			x = .08
		return {"team-code":state["team-code"],
					"game":state["game"],
					"bid": info['money'] * x
			}
	else:
		return {"team-code":state["team-code"],
					"game":state["game"],
					"bid": info['money'] * .01
			}



# Phase 2B - Bidding
# We can bid on 5 others not in slot_list
# Bid of 0 = pass
def play_bids(state):
	info = load_data()

	if('extra_five' not in info):
		temp = []
		for i in info['top_30']:
			if i not in info['slot_list']:
				temp.append((state['auction-lists'][i],i))
		temp.sort(key= lambda x: len(x[0]))
		temp[:5]
		slots = [x[1] for x in temp]
		info['extra_five'] = slots
		save_data(info)


	if state['auction-number'] in info['slot_list'] or state['auction-number'] in info['extra_five']:
		return bid(state,info)
	else:
		return {"team-code":state["team-code"],
				"game":state["game"],
				"bid":0
		}




# Determine what phase we are playing, return correct result
def get_move(state):
    if(state['game'] == 'phase_1'):
        result = play_test_slots(state)
    elif (state['game'] == 'phase_2_a'):
    	result = play_auction(state)
    elif (state['game'] == 'phase_2_b'):
    	result = play_bids(state)
    return result








