# Python script to find optimal NBA DK Draft- Version 2
## By Harsh Rana

import pandas as pd
import numpy as np
from itertools import combinations

def main():
	df = pd.read_csv("DKSalaries_v2.csv")
	# Player DFs by position
	df_C = df[df["Position"].str.contains("C")]
	df_G = df[df["Position"].str.contains("G")]
	df_F = df[df["Position"].str.contains("F")]

	# Created master and positions dicts
	c_dict = dict(zip(df_C.ID,zip(df_C.AvgPointsPerGame,df_C.Salary)))
	g_dict = dict(zip(df_G.ID,zip(df_G.AvgPointsPerGame,df_G.Salary)))
	f_dict = dict(zip(df_F.ID,zip(df_F.AvgPointsPerGame,df_F.Salary)))
	player_dict = dict(zip(df.ID,zip(df.AvgPointsPerGame,df.Salary)))

	# Optimize
	optimize(df, player_dict, g_dict, f_dict, c_dict, 46600)
	

def optimize(df, player_dict, g_dict, f_dict, c_dict, salary_cap):
	max_val = -1
	max_cost = -1
	max_combo = []
	count = 0

	# Pick 3 guards
	for g_players in list(combinations(list(g_dict.keys()), 3)):
	    # Remove players already picked
	    aval_f_players = f_dict
	    for g in g_players:
	        aval_f_players.pop(g, aval_f_players)

        # Pick 3 Forwards
	    for f_players in list(combinations(list(aval_f_players.keys()), 3)):
	        # Remove players already picked
	        aval_c_players = c_dict
	        for g in g_players:
	            aval_c_players.pop(g, aval_c_players)
	        for f in f_players:
	            aval_c_players.pop(f, aval_c_players)
	            
            # Pick 1 center
	        for c_players in list(combinations(list(c_dict.keys()), 1)):
	            players = f_players + g_players + c_players
	            players_cost = playerCostSum(players, player_dict)
	            players_points = playerPointSum(players, player_dict)
	            if (players_points > max_val and  players_cost < salary_cap):
	                max_val = players_points
	                max_cost = players_cost
	                max_combo = players
	print(max_val)
	print(max_cost)
	print(max_combo)
	for player in max_combo:
	    print(df.loc[df['ID'] == player]["Name"].values)


def playerCostSum(plist, p_dict):
	sum = 0
	for player in plist:
		sum += p_dict[player][1]
	return sum

def playerPointSum(plist, p_dict):
	sum = 0
	for player in plist:
		sum+=p_dict[player][0]
	return sum


if __name__ == '__main__':
	main()