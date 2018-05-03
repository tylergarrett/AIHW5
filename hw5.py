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
# Strategy: idk 
def play_test_slots(state):
	slot = 0

	# Generic return
	return {"team-code":state["team-code"], 
			"game":state["game"],
			"pull":slot
	}

# Phase 2A - Choosing slots to auction
# We get to choose 10
def play_auction(state):
	slot_list = []

	# Generic return
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








