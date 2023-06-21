import discord
from discord.ext import commands
import requests
import os
import datetime
from GLOBAL import wc_groups
"""
CONTAINS:
- PROCESSODDS
- SHOWODDS
- CLEARODDS
"""

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

regions = 'us'
markets = 'h2h'
odds_format = 'american'
date_format = 'iso'


class Odds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("host", "chief host-executive financial officer")
    async def processAllOdds(self, ctx, startdate, enddate, fileAdd):
      """
      processes every odd possible given [startdate][enddate][clear/append]
      """

      for league in league_keys:
        await self.processOdds(ctx, league, startdate, enddate, fileAdd)

      await ctx.send("```🎉 all available odds were processed!```")
  
    @commands.command()
    @commands.has_any_role("host", "chief host-executive financial officer")
    async def processOdds(self, ctx, league, startdate, enddate, fileAdd):
        """
      processes every odd given [league][startdate][enddate][clear/append]
      """
        sport = ''

        if league == "" or startdate == "" or enddate == "" or fileAdd == "":
            await ctx.send(
                f"❌ Enter in format: [league][startdate][enddate][clear/append]"
            )
            return

        if league in league_keys:
            sport = league_keys.get(league)
        else:
            await ctx.send(
                f"❌ Enter the league as it is in the league_keys database. Only the following are allowed: {list(league_keys.keys())}"
            )
            return

        async def new_date_format_check(date):
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                await ctx.send(
                    f"❌ enter the right format for {date}, yyyy-mm-dd, and ensure it actually exists"
                )
                exit()

        await new_date_format_check(startdate)
        await new_date_format_check(enddate)

        sports_response = requests.get(
            'https://api.the-odds-api.com/v4/sports', params={'api_key': key})

        if sports_response.status_code != 200:
            print(
                f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}'
            )
            return

        else:
            print('List of in season sports:', sports_response.json())

##########################################

        odds_response = requests.get(
            f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
            params={
                'api_key': key,
                'regions': regions,
                'markets': markets,
                'oddsFormat': odds_format,
                'dateFormat': date_format,
            })

        if odds_response.status_code != 200:
            print(
                f':x: Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}'
            )
            await ctx.send(
                ":x: Failed to get odds for specified league and time frame")
            return

        else:
            odds_json = odds_response.json()
            print('Number of events:', len(odds_json))

            # Check the usage quota
            print('Remaining requests',
                  odds_response.headers['x-requests-remaining'])
            print('Used requests', odds_response.headers['x-requests-used'])


############ coding starts here ############
#print(odds_json)
        sportsbook_odds = []
        if league == "UCL":
            sportsbook = "foxbet"
        else:
            sportsbook = "draftkings"

        for match in odds_json:
            for index in range(len(match['bookmakers'])):

                if match['bookmakers'][index]['key'] == sportsbook and (
                        startdate <= match['commence_time'].split('T')[0] <=
                        enddate):
                    for index2 in range(
                            len(match['bookmakers'][index]['markets'][0]
                                ['outcomes'])):
                        sportsbook_odds.append(
                            match['bookmakers'][index]['markets'][0]
                            ['outcomes'][index2]['name'])
                        sportsbook_odds.append(
                            match['bookmakers'][index]['markets'][0]
                            ['outcomes'][index2]['price'])
                    sportsbook_odds.append(match['commence_time'])

        organized_odds = []

        for match in range(0, len(sportsbook_odds), 7):
            if int(str(sportsbook_odds[match + 1]).replace(" ", "")) > 0:
                team1odd = "".join(("+", str(sportsbook_odds[match + 1])))
            else:
                team1odd = sportsbook_odds[match + 1]

            if int(str(sportsbook_odds[match + 5]).replace(" ", "")) > 0:
                drawodd = "".join(("+", str(sportsbook_odds[match + 5])))
            else:
                drawodd = sportsbook_odds[match + 5]

            if int(str(sportsbook_odds[match + 3]).replace(" ", "")) > 0:
                team2odd = "".join(("+", str(sportsbook_odds[match + 3])))
            else:
                team2odd = sportsbook_odds[match + 3]

            organized_odds.append([
                league, sportsbook_odds[match].lower().replace(" ", "-"),
                sportsbook_odds[match + 2].lower().replace(" ", "-"), team1odd,
                drawodd, team2odd, sportsbook_odds[match + 6]
            ])

        #list -> file
        if organized_odds == []:
            await ctx.send(
                f"```❌ there are no {league} matches in the specified time frame```")
            return

        else:
            fileAdd = fileAdd.lower()

            if fileAdd == "clear":
                try:
                    with open('Data/odds.txt', 'w') as fp:
                        for match in organized_odds:
                            fp.write(
                                f'{match[0]}: {match[6].replace("T", " ").replace("Z", "")} : {match[1]}.v.{match[2]} : {match[3]}, {match[4]}, {match[5]}\n'
                            )
                except:
                    await ctx.send(
                        f"❌ file error occurred, please try again later.")
                    return

            elif fileAdd == "append":
                try:
                    with open('Data/odds.txt', 'a') as fp:
                        for match in organized_odds:
                            fp.write(
                                f'{match[0]}: {match[6].replace("T", " ").replace("Z", "")} : {match[1]}.v.{match[2]} : {match[3]}, {match[4]}, {match[5]}\n'
                            )
                except:
                    await ctx.send(
                        f"❌ file error occurred, please try again later.")
                    return

            else:
                await ctx.send(
                    f"❌ enter input as [league] [startdate] [enddate] [clear/append]"
                )
                return

            await ctx.send(
                f'```✅ odds for matches from {startdate} to {enddate} in {league.replace("_", " ")} were inputted sucessfully. verify using !showOdds```'
            )

    @commands.command()
    async def showOdds(self, ctx, *args):
        """
      PRINTS EVERY MATCH (useful)
      """
        try:
            with open('Data/odds.txt', 'r') as fp:
                readableOdds = fp.read().replace(".", " ").replace("_", " ")
        except:
            await ctx.send("❌ File error occured! Please try again later.")

        try:
          if args[0] != "":
            leagueCode = args[0]
        except:
          leagueCode = None
        #try:
        #    if args[0] == "B":
        #      await ctx.send("Forbid it, Almighty God! I know not what course others may take; but as for me, give me liberty or give me death!")
        #      return
        #    if args[0] in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        #      leagueCode = args[0]
        #    else:
        #      await ctx.send("❌ enter a group from A to H")
        #      return
        #except:
        #    leagueCode = None

        #numbers to emojis
        def int_to_en(num):
            d = {
                0: '<:greenzero:1003495205254733825>',
                1: '1️⃣',
                2: '2️⃣',
                3: '3️⃣',
                4: '4️⃣',
                5: '5️⃣',
                6: '6️⃣',
                7: '7️⃣',
                8: '8️⃣',
                9: '9️⃣'
            }
            return (d[num])

        #Adds index numbers to odds for understandability
        readableOdds = readableOdds.split("\n")
        leagues_list = []

        #LEAGUE SEARCHER (REMOVED FOR WORLD CUP)
        if leagueCode != None:
            readableOdds2 = readableOdds
        
            readableOddsDuplicate = readableOdds

            readableOdds = []
            try:
              readableOdds = [odd for odd in readableOddsDuplicate if odd.split()[0] == f'{leagueCode}:']
            except:
              print(readableOdds)

            for odd in readableOddsDuplicate:
                ogOdd = odd
                if odd == "":
                    break
                if odd.split()[0] == f'{leagueCode}:':           
                    odd = odd.replace(f'{odd.split()[0]} ', "")
                    readableOdd = f'{int(readableOddsDuplicate.index(ogOdd)+1)}) {odd}'
                    readableOdds.append(readableOdd)

            if readableOdds2 == readableOdds or readableOdds == []:
                await ctx.send(
                    ":x: try entering a valid league. check all active leagues with !showOdds"
                )
                return

        if leagueCode == None:
          for i in range(len(readableOdds)):
                try:
                    if readableOdds[i].split()[0].replace(
                            ":", "") not in leagues_list:
                        leagues_list.append(readableOdds[i].split()[0].replace(
                            ":", ""))
                except:
                    pass
                if readableOdds[i] == "":
                    break
                print(readableOdds[i])
                readableOdds[i] = readableOdds[i].replace("WC: ", "")
                print(readableOdds[i])
                readableOdds[i] = f'{int(i+1)}) {readableOdds[i]}'

        #WINNER CHECKER AND CAPITALIZER
        #try:
        for i in readableOdds:
            if len(i.split()) == 13 and leagueCode == None: ##
                ogI = i
                odd = i.split()
                matchWinner = str(odd[12]).replace("[", "").replace("]", "")
                i = i.replace(str(odd[12]), "")
                if matchWinner != "draw" and matchWinner != "postponed":
                    i = i.replace(matchWinner, matchWinner.upper())
                elif matchWinner == "draw":
                    team1 = str(odd[4])
                    team2 = str(odd[6])
                    i = i.replace(" v ", " DRAW ")
                else:
                    i = i.replace(" v ", " pp ")
                readableOdds[readableOdds.index(ogI)] = i  ##
            if len(i.split()) == 12 and leagueCode != None: ##

                ogI = i
                odd = i.split()
                matchWinner = str(odd[11]).replace("[", "").replace("]", "")

                i = i.replace(str(odd[11]), "")
                if matchWinner != "draw" and matchWinner != "postponed":
                    i = i.replace(matchWinner, matchWinner.upper())
                elif matchWinner == "draw":
                    team1 = str(odd[4]) ##
                    team2 = str(odd[6]) ##
                    i = i.replace(" v ", " DRAW ")
                else:
                    i = i.replace(" v ", " PP ")
                readableOdds[readableOdds.index(ogI)] = i
                
        
        oddsA = []
        oddsB = []
        oddsC = []
        oddsD = []
        oddsE = []
        oddsF = []
        oddsG = []
        oddsH = []
      
        #for odd in readableOdds:
        #  if odd == "":
        #    break
        #  if odd.split()[4].lower() in wc_groups[0] and odd.split()[6].lower() in wc_groups[0]:
        #    oddsA.append(odd)
        #  elif odd.split()[4].lower() in wc_groups[1] and odd.split()[6].lower() in wc_groups[1]:
        #    oddsB.append(odd)
        #  elif odd.split()[4].lower() in wc_groups[2] and odd.split()[6].lower() in wc_groups[2]:
        #    oddsC.append(odd)
        #  elif odd.split()[4].lower() in wc_groups[3] and odd.split()[6].lower() in wc_groups[3]:
        #    oddsD.append(odd)
        #  elif odd.split()[4].lower() in wc_groups[4] and odd.split()[6].lower() in wc_groups[4]:
        #    oddsE.append(odd)
        #  elif odd.split()[4].lower() in wc_groups[5] and odd.split()[6].lower() in wc_groups[5]:
        #    oddsF.append(odd)
        #  elif odd.split()[4].lower() in wc_groups[6] and odd.split()[6].lower() in wc_groups[6]:
        #    oddsG.append(odd)
        #  elif odd.split()[4].lower() in wc_groups[7] and odd.split()[6].lower() in wc_groups[7]:
        #    oddsH.append(odd)
        #except:
        #  await ctx.send(":x: unknown error in winner capitalization")
        #  return

        #readableOddsFormatting = readableOdds
        #longestMatch = 0
        #for odd in readableOddsFormatting:
        #  odd = odd.split()
        #  match = f"{odd[4]}.{odd[5]}.{odd[6]}"
        #  if len(match) > longestMatch:
        #    longestMatch = len(match)
        #  else:
        #    continue

        #readableOdds = []
        #longestMatch = longestMatch + 2
        #for odd in readableOddsFormatting:
        #  odd = odd.split()
        #  match = f"{odd[4]} {odd[5]} {odd[6]}"
        #  newOdd = f"{odd[0]} {odd[1]} {odd[2]} {odd[3]} {match:<45} {odd[7]} {odd[8]} {odd[9]} {odd[10]}"
        #  readableOdds.append(newOdd)

        #FINISH LINE
        ############readableOdds = '\n'.join(readableOdds)
        
        #print(readableOdds)
        ##oddsA = '\n'.join(oddsA)
        #oddsB = '\n'.join(oddsB)
        #oddsC = '\n'.join(oddsC)
        #oddsD = '\n'.join(oddsD)
        #oddsE = '\n'.join(oddsE)
        #oddsF = '\n'.join(oddsF)
        #oddsG = '\n'.join(oddsG)
        #oddsH = '\n'.join(oddsH)

        printOdd = [[]] # list of chunks

        #for odd in readableOdds:
        #  odd2 = odd.replace(odd.split()[2], "")
        #  readableOdds[readableOdds.index(odd)] = odd2
        
        if len(readableOdds) > 15:
          for odd in readableOdds: # for every odd in odds to be shown
            if len(printOdd[-1]) >= (len(readableOdds)/2): # if the current chunk of printBet is too large, add another chunk
              printOdd.append([])
            printOdd[-1].append(odd)



        if len('\n'.join(readableOdds)) < 2000:
            if args[0] != None:
              await ctx.send(f'```{args[0].upper()} WEEKLY ODDS ⚽```')
            else:
              await ctx.send(f'```ALL ROUND ODDS ⚽```')
            if printOdd != [[]]:  
              for chunk in printOdd:
                chunk = '\n'.join(chunk)
                await ctx.send(f"```{chunk}```")
            else:
              readableOdds = '\n'.join(readableOdds)
              await ctx.send(f"```{readableOdds}```")
            await ctx.send(f'```-5hrs for CST, -6hrs for MDT```')
        else:
            await ctx.send(
                f'```❌ Uh oh, looks like there\'s too many odds for Discord to handle. \nTry searching specific leagues with !showOdds [league]```'
            )
            leagues_list = ", ".join(leagues_list)
            await ctx.send(f'```current leagues: {leagues_list}```')

    @commands.command(hidden=True)
    @commands.has_any_role("host", "chief host-executive financial officer")
    async def clearOdds(self, ctx):
        """
      clear odds for matches. host only.
      """
        try:
            with open('Data/odds.txt', 'w') as fp:
                fp.write('')
        except:
            await ctx.send("❌ File error occured! Please try again later.")

        await ctx.send(f"✅ all odds were cleared successfully")


def setup(bot):
    bot.add_cog(Odds(bot))
