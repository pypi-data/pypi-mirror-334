from operator_precedence_high_roller.json_handling.json_handle import JsonHandle
from datetime import datetime
import seaborn as sns
import numpy as np
import matplotlib
matplotlib.use('TkAgg',force=True)
import matplotlib.pyplot as plt
import time
from operator_precedence_high_roller.computing.compute import Compute
import discord

class RollSave:
    #kh stuff is messing this up, change it at some point
    #save multiple rolls as separate rolls
    def __init__(self, message: discord.Message, c: Compute):
        self.message = message
        self.c = c
        self.json_handler = JsonHandle(playername=message.author.name)

    def add_rolls_to_json(self):
        i = 0
        for list_of_rolls in self.c.all_lists_of_rolls:
            roll_total = 0
            for roll in list_of_rolls:
                roll_total += roll
            self.json_handler.add_roll(
                self.message.author.name,
                self.c.list_of_dice[i],
                roll_total,
                datetime.timestamp(datetime.now())
            )
            i += 1

    def get_rolls_from_json(self, hours:int=12, die:str="d20"):
        rolls = self.json_handler.get_rolls(self.message.author.name)
        recent_rolls = []
        for i in range(len(rolls)):
            ts = rolls[i]["timestamp"]
            d = rolls[i]["die"]
            seconds_to_subtract = hours*3600
            if ts > time.time() - seconds_to_subtract and d == die:
                recent_rolls.append(rolls[i])
        num_rolls = int(die[:die.index('d')]) if die[:die.index('d')] != '' else 1
        num_sides = int(die[die.index('d')+1:])
        results = [0]*num_rolls*num_sides
        for i in range(len(recent_rolls)):
            results[recent_rolls[i]["roll"]-1] += 1
            pass
        ax = sns.barplot(x=np.arange(1,num_rolls*num_sides+1), y=results)
        ax.bar_label(ax.containers[0])
        plt.axis('off')
        plt.savefig('bar_plots/bar_plot_' + self.message.author.name + '.png')
        plt.clf()