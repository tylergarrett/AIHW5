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
		

	# Load in data
	info = load_data()

	# First time
	if len(info) == 0:
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
	# Stop pulling after 1000 tests
	if (state["pulls-left"] < 5000 or int(info['current_slot']) > 99):
		return {"team-code":state["team-code"], 
			"game":state["game"],
			"pull":None
	}

	info['trials'] +=1
	if info['current_slot'] in info['payoffs']:
		info["payoffs"][info['current_slot']] += state["last-payoff"]
	else:
		info["payoffs"][info['current_slot']] = state["last-payoff"]
	info['costs'][info['current_slot']] = state['last-cost']
	info['money'] = info['money'] - state['last-cost'] + state['last-payoff']
	if(info['trials'] == 49 or (info['costs'][info['current_slot']] * info['trials'] - info['payoffs'][info['current_slot']]) > 5000):
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
	ratio = []

	# Get average payoff ratio for each slot
	for i in range(0,100):
		ratio.append(info['payoffs'][str(i)] / info["costs"][str(i)])
		
	
	# Need to get top 10 ratios
	slot_list= sorted(range(len(ratio)), key=lambda i: ratio[i])[-15:]
	slot_list.reverse()
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
	#TODO:currently only the simple solution
	return {"team-code":state["team-code"],
				"game":state["game"],
				"bid": info['money'] * .10
		}



# Phase 2B - Bidding
# We can bid on 5 others not in slot_list
# Bid of 0 = pass
def play_bids(state):
	info = load_data()
	if state['auction_number'] in info[slot_list]:
		return bid(state,info)
	else:
		# Generic return
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








