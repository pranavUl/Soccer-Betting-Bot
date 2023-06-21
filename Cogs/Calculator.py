import discord
from discord.ext import commands
from GLOBAL import open_file, statsCalculator, lookups, bankUpdate, calculateGlobal
from datetime import datetime
import requests
import os

"""
CONTAINS
- ENTERRESULT
- PROCESSRESULTS
- CALCULATE
- POTENTIALBET
"""
## maybe move to global
key = os.environ['OddsAPI']

league_keys = {
    'MLS': 'soccer_usa_mls',
    'EPL': 'soccer_epl',
    'LaLiga': 'soccer_spain_la_liga',
    'UCL': 'soccer_uefa_champs_league',
    'WC': 'soccer_fifa_world_cup',
    'Bundesliga': 'soccer_germany_bundesliga',
    'Brazil_Serie_A': 'soccer_brazil_campeonato',
    'SerieA': 'soccer_italy_serie_a',
    'Ligue1': 'soccer_france_ligue_one',
    'NationsLeague': 'soccer_uefa_nations_league',
    'CarabaoCup': 'soccer_england_efl_cup',
    'FACup': 'soccer_fa_cup',
    'LigaPortugal': 'soccer_portugal_primeira_liga',
    'UEL': 'soccer_uefa_europa_league',
    'EFLChampionship': 'soccer_efl_champ',
    'Scotland': 'soccer_spl',
    'Eredivisie': 'soccer_netherlands_eredivisie'
}

date_format = 'iso'
#####


class Calculator(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
  
    @commands.command(hidden=True)
    @commands.has_any_role("host", "chief host-executive financial officer")
    async def enterResult(self, ctx, match, result):
      """
      [match#] [winteam] - Ex. !enterResult 1 home. host only.
      """   

      result = result.lower()
      winner = result
      
      try:
        with open('Data/odds.txt', 'r') as fp:
          all_odds = fp.readlines()
      except:
        await ctx.send("❌ File error occured! Please try again later.")

      odd = all_odds[int(match)-1].replace(".", " ").split()
      
      if result == "home":
        result = str(odd[4])
      elif result == "away":
        result = str(odd[6])
      elif result == "draw":
        result = result
      elif result == "postponed":
        result = result
      else:
        await ctx.send("❌ Enter the correct number and result identifier")
        return
      if len(odd) == 11:
          result = f'[{result}]'
          result += "\n"
          odd.append(result)
          odd = ' '.join(odd)
          all_odds[int(match) - 1] = odd
        
      else:
          await ctx.send("❌ Result was already entered")
          return
      
      try: 
        with open('Data/odds.txt', 'w') as fp:
          for item in all_odds:
            fp.write(item.replace(" v ", ".v."))
      except:
        await ctx.send("❌ File error occured! Please try again later.")
        return

      team1 = odd.split()[4]
      team2 = odd.split()[6]
      if winner == "home":
        winner = str(odd.split()[4])
      elif winner == "away":
        winner = str(odd.split()[6])
      elif winner == "draw":
        winner = winner
      elif winner == "postponed":
        winner = winner
      else:
        return
      
      if winner == "postponed":
        await ctx.send(f'✅ match {match}: ``{team1} vs {team2}`` has been ``{winner}``')
      else:
        await ctx.send(f'✅ the winner of match {match}: ``{team1} vs {team2}`` is ``{winner}``')

  
    @commands.command()
    @commands.has_any_role("host", "chief host-executive financial officer")
    async def bulkEnterResult(self, ctx, *, submission):
      """
        [match#] [winteam] - Ex. !enterResult 1 dortmund ↩ 2 toronto-fc ↩ ... . host only.
      """
      split_submission = submission.split('\n')
      for sub_submission in split_submission:
        split_sub_submission = sub_submission.split(" ")
        await self.enterResult(ctx, split_sub_submission[0], split_sub_submission[1])


    @commands.command(hidden=True)
    @commands.has_any_role("host", "chief host-executive financial officer")
    async def calculate(self, ctx, *, person):
      """
      [person] calculates all profit based on bets and odds.
      """
      await calculateGlobal(self, ctx, person) # exported so that superSunday also works
      
    @commands.command()
    @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
    async def calculateAll(self, ctx, *args):
      """
      Calculates the results of all bets
      """
      for player in lookups:
        await calculateGlobal(self, ctx, player)

      #await ctx.send("```check console for ignored bets pls```")
      await ctx.send("```✅ done!```")


    @commands.command()
    async def checkResults(self, ctx):
      all_odds = await open_file("Data/odds.txt", ctx)
    
      #check if match results were input into odds
      flag = 0
      for i in range(len(all_odds)):
        match_odd = all_odds[i].split()
        if len(match_odd) < 10:
          flag = flag + 1
      
      await ctx.send(f"```{flag} results have yet to be entered```") 

    @commands.command(hidden=True)
    @commands.has_any_role("host", "chief host-executive financial officer")
    async def processAllResults(self, ctx):
      """
      process results for all games in all active leagues at once
      """
      try:
        with open('Data/odds.txt', 'r') as fp:
          readableOdds = fp.read().replace(".", " ").replace("_", " ")
      except:
        await ctx.send("❌ File error occured! Please try again later.")

      readableOdds = readableOdds.split("\n")
      leagues_list = []
      for i in range(len(readableOdds)):
          try:
            if readableOdds[i].split()[0].replace(":", "") not in leagues_list and readableOdds[i].split()[0].replace(":", "") in league_keys: #and readableOdds[i].split()[0].replace(":", "") in leagues_list_master
              leagues_list.append(readableOdds[i].split()[0].replace(":", ""))
          except:
            pass
      
      for league in leagues_list:
        await self.processResults(ctx, league)

      await ctx.send(f'```🎉 all finished results in the top 5 leagues were added!```')

      
  
    @commands.command(hidden=True)
    @commands.has_any_role("host", "chief host-executive financial officer")
    async def processResults(self, ctx, league):
      """
      process results for all games in a league at once
      """
      sport = ''
      if league in league_keys:
        sport = league_keys.get(league)
      else:
        await ctx.send(f"❌ Enter the league as it is in the league_keys database. Only the following are allowed: {list(league_keys.keys())}")
        return
      
      #### Get Scores from API in the past 3 days ####
      results_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/scores/?daysFrom=3&apiKey={key}', params={
        'dateFormat': date_format,
    }
  )

      if results_response.status_code != 200:
        print(f':x: Failed to get odds: status_code {results_response.status_code}, response body {results_response.text}')
        await ctx.send(":x: Failed to get scores for the specified league")
        return

      else:
        results_json = results_response.json()
        print('Number of events:', len(results_json))
  
    # Check the usage quota
        print('Remaining requests', results_response.headers['x-requests-remaining'])
        if int(results_response.headers['x-requests-remaining']) < 100:
          await ctx.send(f"```⚠️ only {results_response.headers['x-requests-remaining']} requests remaining```")
        print('Used requests', results_response.headers['x-requests-used'])
      #### Coding starts here ####
      
      #print(results_json) #TROUBLESHOOOTING
      
      games_with_results = []
      
      for match in results_json:
        if match['completed'] == True:
          games_with_results.append(match['scores'])

      try:
        with open('Data/odds.txt', 'r') as fp:
          all_odds = fp.readlines()
      except:
        await ctx.send("❌ File error occured! Please try again later.")

      result_counter = 0
      for i in games_with_results:
        result = ''

        i[0]['name'] = i[0]['name'].lower().replace(" ", "-")
        i[1]['name'] = i[1]['name'].lower().replace(" ", "-")
        
        if i[0]['score'] == i[1]['score']:
          result = 'draw'
        elif i[0]['score'] > i[1]['score']:
          result = i[0]['name']
        else:
          result = i[1]['name']

        
        
        for odd in all_odds:
          #print(odd) #TESTING
          
          if (i[0]['name'] in odd.replace(".v.", " ")) and (i[1]['name'] in odd.replace(".v.", " ")) and len(odd.split()) < 10:
            oddIndex = all_odds.index(odd)
            odd = odd.split()
            odd.append(f'[{result}]\n')
            await ctx.send(f'```✅ match {oddIndex+1}: {i[0]["name"]} {i[0]["score"]} - {i[1]["score"]} {i[1]["name"]}```')
            #await ctx.send(f'```TEST winner of match {oddIndex+1}: {odd[4].replace(".v.", " ").split()[0]} vs {odd[4].replace(".v.", " ").split()[1]} is {result}```')
            odd = " ".join(odd)
            all_odds[oddIndex] = odd     
            result_counter += 1
            break
          else:
            continue
            
        
      #print(all_odds) #TESTING
      all_odds = "".join(all_odds)
      try:
        with open("Data/odds.txt", "w") as fp:
          fp.write(all_odds)
      except:
        await ctx.send(":x: file error, please try again later")

      #print(games_with_results)
      
          

      
      
      

  
def setup(bot):
  bot.add_cog(Calculator(bot))

  