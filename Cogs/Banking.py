import discord
from discord.ext import commands
from GLOBAL import statsCalculator, lookups, getAllData, key_from_value, player_ids, open_file, globalCheckAllBets, globalCheckPotential, globalCheckStake, globalNet, bankUpdate, ubcl_lookups, ubel_lookups
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

"""
CONTAINS:
- STAT
- LB
- PROCEDURE
- SHOWGRAPH
"""

class Banking(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def stat(self, ctx, *args):
    """
    [person] finds bank account for person
    """
    person = None
    if not args:
      person = key_from_value(player_ids, str(ctx.author.id))
    else:
      person = args[0]
    await statsCalculator(self, ctx, person, "print")

  @commands.command()
  async def allStatsCurrent(self, ctx):
    """
    it has a little stat for everyone
    """
    for person in lookups:
      await statsCalculator(self, ctx, person, "print")


  
  #@commands.command()
  async def ffpcheck(self, ctx, *, person):
    """
    [person] checks how close person is to breaking ffp
    """
    ffpcheck = await statsCalculator(self, ctx, person, "ffpcheck")
    await ctx.send(f"```{person}'s investments are {round(ffpcheck, 2)}mb away from breaching ffp```")
    
  #@commands.command()
  #@commands.has_role("host")
  #async def addOdd(self, ctx, *args):
  #  """
  #  add odds for matches. host only.
  #  """
  #  
  #  if ',' in args or len(args) != 5:
  #    await ctx.send("invalid input \nsend as ``team1 team2 team1odds drawodds team2odds`` (without commas please)")
  #  
  #  else: 
  #  try:
  #      with open('odds.txt', 'a') as fp:
  #          fp.write(f'\n{args[0]}.v.{args[1]} : {args[2]}, {args[3]}, {args[4]}')
  #      await ctx.send(
  #          f"✅   odds for {args[0]} vs {args[1]}: ``{args[2]}, {args[3]}, {args[4]}``, were entered successfully")
        
  #    except:
  #      await ctx.send("❌ File error occured! Please try again later.")

  @commands.command()
  async def lb(self, ctx):
    """
    Use to see the leaderboard based on current net worth.
    """
    net_worth_list = {}
    
    for person in lookups:
      netWorth = await statsCalculator(self, ctx, person, "net worth")
      net_worth_list.update({person:netWorth})
    
    leaderboard = dict(sorted(net_worth_list.items(), key = lambda x:x[1], reverse = True))
    
    message = '\n'.join(f'{list(leaderboard).index(key) + 1}) ' + str(key) + ' ' + str(value) for key, value in leaderboard.items())
    await ctx.send(f'```LEADERBOARD \n{message}```')
    
    #ubcl_net_worth_list = {}
    #ubel_net_worth_list = {}
    
    #for person in ubcl_lookups:
    #  netWorth = await statsCalculator(self, ctx, person, "net worth")
    #  ubcl_net_worth_list.update({person:netWorth})
    #print(ubcl_net_worth_list)

    #leaderboard = dict(sorted(ubcl_net_worth_list.items(), key = lambda x:x[1], reverse = True))
    
    #message = '\n'.join(f'{list(leaderboard).index(key) + 1}) ' + str(key) + ' ' + str(value) for key, value in leaderboard.items())
    #await ctx.send(f'```TIER 1 - UBCL \n{message}```')

    
    #for person in ubel_lookups:
    #  netWorth = await statsCalculator(self, ctx, person, "net worth")
    #  ubel_net_worth_list.update({person:netWorth})

    #leaderboard = dict(sorted(ubel_net_worth_list.items(), key = lambda x:x[1], reverse = True))
    
    #message = '\n'.join(f'{list(leaderboard).index(key) + 1}) ' + str(key) + ' ' + str(value) for key, value in leaderboard.items())
    #await ctx.send(f'```TIER 2 - UBEL \n{message}```')
    #await ctx.send(f'```promotion - top 2\nrelegation - bottom 2```')

  @commands.command()
  async def procedure(self, ctx):
    """
    procedure of a round (USEFUL)
    """
    await ctx.send(
      """```P R O C E D U R E:

COMPETITOR:
Once a round begins...
1. 👀 Look at odds using !showOdds
2. 💹 Place bets using !bulkBet, or check potential winnings with !potentialBet
3. 😤 Check bets are correct using !showBet, fix them using !removeBet before !bulkBet-ing again
4. 🤑 Wait for the money to roll in!*

HOST:
1. 👩‍💻 Before a round: find odds through API with !processOdds
2. 💻 After a round: match results are entered using !enterResult
3. 💸 Every Sunday: results are calculated using !sunday, !calculateAll, and !manualSaveHistory; OR !superSunday
4. 🧓 Every Sunday: old bets and odds from last week are archived using !archiveBet and !clearOdd

*: not guaranteed```""")

  @commands.command()
  async def showGraph(self, ctx, to_show):
    """
    Shows line graphs! Requires [to-show] as net-worth, wallet, investments, debts, or winnings
    """
    plt.clf() # refresh plt

    # possible toshow values
    data_locations = [
      "wallet",
      "investments",
      "debts",
      "net-worth",
      #"investment-ratio",
      "winnings"
    ]
    
    if (not to_show) or (to_show not in data_locations):
      await ctx.send("❌ yo enter a graph type to show: net-worth, wallet, interest, debts, or winnings.")
      return

    #await ctx.send("doin your math homework...")

    ## PRINT UBCL
    #entries_by_player = await getAllData(self, ctx)

    # exit loop for all players
    #data_to_graph_index = data_locations.index(to_show)

    #prettified_to_show = to_show.replace('-', ' ').title()
    #plt.xlabel("Entry")
    #plt.ylabel(prettified_to_show)
    #plt.title("UBCL " + prettified_to_show)
    
    #for player in ubcl_lookups:
      #this_players_data_to_graph = entries_by_player[player][data_to_graph_index]
      #x = np.array(range(len(this_players_data_to_graph)))
      #y = np.array(this_players_data_to_graph)
      #plt.plot(x, y, label=player)

    # print(entries_by_player)

    #plt.legend(loc="upper left")
    #plt.savefig(fname='plot.png')
    #file = discord.File('plot.png', filename='plot.png')
    #embed = discord.Embed(color=0x771bb8)
    #embed = embed.set_image(url='attachment://plot.png')
    #await ctx.send(file=file, embed=embed)
    #plt.clf()
    #os.remove('plot.png')

    ## PRINT UBEL
    #entries_by_player = await getAllData(self, ctx)

    # exit loop for all players
    #data_to_graph_index = data_locations.index(to_show)

    #prettified_to_show = to_show.replace('-', ' ').title()
    #plt.xlabel("Entry")
    #plt.ylabel(prettified_to_show)
    #plt.title("UBEL " + prettified_to_show)
    
    #for player in ubel_lookups:
      #this_players_data_to_graph = entries_by_player[player][data_to_graph_index]
      #x = np.array(range(len(this_players_data_to_graph)))
      #y = np.array(this_players_data_to_graph)
      #plt.plot(x, y, label=player)

    # print(entries_by_player)

    #plt.legend(loc="upper left")
    #plt.savefig(fname='plot.png')
    #file = discord.File('plot.png', filename='plot.png')
    #embed = discord.Embed(color=0xff6900)
    #embed = embed.set_image(url='attachment://plot.png')
    #await ctx.send(file=file, embed=embed)
    #plt.clf()
    #os.remove('plot.png')

    ### PRINT ALL
    entries_by_player = await getAllData(self, ctx)

    # exit loop for all players
    data_to_graph_index = data_locations.index(to_show)

    prettified_to_show = to_show.replace('-', ' ').title()
    plt.xlabel("Entry")
    plt.ylabel(prettified_to_show)
    plt.title("Overall " + prettified_to_show)
    
    for player in lookups:
      this_players_data_to_graph = entries_by_player[player][data_to_graph_index]
      x = np.array(range(len(this_players_data_to_graph)))
      y = np.array(this_players_data_to_graph)
      plt.plot(x, y, label=player)

    # print(entries_by_player)

    plt.legend(loc="upper left")
    plt.savefig(fname='plot.png')
    file = discord.File('plot.png', filename='plot.png')
    embed = discord.Embed(color=0x00bf0c)
    embed = embed.set_image(url='attachment://plot.png')
    await ctx.send(file=file, embed=embed)
    os.remove('plot.png')

  @commands.command()
  @commands.has_any_role("host", "chief host-executive financial officer") 
  async def exportData(self, ctx, *args):
    await ctx.send("```doing your taxes...```")
    entries_by_player = await getAllData(self, ctx)
    with open('output.csv', mode='w') as output:
      writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      for player in entries_by_player:
        for statNum, stat in enumerate(entries_by_player[player]):
          writer.writerow([player, statNum] + entries_by_player[player][statNum])
    await ctx.send("```✅ done```")

  @commands.command()
  async def checkAll(self, ctx, player=None):
    """
    Check a specific [player]'s betting in this round
    """
    # using a global
    # this is because it is also used at the end of bulkBet
    await globalCheckAllBets(self, ctx, player)

  @commands.command()
  async def checkPotential(self, ctx, player=None):
    """
    Check a specific [player]'s undecided bets in this round
    """
    # using a global
    # this is because it is also used at the end of bulkBet
    await globalCheckPotential(self, ctx, player)

  @commands.command()
  async def checkStake(self, ctx, player=None):
    """
    Check a specific [player]'s undecided bets in this round
    """
    # using a global
    # this is because it is also used at the end of bulkBet
    await globalCheckStake(self, ctx, player)

  @commands.command()
  async def checkNet(self, ctx, player=None):
    """
    Check a specific [player]'s undecided bets in this round
    """
    # using a global
    # this is because it is also used at the end of bulkBet
    await globalNet(self, ctx, player)

  @commands.command(hidden=True)
  @commands.has_any_role("host", "chief host-executive financial officer") 
  async def newCompetitor(self, ctx, *args):
    """
    SETS UP A NEW COMPETITOR! [name] [long discord id#]
    """
    #name and id in lookups (as an ARRAY not a DICT)(this is to introduce some object orientation and organization)
    #determines their wallet by averaging every other wallet
    #presets investment and loan to 0, giving them a slot in bank.txt

    person = args[0].lower()
    id = args[1]

    lookups_list = []
    try:
      with open("Data/lookups.txt", "r") as fp:
        lookups_list = fp.read().splitlines()
    except:
      await ctx.send("❌ file error occurred, please try again later.")
      return

    lookups_list.append(person)

    try:
      with open("Data/lookups.txt", "w") as fp:
        fp = fp.write("\n".join(lookups_list))
    except:
      await ctx.send("❌ file error occurred, please try again later.")
      return

    player_ids_list = []
    try:
      with open("Data/player_ids.txt", "r") as fp:
        player_ids_list = fp.read().splitlines()
    except:
      await ctx.send("❌ file error occurred, please try again later.")
      return

    player_ids_list.append(f'{person}, {id}')

    try:
      with open("Data/player_ids.txt", "w") as fp:
        fp = fp.write("\n".join(player_ids_list))
    except:
      await ctx.send("❌ file error occurred, please try again later.")
      return
    
    await ctx.send(f"meet <@{id}> - aka ``{person}``")
    await ctx.send(f"```🍾 {person.upper()} IS NOW A COMPETITOR! 🎉```")
    await ctx.send(f"```rerun replit and run !newBank and create new line to confirm```")
    

  @commands.command(hidden=True)
  @commands.has_any_role("host", "chief host-executive financial officer") 
  async def postponeAll(self, ctx):
      all_odds = await open_file("Data/odds.txt", ctx)
      
      flag = 0
      for i in range(len(all_odds)):
        match_odd = all_odds[i].split()
        if len(match_odd) < 10:
          flag = flag + 1
          match_odd.append('[postponed]\n')
          match_odd = ' '.join(match_odd)
          all_odds[i] = match_odd
          await ctx.send(f'```✅ match {i+1} has been postponed```')
        else:
          match_odd.append('\n')
          match_odd = ' '.join(match_odd)
          all_odds[i] = match_odd

      try: 
        with open('Data/odds.txt', 'w') as fp:
          for item in all_odds:
            fp.write(item)
      except:
        await ctx.send("❌ File error occured! Please try again later.")
        return
      
      await ctx.send(f'```🎉 {flag} missing results have been found```')


  @commands.command(hidden=True)
  @commands.has_any_role("host", "chief host-executive financial officer") 
  async def findUnfinished(self, ctx):
      all_odds = await open_file("Data/odds.txt", ctx)
      
      flag = 0
      for i in range(len(all_odds)):
        if len(all_odds[i].split()) < 10:
          flag = flag + 1
          await ctx.send(f'```match {i+1}: {all_odds[i]}```')
      
      await ctx.send(f'```✅ {flag} missing results have been found```')
  
  @commands.command(hidden=True)
  @commands.has_any_role("host", "chief host-executive financial officer") 
  async def newBank(self, ctx, player):
    """
    SETS UP A NEW COMPETITOR BANK! [name]
    """

    walletSum = 0
    for person in lookups:
      if person == player.lower():
        print(player)
        continue
      wallet = await statsCalculator(self, ctx, person, "wallet")
      walletSum = walletSum + wallet
    averageWallet = round(walletSum/(len(lookups)-1), 2)

    investmentSum = 0
    for person in lookups:
      if person == player.lower():
        print(player)
        continue
      investment = await statsCalculator(self, ctx, person, "investment")
      investmentSum = investmentSum + investment
    averageInvestment = round(investmentSum/(len(lookups)-1), 2)
    averageInvestment = round(averageInvestment*0.8, 2)
    averageWallet = averageWallet + averageInvestment

    debtSum = 0
    for person in lookups:
      if person == player.lower():
        print(player)
        continue
      debt = await statsCalculator(self, ctx, person, "debt")
      debtSum = debtSum + debt
    averageDebt = round(debtSum/(len(lookups)-1), 2)
    averageWallet = averageWallet - averageDebt
    
    
    await bankUpdate(self, ctx, "wallet", person, averageWallet)
    await bankUpdate(self, ctx, "investment", person, 0)
    await bankUpdate(self, ctx, "debt", person, 0)
    await statsCalculator(self, ctx, player.lower(), "print")
    
    
    
  
  

def setup(bot):
	bot.add_cog(Banking(bot))