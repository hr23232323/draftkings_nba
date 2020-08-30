# Python script to find optimal NBA DK Draft
## By Harsh Rana
import pandas as pd
import numpy as np
from itertools import combinations

def main():
	df = pd.read_csv("DKSalaries.csv")
	df.dropna(inplace=True)
	player_dict = dict(zip(df.ID,zip(df.AvgPointsPerGame,df.Salary)))
	optimize(df, player_dict, 5, 35000)
	

def optimize(df, player_dict, num_players, salary_cap):
	max_val = -1
	max_cost = -1
	max_combo = []
	count = 0
	for players in list(combinations(list(player_dict.keys()), num_players)):
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