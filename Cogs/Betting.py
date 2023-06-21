import discord
from discord.ext import commands
from GLOBAL import player_ids, key_from_value, lookups, statsCalculator, open_file, get_match, globalCheckStake, showBetGlobal, checkDate
from datetime import date, datetime

"""
CONTAINS:
- BET
- BULKBET
- REMOVEBET
- SHOWBET
- ARCHIVEBET
- POTENTIALBET
"""

class Betting(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(hidden=True)
  async def bet(self, ctx, *, submission):
    """
    Bet for a team! [match number] [team to win or draw] [amount]
    """
    player = key_from_value(player_ids, str(ctx.author.id))
    current_date = date.today()
    
    #NEW FORMATTING CODE#
    
    submission = submission.split()
    odds = await open_file('Data/odds.txt', ctx)
    match = await get_match(submission[0], odds)

    if submission[1] == "home":
      result = submission[1].lower()
      if result != "draw":
        result = "win"
      match = f'{submission[2]} {match.split()[0]} {result} {match.split()[1]}'
    elif submission[1] == "away":
      result = submission[1].lower()
      if result != "draw":
        result = "win"
      match = f'{submission[2]} {match.split()[1]} {result} {match.split()[0]}'
    elif submission[1].lower() == "draw":
      result = submission[1].lower()
      match = f'{submission[2]} {match.split()[1]} {result} {match.split()[0]}'
    else:
      await ctx.send(":x: that team isn't in that match")
      return

    ##
    
    async def checkDuplicate(person, match):
      team1 = match.split()[1]
      team2 = match.split()[3]
      all_bets = await open_file('Data/bets.txt', ctx)
      for bet in all_bets:
        if person in bet and team1 in bet and team2 in bet:
          await ctx.send(f"❌ you already bet that")
          return False

    #async def checkWallet(player_query, amount):
    #  player_wallet = await statsCalculator(self, ctx, player, "wallet")
    #  await ctx.send(player_wallet)
    #  chunked_all_player_bets = await self.showBet(ctx, player=player_query, only_return=True)
    #  all_player_bets = [*chunked_all_player_bets]
    #  await ctx.send(all_player_bets)
    #  return False

    player_wallet = await statsCalculator(self, ctx, player, "wallet")
    
    #CHECK WALLET TOTAL
    all_bets = await open_file("Data/bets.txt",  ctx)
    organized_bet_data = [[this_bet.split()[h] for h in range(2, 6)] for this_bet in all_bets if this_bet.split()[1] == player] 
    amountBetted = 0
    for bet in organized_bet_data:
      print(bet)
      amountBetted = amountBetted + float(bet[0])
    if amountBetted + float(submission[2]) > player_wallet: 
      await ctx.send(f":x: you've already betted ``{amountBetted}`` so you can only take ``{round(player_wallet-amountBetted, 2)}`` on this")
      return
    
          
    #CHECK WALLET 50%
    if float(submission[2]) > player_wallet/2:
      await ctx.send(f":x: your max is 50% of wallet: ``{round(player_wallet/2, 2)}``")
      return
    
      

    possible_rivals = []
    try:
      bets = await open_file("Data/bets.txt", ctx)
      for bet in bets:
        if f"{match.split()[0]} {result} {match.split()[1]}" in bet:
          possible_rivals.append(bet)
    except:
      await ctx.send("❌ File error occurred, please try again later")

    if possible_rivals != []:
      possible_rivals = "\n".join(possible_rivals)
      await ctx.send(f"```POSSIBLE RIVALS: \n{possible_rivals}```")
      
    
    if len([len(i) for i in match.split()]) != 4:
      await ctx.send(f"❌ Please use the proper format: ``[match number] [team to win or draw] [amount]``")

    else:
      #checks
      c1 = await checkDuplicate(player, match)
      c2 = await checkDate(ctx, current_date, match, 1, 3)
    #  c3 = await checkWallet(player, submission[2])
      if c1 == False or c2 == False:
        return
      
      try:
        with open("Data/bets.txt", 'a') as fp:
          fp.write(f'{current_date} {player} {match.lower()}\n')
          await ctx.send(
            f"✅  The bet ``{current_date} {player} {match}`` was added."
          )
        fp.close()
      except:
        await ctx.send("❌ File error occured! Please try again later.")



  @commands.command()
  async def bulkBet(self, ctx, *, submission):
    """
    Bet for more than one team at a time! !bulkBet first-bet ↩ second-bet ↩ enter...
    """

    split_submission = submission.split('\n')
    for sub_submission in split_submission:
      if len(sub_submission.split()) > 3:
        await ctx.send(f"YOU TYPED ``{sub_submission}`` WRONG\nDo it like this:\n ```!bulkBet [match number] [team to win or draw] [amount]\n[match number] [team to win or draw] [amount]\n[match number] [team to win or draw] [amount]...```\nDid not add any bets including and after this entry")
        return
      await self.bet(ctx, submission=sub_submission)
    await globalCheckStake(self, ctx, key_from_value(player_ids, str(ctx.author.id)))
    
  
  @commands.command()
  async def removeBet(self, ctx, *, submission):
    """
    To remove a bet. [date] [player] [amount] [team] [result] [team2]
    """
    
    if len(submission.split()) != 6:
      await ctx.send(f"❌ Enter in format [date] [player] [amount] [team] [result] [team2]")
      return

    player = submission.split()[1]

    current_date = date.today()
    dateCheck = await checkDate(ctx, current_date, submission, 3, 5)
    if dateCheck == False:
      return


    if ctx.author.id != int(player_ids[player]):
      await ctx.send(f"❌ You can't remove someone else's bet")
      return

    else:
      try:
        with open('Data/bets.txt', 'r+') as fp:
          bet_list = fp.readlines()
          fp.seek(0)
          for line in bet_list:
            if line.strip("\n") != submission:
              fp.write(line)
          fp.truncate()

        await ctx.send(f"✅   The bet ``{submission}`` was removed.")
      except:
        await ctx.send("❌ File error occured! Please try again later.")


  
  @commands.command()
  async def showBet(self, ctx, *, player="", only_return=False):
    """
    [person/all/empty/anySearchTerm] PRINTS EVERY BET
    """
    await showBetGlobal(self, ctx, player, only_return)

  @commands.command()
  async def remind(self, ctx, *, number, only_return=True):
    """
    bet reminder
    """
    for player in lookups:
      player_bets = await showBetGlobal(self, ctx, player, only_return)
      if player_bets == [[]]:
        id = player_ids[player]
        printID = f"<@{id}>"
        spamID = ""
        for i in range(int(number)):
          spamID = f'{spamID} \n{printID} bet'
        await ctx.send(f"{spamID}")
    
  @commands.command()
  @commands.has_any_role("host", "chief host-executive financial officer")
  async def archiveBet(self, ctx, *, date):
    """
    To archive old bets. Only hosts can use.
    """
    try:
      with open('Data/bets.txt', 'r+') as fp:
        with open('Data/archived_bets.txt', 'a') as fp2:
          bet_list = fp.readlines()
          fp.seek(0)
          date = date.lower()
          for line in bet_list:
            if date == "all":
              fp2.write(line)
            else:
              if date in line:
                fp2.write(line)
              else:
                fp.write(line)
        fp.truncate()

      await ctx.send(f"✅   The bets from ``{date}`` were archived.")
      
    except:
      await ctx.send("❌ File error occured! Please try again later.")

  @commands.command()
  async def bulkPotentialBet(self, ctx, *, submission):
    """
    Like bulkBet, but for potential bets! [match number] [team or draw] [amount]
    """
    split_submission = submission.split('\n')
    for sub_submission in split_submission:
      split_sub = sub_submission.split(' ')
      await self.potentialBet(ctx, *split_sub)

  @commands.command()
  async def potentialBet(self, ctx, *args):
      """
      [match number] [team or draw] [amount] calculate potential profit for a bet
      """

      if len(args) != 3:
        await ctx.send(f':x: enter the correct inputs')
        return
      
      person = key_from_value(player_ids, str(ctx.author.id))
      submission = args[0]
      result = args[1]
      result = result.lower()
      amt = float(args[2])
      
      all_odds = []     
      all_odds = await open_file("Data/odds.txt", ctx)
      person = person.lower()

      odds = await open_file('Data/odds.txt', ctx)
      match = await get_match(int(submission), odds)

      if result == "home":
        if result != "draw":
          result = "win"
        team1 = match.split()[0]
        team2 = match.split()[1]
      elif result == "away":
        if result != "draw":
          result = "win"
        team1 = match.split()[1]
        team2 = match.split()[0]
      elif result == "draw":
        team1 = match.split()[0]
        team2 = match.split()[1]
      else:
        await ctx.send(":x: that team isn't in that match")
        return

      #finds wallet for person
      wallet = await statsCalculator(self, ctx, person, "wallet")
      
      #error check
      if person not in lookups:
        await ctx.send(f':x: {person} is not registered as a player')
        return
      if result != "draw" and result != "win":
        await ctx.send(f':x: {result} is not a match result')
        return

      #cleans odds
      for i in range(len(all_odds)):
        all_odds[i] = all_odds[i].replace(".v.", " ").replace(":","").split()
      
      #finding necessary odds (non listcomp version):
      organized_odds_data = []
      for odd in all_odds:
        if team1 in odd and team2 in odd:
          organized_odds_data.append(odd)

      #error check
      if organized_odds_data == []:
        await ctx.send(f':x: invalid match, try again')
        return
        
      calc_data = []
      calcOdd = None
        
      for odd in organized_odds_data:
          #if win predict
          if team1 == odd[3] and team2 == odd[4] and result == "win":
            calcOdd = odd[5]
            break
          if team1 == odd[4] and team2 == odd[3] and result == "win":
            calcOdd = odd[7]
            break

          #if draw success
          elif result == "draw":
            calcOdd = odd[6]
            break
          
      if calcOdd != None:
         calc_data.append([amt, calcOdd])
          
      profit_results = []
      for i in range(len(calc_data)):
        amt = int(calc_data[i][0])
        if '+' in calc_data[i][1]:
          odd = calc_data[i][1].replace('+', '').replace(',', '')
          amt = (amt/100)*int(odd)
        elif '-' in calc_data[i][1]:
          odd = calc_data[i][1].replace('-', '').replace(',', '')
          amt = (amt/int(odd))*100
        amt = round(amt, 2)
        profit_results.append(amt)

      await ctx.send(f'```BET PROFIT FOR {person.upper()} IF {team1.upper()} {result.upper()}S: \n{profit_results}```')

      totalSum = 0
      for i in profit_results:
        totalSum = totalSum + i
      wallet = round(wallet + totalSum, 2)
        
      #FINALLY woot woot 
      await ctx.send(f'```POTENTIAL WALLET: \n{wallet}```')

  @commands.command()
  async def betHistory(self, ctx, person):
    """
      [person] show person's bet history
      """

    person = person.lower()
    if person not in lookups:
        await ctx.send(f':x: {person} is not registered as a player')
        return

    open_file()

  # @commands.command()
  # async def betRecord(self, ctx):
  #   """
  #   best and worst bets of all time
  #   """

  #   betRecord = await open_file("Data/bet_record.txt", ctx)
    
    
    

def setup(bot):
	bot.add_cog(Betting(bot))