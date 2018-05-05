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

# Phase One - Testing the slot machines
# Strategy: Test each slot 10 times since we have 1,000,000 credits
def play_test_slots(state):

	# Stop pulling after 1000 tests
	if (state["pulls-left"] < 5000):
		return {"team-code":state["team-code"], 
			"game":state["game"],
			"pull":None
	}	

	# Load in data
	info = load_data()

	# First time
	if len(info) == 0:
		info['current_slot'] = '0'
		info['trials'] = 0
		# Dictionary of slots with list of payoffs
		info["payoffs"] = {}
		# Dict of slots with costs
		info["costs"] = {}
		save_data(info)
		return {"team-code":state["team-code"], 
				"game":state["game"],
				"pull":0
		}

	info['trials'] +=1
	if info['current_slot'] in info['payoffs']:
		info["payoffs"][info['current_slot']] += state["last-payoff"]
	else:
		info["payoffs"][info['current_slot']] = state["last-payoff"]
	info['costs'][info['current_slot']] = [state['last-cost']]
	
	if(info['trials'] == 49 or info['costs']info['current_slot'] * info['trials'] > 5,000):
		info['trials'] =0
		info['current_slot'] = str(int(info['current_slot']) + 1)
	save_data(info)


	# Return statement
	return {"team-code":state["team-code"], 
			"game":state["game"],
			"pull":info['current_slot']
	}

# Pick best slots from testing phase
def choose_slots():
	slot_list = []
	# Load data
	info = load_data()
	info["slot-ratios"] = {}

	# Get average payoff ratio for each slot
	for i in range(0,100):
		average_payoff = info["payoffs"][i] / 10
		ratio = average_payoff / info["costs"][i]
		info["slot-ratios"][i] = ratio 
	
	# save
	save_data(info)
	
	# Need to get top 10 ratios
	for i in range(0,10):
		key_to_choose = get_max_in_dict(info["slot-ratios"])
		slot_list.append(key_to_choose)
		info["slot-ratios"][key_to_choose] = 0
		save_data(info)
	return slot_list

def get_max_in_dict(dict):
	# Citing source: https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
	values = dict.values() # this gets all values
	keys = dict.keys() # this gets all keys
	return keys[values.index(max(values))] # this selects the key based on the max value in the list of avalues


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

# Phase 2B - Bidding
# We can bid on 5 others not in slot_list
# Bid of 0 = pass
def play_bids(state):
	bid = 0

	# Generic return
	return {"team-code":state["team-code"],
			"game":state["game"],
			"bid":bid
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








