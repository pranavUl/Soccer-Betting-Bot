import discord
from discord.ext import commands
from GLOBAL import statsCalculator, lookups, bankUpdate, open_file, historyUpdate, calculateGlobal, key_from_value, player_ids, remove10Global, checkDate
from Cogs.Calculator import Calculator
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import date, datetime

"""
CONTAINS:
- INVEST
- LOAN
- SHOWACTIVE
- COMPOUND / SUNDAY
- WITHDRAW
- LOANPAYMENT
- UPDATE
- REMOVE10
"""

    #entries_by_player = {j:[] for j in lookups}

class Money(commands.Cog):
  def __init__(self, bot):
    self.bot = bot



  @commands.command()
  async def showActive(self, ctx):
    """
    see active deposits, loans, and sponsorships
    """

    #await self.showInvestments(ctx)
    await self.showSponsors(ctx)




  
  #@commands.command(hidden=True)
  async def showInvestments(self, ctx):
    """
    see active deposits and loans
    """

    try:
      with open('Data/deposits-loans.txt', 'r') as fp:
        readableDataFile = fp.read()
    except:
      await ctx.send("❌ File error occured! Please try again later.")

    readableData = []
    for item in readableDataFile:
      item = item.split()
      formattedItem = f"{item[0]:<10}{item[1]:<20}{item[2]:<6}{item[3]:<3}{item[4]:<5}"
      readableData.append(formattedItem)
    readableData = "\n".join(readableData)

    #for i in range(len(readableData)):
    #  
    #  line = readableData[i].split()
    #  await ctx.send(line)
    #  person = str(line[0])
    #  await ctx.send(person)
    # line[2] = await statsCalculator(self, ctx, person, "investment")

    #  try:
    #    with open('Data/sponsorships.txt', 'r') as fp:
    #      readableSponsors = fp.read()
    #  except:
    #    await ctx.send("❌ File error occured! Please try again later.")  
    #
    #  readableSponsors = readableSponsors.split()
    #  sponsorAmts = []
    #  for line2 in readableSponsors:
    #    if line2[0] == line[0]:
    #      sponsorAmts.append(line[2])
    #  
    #  for amt in sponsorAmts:
    #    line[2] = line[2] - amt

    #  line = " ".join(line)

    await ctx.send(f'```ALL ACTIVE DEPOSITS AND LOANS: \n{readableData}```')

  

  
  #@commands.command()
  #@commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def invest(self, ctx, *args):
    """
    [person][amount][rate][period]
    """
  
    #format for entries: PLAYER, D/L, AMT, RATE, PERIOD, WEEKNUMBER
    #example: rithik, D, 50, 5%, 6

    deposits_loans = await open_file('Data/deposits-loans.txt', ctx)
    
    if len(args) != 4:
      await ctx.send("❌ enter every necessary input please")
      return
    person = args[0].lower()
    amount = args[1] 
    rate = args[2]
    period = args[3]

    newEntry = f'{person} D {amount} {rate} {period} 0' 
    deposits_loans.append(newEntry)
    
    if person in lookups:
      try:
        with open('Data/deposits-loans.txt', 'w') as fp:
          for entry in deposits_loans:
            fp.write(f'{entry}\n')
      except:
        await ctx.send("❌ file error occurred, please try again later")
        
    else:
      await ctx.send("❌ enter a valid person")
      return

    wallet = await statsCalculator(self, ctx, person, "wallet")
    investment = await statsCalculator(self, ctx, person, "investment")
    wallet = float(wallet) - float(amount)
    investment = float(investment) + float(amount)
    if investment > wallet:
      await ctx.send("❌ this already violates ffp")
      return
    await bankUpdate(self, ctx, "wallet", person, wallet)
    await bankUpdate(self, ctx, "investment", person, investment)
    await self.showActive(ctx)










  
  @commands.command()
  @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def loan(self, ctx, *args):
    """
    [person][amount][rate][period] no commas
    """

    #format for entries: PLAYER, D/L, AMT, RATE, PERIOD, WEEKNUMBER
    #example: rithik L 50 5% 6

    deposits_loans = await open_file('Data/deposits-loans.txt', ctx)
    
    if len(args) != 4:
      await ctx.send("❌ enter every necessary input please")
      return
    person = args[0].lower()
    amount = args[1] 
    rate = args[2]
    period = args[3]

    newEntry = f'{person} L {amount} {rate} {period}' 
    deposits_loans.append(newEntry)
    
    if person in lookups:
      try:
        with open('Data/deposits-loans.txt', 'w') as fp:
          for entry in deposits_loans:
            fp.write(f'{entry}\n')
      except:
        await ctx.send("❌ file error occurred, please try again later")
        
    else:
      await ctx.send("❌ enter a valid person")
      return

    wallet = await statsCalculator(self, ctx, person, "wallet")
    wallet = float(wallet) + float(amount)
    await bankUpdate(self, ctx, "wallet", person, wallet)
    await bankUpdate(self, ctx, "debt", person, 0-float(amount))
    await self.showActive(ctx)




  
  
  #@commands.command(hidden=True)
  #@commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def compoundInvestment(self, ctx, *args):
    """
    [number] <- investment number in !showActive list
    """

    try:
      number = args[0]
    except:  
      await ctx.send("❌ enter a number")
      return
    
    deposits_loans = await open_file('Data/deposits-loans.txt', ctx)

    try:
      investment = deposits_loans[int(number)-1]
    except:
      await ctx.send("❌ enter a valid deposit index")
      return

    if investment[0] == "ARCHIVED":
      # no message or else itll clog up !sunday
      return

    investment = investment.split()  
    if investment[1] != "D":
      # no message or else itll clog up !sunday
      return
      
    player = str(investment[0]).lower()
    amt = float(investment[2])
    rate = investment[3]
    period = int(investment[4])
    weeksComplete = int(investment[5])

    rate = rate.replace("%", "")
    rate = round(int(rate)/100, 2)
    growth = round(amt*rate, 2)
    amt = round(amt + amt*rate, 2)

    weeksComplete = weeksComplete + 1    
    investment[2] = amt
    investment[5] = weeksComplete
    for i in range(len(investment)):
      investment[i] = str(investment[i])  
    investment = " ".join(investment)

    # remove the now outdated investment line
    deposits_loans.remove(deposits_loans[int(number)-1])

    # if that investment is actually done
    if int(weeksComplete) == int(period):
      # add the investment line into the investment log, but now marked as ARCHIVED, which will be filtered out later
      # inserts at zero so that it doesnt reach it later for !sunday
      deposits_loans.insert(0, "ARCHIVED "+ investment)
      # send funky messages
      await ctx.send(f"```✅ investment for {player} was successfully compounded at {round(rate*100, 1)}%```")
      await ctx.send(f"```🎉 {player}'s investment is complete!```")
      await ctx.send(f"```💰 final investment value: {amt}```")

      statInvestment = await statsCalculator(self, ctx, player, "investment")
      wallet = await statsCalculator(self, ctx, player, "wallet")
      wallet = round(wallet + amt, 2)

      newBankInvestment = int(statInvestment) + int(growth) - int(amt)
      if newBankInvestment < 0:
        newBankInvestment = 0.0
      
      await bankUpdate(self, ctx, "wallet", player, wallet)
      await bankUpdate(self, ctx, "investment", player, newBankInvestment)
      await statsCalculator(self, ctx, player, "print")
    
    
    else:
      # otherwise, the investment shall continue, just reappend it
      # and print funky stats
      deposits_loans.insert(0, investment)
      await ctx.send(f"```✅ investment for {player} was successfully compounded at {round(rate*100, 1)}%```")
      
      statInvestment = await statsCalculator(self, ctx, player, "investment")
      await bankUpdate(self, ctx, "investment", player, round(statInvestment + growth, 2))

    # everythings been printed, now just actually write it to the file
    try:
      with open('Data/deposits-loans.txt', 'w') as fp:
        for entry in deposits_loans:
          fp.write(f'{entry}\n')
    except:
      await ctx.send("❌ file error occurred, please try again later")











  

  @commands.command()
  @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def withdraw(self, ctx, person, number, request):
    """
    [person][investment id][amount or all]
    """
    all_investments = await open_file("Data/deposits-loans.txt", ctx)

    personInvestment = all_investments[int(number)-1].split()

    if personInvestment[1] != "D":
        await ctx.send("❌ thats not an investment!")
        return
    
    bankInvestment = await statsCalculator(self, ctx, person, "investment")
    wallet = await statsCalculator(self, ctx, person, "wallet")

    bankInvestment = float(bankInvestment)

    if person != personInvestment[0]:
      await ctx.send("❌ person does not match investment person")
      return
      
    if request == "all":
      wallet = round(wallet + float(personInvestment[2]) - float(personInvestment[2])*0.2, 2)
      personInvestment[2] = 0.0
      bankInvestment = round(bankInvestment - float(personInvestment[2]), 2)
    else:
      request = float(request)
      personInvestment[2] = float(personInvestment[2])
      try:
        if request <= personInvestment[2]:
          personInvestment[2] = round(personInvestment[2] - request, 2)
          wallet = round(wallet + request - request*0.2, 2)
          bankInvestment = round(bankInvestment - request, 2)
        else:
          await ctx.send("❌ your investment isn't that large")
          return
      except:
        await ctx.send("❌ you've made a mistake!")
        return

    for i in range(len(personInvestment)):
      personInvestment[i] = str(personInvestment[i])  
    personInvestment = " ".join(personInvestment)
    all_investments[int(number)-1] = personInvestment
    
    try:
      with open('Data/deposits-loans.txt', 'w') as fp:
        for entry in all_investments:
          fp.write(f'{entry}\n')
    except:
      await ctx.send("❌ file error occurred, please try again later")
      return

    await bankUpdate(self, ctx, "wallet", person, wallet)
    await bankUpdate(self, ctx, "investment", person, bankInvestment)
    await ctx.send(f"```✅ {request} successfully withdrawn from the investment for {person}```")
















  
  @commands.command()
  @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def loanPayment(self, ctx, person, number, request):
    """
    [person][loan id][amount or all] use all on final payment
    """
    all_investments = await open_file("Data/deposits-loans.txt", ctx)

    personLoan = all_investments[int(number)-1].split()

    if personLoan[1] != "L":
      await ctx.send("❌ thats not a loan!")
      return
    
    bankLoan = await statsCalculator(self, ctx, person, "debt")
    wallet = await statsCalculator(self, ctx, person, "wallet")

    bankLoan = float(bankLoan)

    if person != personLoan[0]:
      await ctx.send("❌ person does not match loan person")
      return

    rate = float(personLoan[3].replace("%", ""))/100
    
    if request == "all":
      wallet = round(wallet - float(personLoan[2]) - float(personLoan[2]*rate), 2)
      personLoan[2] = 0.0
      bankLoan = 0.0
      await ctx.send(f'```🎉 {person}s debt is fully paid off!```')
      
    else:
      request = float(request)
      personLoan[2] = float(personLoan[2])
      try:
        if request <= personLoan[2]:
          personLoan[2] = round(personLoan[2] - request, 2)
          wallet = round(wallet - request - request*rate, 2)
          bankLoan = round(bankLoan + request, 2)
        else:
          await ctx.send("❌ your loan isn't very large")
          return
      except:
        await ctx.send("❌ you've made a mistake!")
        return

      for i in range(len(personLoan)):
        personLoan[i] = str(personLoan[i])  
      personLoan = " ".join(personLoan)
      all_investments[int(number)-1] = personLoan

      await ctx.send(f"```✅ {request} successfully paid off from the loan for {person}```")
    
    try:
      with open('Data/deposits-loans.txt', 'w') as fp:
        for entry in all_investments:
          fp.write(f'{entry}\n')
    except:
      await ctx.send("❌ file error occurred, please try again later")
      return

    await bankUpdate(self, ctx, "wallet", person, wallet)
    await bankUpdate(self, ctx, "debt", person, bankLoan)











  
  @commands.command(hidden=True)
  @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def update(self, ctx, *args): 
      """
      [w/i/d][person][new amt] update bank manually. host/finance only.
      """
      await bankUpdate(self, ctx, args[0], args[1], args[2])
      await statsCalculator(self, ctx, args[1], "print")






  
  @commands.command()
  async def tipFred(self, ctx, *args):
    """
    give the bot $1
    """
    person = key_from_value(player_ids, str(ctx.author.id))

    currentwallet = await statsCalculator(self, ctx, person, "wallet")
    currentwallet = currentwallet - 1
    
    await bankUpdate(self, ctx, 'wallet', person, currentwallet)

    await ctx.send("thanks for the $1!")
    # await ctx.send(":smiling_face_with_3_hearts: :monkey:  _fred whispers_: i like ~~~nuts~~~")
    # await ctx.send("💋 :kiss: mwahf")
    # await ctx.send(":smiling_face_with_3_hearts: :gun: :monkey:  _fred whispers_: give me ur ~~~nuts~~~ money")






  
  
  @commands.command()
  @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def remove10(self, ctx, *, person): 
    await remove10Global(self, ctx, person)










  
  @commands.command()
  @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def manualSaveHistory(self, ctx, *args):
    """
    Manually saves history. Hosts only
    """
    await historyUpdate(self, ctx)
    await ctx.send("```📝 history made!```")


  @commands.command(hidden=True)
  @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def compoundSponsor(self, ctx, *args):
    """
    [number][matchweek]
    """

    #await ctx.send("not yettt")
    #return
    
    try:
      number = args[0]
    except:  
      await ctx.send("❌ enter a number")
      return
    
    try:
      if args[1] != "midweek" and args[1] != "weekend":
        await ctx.send("❌ enter a 1 or 2 to specify which matchweek to compound (either is fine for teams with just one)")
        return
      else:
        matchweek = args[1]
    except:  
      await ctx.send("❌ enter a matchweek")
      return
    
    sponsorships = await open_file('Data/sponsorships.txt', ctx)

    try:
      sponsorship = sponsorships[int(number)-1]
    except:
      await ctx.send("❌ enter a valid deposit index")
      return

    if sponsorship[0] == "ARCHIVED":
      # no message or else itll clog up !sunday
      return

    sponsorship = sponsorship.split()  
      
    player = str(sponsorship[0]).lower()
    team = str(sponsorship[1]).lower()
    amt = float(sponsorship[2])
    term = sponsorship[3]
    weeksComplete = int(sponsorship[4])
    rate = float(str(sponsorship[5]).replace("%",""))


    
    async def findMatch(team, matchweek):
    #  
      all_odds = await open_file("Data/odds.txt", ctx)
      for odd in all_odds:
        oddIndex = all_odds.index(odd)
        odd = odd.replace(f"{odd.split()[0]} ", "")
        all_odds[oddIndex] = odd
      all_odds.sort()
      match = ""
      fixture = ''
      for odd in all_odds:
        if team in odd:
          oddDateFormatted = datetime.strptime(odd.split()[0], '%Y-%m-%d')
          if (matchweek == "midweek" and 0 < oddDateFormatted.weekday() < 4) or (matchweek == "weekend" and (3 < oddDateFormatted.weekday() < 7 or oddDateFormatted.weekday() == 0)):
            fixture = odd
        else:
          continue
      
      if fixture == '':
        #await ctx.send(f"```❌ no matches were found for {team} this {matchweek}```")
        return "fail"

      match = f'league {fixture}'
      
      if len(match.split()) != 10:
        #print("ERROR" + match)
        await ctx.send(f"```❌ results haven't been posted for {team} during this {matchweek}```")
        
    #    await ctx.send(f"```❌ the error match in question: \n{match}```")
        return "fail"
      
      matchWinner = match.split()[9].replace("[", "").replace("]", "")
      
      
      if matchWinner == "postponed":
        await ctx.send(f"```❌ {team}'s match in matchweek {matchweek} was postponed!```")
        return "fail"
      elif matchWinner != team:
        return "no"
      else:
        return "yes"
        
      
    matchResult = await findMatch(team, matchweek)
    if matchResult == "fail":
      return
    if matchResult == "no":
      try:  
        await ctx.send(f"```🔻 sponsorship for {player} did not increase because {team} failed to win their {matchweek} match this week```")
        weeksComplete = weeksComplete + 1
        sponsorship[4] = weeksComplete
        for i in range(len(sponsorship)):
          sponsorship[i] = str(sponsorship[i])  
        sponsorship = " ".join(sponsorship)
        sponsorships.remove(sponsorships[int(number)-1])

        if int(weeksComplete) == int(term):
          sponsorships.insert(0, f"ARCHIVED {sponsorship}")
          await ctx.send(f"```🎉 {player}'s sponsorship is finished!```")
          await ctx.send(f"```💰 final sponsorship value: {amt}```")
    
          statInvestment = await statsCalculator(self, ctx, player, "investment")
          wallet = await statsCalculator(self, ctx, player, "wallet")
          wallet = round(wallet + amt, 2)
    
          newBankInvestment = round(float(statInvestment) - float(amt), 2)
          if newBankInvestment < 0:
            newBankInvestment = 0.0
    
          
          await bankUpdate(self, ctx, "wallet", player, wallet)
          await bankUpdate(self, ctx, "investment", player, newBankInvestment)
          await statsCalculator(self, ctx, player, "print")

          try:
            with open('Data/sponsorships.txt', 'w') as fp:
              for entry in sponsorships:
                fp.write(f'{entry}\n')
          except:
            await ctx.send("❌ file error occurred, please try again later")
            return
          return
        else:  
          sponsorships.insert(0, sponsorship)
          try:
            with open('Data/sponsorships.txt', 'w') as fp:
              for entry in sponsorships:
                fp.write(f'{entry}\n')
          except:
            await ctx.send("❌ file error occurred, please try again later")
            return
          return
      except:
          await ctx.send("❌ unexpected error in sponsorship failure tracking")
    
    rate = rate/100
    growth = round(amt*rate, 2)
    amt = round(amt + amt*rate, 2)
    
    weeksComplete = weeksComplete + 1
    sponsorship[2] = amt
    sponsorship[4] = weeksComplete
    for i in range(len(sponsorship)):
      sponsorship[i] = str(sponsorship[i])  
    sponsorship = " ".join(sponsorship)

    # remove the now outdated investment line
    sponsorships.remove(sponsorships[int(number)-1])

    # if that investment is actually done
    if int(weeksComplete) == int(term):
      # add the investment line into the investment log, but now marked as ARCHIVED, which will be filtered out later
      # inserts at zero so that it doesnt reach it later for !sunday
      sponsorships.insert(0, f"ARCHIVED {sponsorship}")
      # send funky messages
      await ctx.send(f"```🌲 {player}'s sponsorship for {team} was successfully compounded at {round(rate*100, 2)}%```")
      await ctx.send(f"```🎉 {player}'s sponsorship is finished!```")
      await ctx.send(f"```💰 final sponsorship value: {amt}```")

      statInvestment = await statsCalculator(self, ctx, player, "investment")
      wallet = await statsCalculator(self, ctx, player, "wallet")
      wallet = round(wallet + amt, 2)

      newBankInvestment = int(statInvestment) + int(growth) - int(amt)
      if newBankInvestment < 0:
        newBankInvestment = 0.0

      
      await bankUpdate(self, ctx, "wallet", player, wallet)
      await bankUpdate(self, ctx, "investment", player, newBankInvestment)
      await statsCalculator(self, ctx, player, "print")
    
    
    else:
      # otherwise, the investment shall continue, just reappend it
      # and print funky stats
      sponsorships.insert(0, sponsorship)
      await ctx.send(f"```🌲 {player}'s sponsorship for {team} was successfully compounded at {round(rate*100, 2)}%```")
      
      statInvestment = await statsCalculator(self, ctx, player, "investment")
      await bankUpdate(self, ctx, "investment", player, round(statInvestment + growth, 2))

    # everythings been printed, now just actually write it to the file
    try:
      with open('Data/sponsorships.txt', 'w') as fp:
        for entry in sponsorships:
          fp.write(f'{entry}\n')
    except:
      await ctx.send("❌ file error occurred, please try again later")
  
  @commands.command()
  @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def sunday(self, ctx, *args):
    """
    Compound all investments and sponsorships [midweek/weekend]
    """
    #deposits_loans = await open_file('Data/deposits-loans.txt', ctx)
    #for i, line in enumerate(deposits_loans):
    #  splitline = line.split()
    #  if splitline[1] == 'D':
    #    await self.compoundInvestment(ctx, i+1) # since ids count from 1, not 0

    matchweek = ""
    try:
      if args[0] != "midweek" and args[0] != "weekend":
        await ctx.send("❌ enter a 1 or 2 to specify which matchweek to compound")
        return
      else:
        matchweek = args[0]
    except:  
      await ctx.send("❌ enter either [midweek] or [weekend]")
      return

    #try:
    sponsorships = await open_file('Data/sponsorships.txt', ctx)
    for i, line in enumerate(sponsorships):
        await self.compoundSponsor(ctx, i+1, matchweek) # since ids count from 1, not 0
    #except:
    #  await ctx.send("❌ error in bulk sponsorship compounding")
    #  return

  @commands.command()
  @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def superSunday(self, ctx, *args):
    """
    Compounds, calculates bets, and writes to history!
    """
    try:
      await ctx.send("```💰 compounding...```")
      await self.sunday(ctx, "weekend")
      await ctx.send("```🔢 calculating bets...```")
      for player in lookups:
        await calculateGlobal(self, ctx, player)
      await ctx.send("```✏️ making history...```")
      await historyUpdate(self, ctx)
      await ctx.send("```🎉 all done!```")
    except:
      await ctx.send("🚨 error encountered, halting superSunday 🚨")
      return


  @commands.command(hidden=True)
  @commands.has_any_role("host", "finance management")
  async def archiveInvestments(self, ctx):
    """
    To archive old investments and sponsorships. Only managers can use this.
    """
    try:
      with open('Data/deposits-loans.txt', 'r+') as fp:
        with open('Data/archived_investments.txt', 'a') as fp2:
          deposit_list = fp.readlines()
          fp.seek(0)
          for line in deposit_list:
            if "ARCHIVED" in line:
              fp2.write(line)
            else:
              fp.write(line)
        fp.truncate()

      await ctx.send(f"✅ Finished investments were archived")
      
    except:
      await ctx.send("❌ File error occured! Please try again later.")

    try:
        with open('Data/sponsorships.txt', 'r+') as fp:
          with open('Data/archived_investments.txt', 'a') as fp2:
            deposit_list = fp.readlines()
            fp.seek(0)
            for line in deposit_list:
              if "ARCHIVED" in line:
                fp2.write(line)
              else:
                fp.write(line)
          fp.truncate()
  
        await ctx.send(f"✅ Finished sponsorships were archived")
      
    except:
      await ctx.send("❌ File error occured! Please try again later.")


  
  @commands.command(hidden=True)
  async def showSponsors(self, ctx):
    """
    see active sponsorships
    """

    try:
      with open('Data/sponsorships.txt', 'r') as fp:
        readableDataFile = fp.read()
    except:
      await ctx.send("❌ File error occured! Please try again later.")

    readableData = []
    for item in readableDataFile.split("\n"):
      item = item.split()
      if item == []:
        break
      formattedItem = f"{item[0]:<15}{item[1]:<27}{item[2]:<14}{item[3]:<11}{item[4]:<14}{item[5]:<10}"
      readableData.append(formattedItem)
    readableData = "\n".join(readableData)

    space = " "
    person = "person"
    team = "team"
    amount = "amount"
    term_length = "term"
    weeks_elapsed = "elapsed"
    interest_rate = "rate" 

    title = "ALL ACTIVE SPONSORSHIP PROGRAMS"

    await ctx.send(f"```{title.center(87)}```")
    
    await ctx.send(f'```{person.upper():<15}{team.upper():<27}{amount.upper():<14}{term_length.upper():<11}{weeks_elapsed.upper():<14}{interest_rate.upper():<10}```')

    await ctx.send(f'```{readableData}```')


  
  @commands.command()
  @commands.has_any_role("host", "finance management", "chief host-executive financial officer")
  async def sponsor(self, ctx, *args):
    """
    sponsor an underdog team! ping a host to do so. [person][team][amount][term/weeks][rank last season]
    """

    sponsorships = await open_file('Data/sponsorships.txt', ctx)

    
    current_date = date.today()
    #dateCheck = await checkDate(ctx, current_date, *args, 1, 1)
    #if dateCheck == False:
    #  return
    
    if len(args) != 5:
      await ctx.send("❌ enter every necessary input please")
      return
    
    person = args[0].lower()
    team = args[1].lower()
    amount = args[2]
    term = args[3]
    starting7 = int(args[4])
    startingPlace = int(args[4])

    places = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    if startingPlace not in places:
      await ctx.send("❌ an underdog has to be from 11 to 20th place")
      return

    starting7 = starting7 -2
    startingPlace = startingPlace -2
    
    if starting7 == 14:
      rate = 0.07
      multiplier = round(starting7/10, 2)
      rate = round(rate*multiplier*100, 2)
    else:
      rate = startingPlace/100/2
      multiplier = round(starting7/10, 2)
      rate = round(rate*multiplier*100, 2)
    

    all_odds = await open_file("Data/odds.txt", ctx)
    
    checker = 0
    for odd in all_odds:
      if team not in odd:
        continue
      else:
        checker = 1
    if checker != 1:
      await ctx.send("❌ requested team was not found in odds")
      return

    newEntry = f'{person} {team} {amount} {term} 0 {rate}%' 
    sponsorships.append(newEntry)

    wallet = await statsCalculator(self, ctx, person, "wallet")
    investment = await statsCalculator(self, ctx, person, "investment")
    investment2 = investment
    wallet2 = wallet
    wallet = float(wallet) - float(amount)
    investment = float(investment) + float(amount)
    if investment > wallet:
      await ctx.send(f"❌ the maximum you can do is ``{round((wallet2-investment2)/2, 2)}``")
      return
    
    
    if person in lookups:
      try:
        with open('Data/sponsorships.txt', 'w') as fp:
          for entry in sponsorships:
            fp.write(f'{entry}\n')
      except:
        await ctx.send("❌ file error occurred, please try again later")
        
    else:
      await ctx.send("❌ enter a valid person")
      return
    
    
    
    await bankUpdate(self, ctx, "wallet", person, wallet)
    await bankUpdate(self, ctx, "investment", person, investment)
    await ctx.send(f'```✅ {person.upper()} IS NOW SPONSORING {team.upper()}!```')
    await self.showSponsors(ctx)
  
      
def setup(bot):
	bot.add_cog(Money(bot))