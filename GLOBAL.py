from datetime import date, datetime
import random
import discord

async def open_file(file, ctx):
  try:
    with open(file, "r") as fp:
      l = fp.read().splitlines()
      return l
  except:
    await ctx.send("❌ File error occured! Please try again later.")
    return []

async def get_match(submissionID, odds):
  submissionID = int(submissionID) - 1
  match = odds[submissionID]
  match = match.replace(".", " ").split(" ")
  homeTeam = match[4]
  awayTeam = match[6]
  match = f'{homeTeam} {awayTeam}'
  return match
  
  

def key_from_value(d, v):
  # its hard to get the key of a dictionary from its value, you have to do it this complicated way, so lets abstract it to this function
  return list(d.keys())[list(d.values()).index(v)]


try:
  with open("Data/WCgroups.txt", "r") as fp:
      wc_groups = fp.read().splitlines()
except:
  print("!! UNEXPECTED ERROR IN FINDING WC GROUPS !!")
  exit()
print(wc_groups)
print(" * WC groups found successfully \n")

try:
  with open("Data/lookups.txt", "r") as fp:
      lookups = fp.read().splitlines()
except:
  print("!! UNEXPECTED ERROR IN FINDING PLAYER LOOKUPS !!")
  exit()
print(lookups)
print(" * Lookups found successfully \n")

try:
  with open("Data/ubcl.txt", "r") as fp:
      ubcl_lookups = fp.read().splitlines()
except:
  print("!! UNEXPECTED ERROR IN FINDING PLAYER LOOKUPS !!")
  exit()
print(" * UBCL found successfully \n")

try:
  with open("Data/ubel.txt", "r") as fp:
      ubel_lookups = fp.read().splitlines()
except:
  print("!! UNEXPECTED ERROR IN FINDING PLAYER LOOKUPS !!")
  exit()
print(" * UBEL found successfully \n")

# OLD, SEE BELOW PROGRAMMATIC APPROACH
player_ids = {
    'pranav': '857021549554302987',
    'ahyan': '785596136219344916',
    'john': '713105065849651331',
    'jonathan': '830842310815645706',
    'rithik': '940745733546577920',
    'eric': '697833592382029826'
  }

#PLAYER IDS FROM FILE

try:
  with open("Data/player_ids.txt", "r") as fp:
      player_ids_list = fp.read().splitlines()
except:
  print("!! UNEXPECTED ERROR IN FINDING PLAYER IDS !!")
  exit()


for i in range(len(player_ids_list)):
  id = player_ids_list[i]
  id = id.replace(", ", " ").split(" ")
  player_ids_list[i] = id
  
  
player_ids = {}
for i in range(len(lookups)):
  player_ids[f'{lookups[i]}'] = player_ids_list[i][1]

print(player_ids)
print(" * Player ids found successfully \n")


async def statsCalculator(self, ctx, *args): 
  #arg[0] is person #arg[1] is printNeed

    bank_numbers = []
    try:
      with open("Data/bank.txt", "r") as fp:
        bank_numbers = fp.read().splitlines()
    except:
      await ctx.send("❌ File error occured! Please try again later.")
      return

    person = args[0]
    person = person.lower()

    index = None
    try:
      index = lookups.index(person) * 3
    except ValueError:
      await ctx.send(f"❌ Invalid input, enter a valid name")
      return

    w, i, d = bank_numbers[int(index)], bank_numbers[int(index)+1], bank_numbers[int(index)+2]
    w, i, d = float(w), float(i), float(d)

    n = round(w + i + d, 2)
    #ir = abs(round(i/(w+i), 2))
    win = round(n - i, 2)

    #ffpcheck = ((w+i)/2)-i

    #rank calculator
    rank = 1
    for h in range(0, len(bank_numbers), 3):
      indexWorth = float(bank_numbers[h]) + float(bank_numbers[h+1]) + float(bank_numbers[h+2])
      if indexWorth > n:
        rank = rank + 1
      
    #if ir > 0.5:
    #  ffpBreach = " **ffp broken**"
    #else:
    #  ffpBreach = ""

    if args[1] == "print":
      await ctx.send(f"```{person.upper()}'S FINANCES: \nRank: {rank} \nWallet: {w} \nInvestments: {i} \nDebts: {d} \nNet Worth: {n}```")
      return
    elif args[1] == "wallet":
      return w
    elif args[1] == "net worth":
      return n
    elif args[1] == "investment":
      return i
    elif args[1] == "debt":
      return d
    #elif args[1] == "ffpcheck":
    #  return ffpcheck

## GAUTHAM'S COMPREHENSIONS CODE '##
      
      #organized_odds = {k[k.find(" ")+1:-1]: [int(i) for i in v.split(", ")] for k, v in [odd.split(": ") for odd in all_odds]}
      #organized_bets_lists = [bet.replace(" ", "X", 1).split(" ") for bet in range(2, 6) in all_bets] #X is a placeholder, so the first space is ignored
      #organized_bets = {}
      #for k, v in [(i[0][i[0].find("X")+1:], (int(i[1]), i[2])) for i in organized_bets_lists]:
      #  if k not in organized_bets:
      #    organized_bets[k] = [v]
      #  else:
      #    organized_bets[k].append(v)

async def bankUpdate(self, ctx, *args): 

    if len(args) != 3:
      await ctx.send("❌ Enter the info correctly")
    else:
      data = args[0].lower()
      person = args[1].lower()
      newAmt = str(args[2])
      
    try:
      with open('Data/bank.txt', 'r') as fp:
        bank_data = fp.readlines()
    except:
      await ctx.send("❌ File error occured! Please try again later. Error code 01")

    index = None
    try:
      index = lookups.index(person) * 3
    except ValueError:
      await ctx.send(f"❌ Invalid input, enter a valid name")
      return

    if data == "wallet":
      index = int(index)
    elif data == "investment":
      index = int(index) + 1
    elif data == "debt":
      index = int(index) + 2
    else:
      await ctx.send(f"❌ Invalid input, enter a valid bank account")
      return

    newAmt = newAmt + "\n"
    try:
      bank_data[index] = newAmt
    except:
      bank_data.append(newAmt)
      
    try:
      with open('Data/bank.txt', 'w') as fp:
        for line in bank_data:
          fp.write(line)
    except:
      await ctx.send("❌ File error occured! Please try again later. Error code 03")

    # await statsCalculator(self, ctx, person, "print")

async def historyUpdate(self, ctx):
  dt_string = datetime.now().strftime("%d/%m/%Y:::%H:%M:%S")
  try:
    with open('Data/bank.txt', 'r') as fp:
      fpl = fp.read().splitlines()
      try:
        with open('Data/archived_bank.txt', 'a') as fp2:
          for line in fpl:
            fp2.write(line + '\n')
          fp2.write(f'||{dt_string}||\n')
      except:
        await ctx.send("❌ File error occured! Please try again later. Error code 00")
  except:
    await ctx.send("❌ File error occured! Please try again later. Error code 02")

async def getAllData(self, ctx):
  fp = open("Data/archived_bank.txt", "r")
  sfp = fp.read().splitlines()
  all_entries = []
  temporary_container = []
  for i, line in enumerate(sfp):
    # for each line in the bank history
    if line[0] == '|':
      # if we reach a line marking the end of a log, append what we collected above to all_entries and refresh the temporary log
      all_entries.append(temporary_container)
      temporary_container = []
    else:
      # add each line to the temporary log
      temporary_container.append(line)

  entries_by_player = {j:[] for j in lookups}

  for i in range(len(lookups)):
    # get the point in the data where that player's entries start; since there are three lines per person, multiply the player by three
    a = i * 3 # file starting point
    d = [] # current player data

    def gather_player_data(offset):
      d.append(
        # to the data for this player, go through each entry (each moemnt in time) in all_entries and add the line within that entry at the file starting point for this player, plus the subindex for the value (wallet, investments, debts) the code is looking for
        [float(entry[a+offset]) for entry in all_entries]
      )
    
    gather_player_data(0) # wallet
    gather_player_data(1) # investments
    gather_player_data(2) # debts

    # for each entry, each moment in time the archive was saved to, for each "column", as it is, in the old spreadsheet
    # for each "column", add the first, second, and third "rows": wallet, investments, and debts, to create...
    d.append( # networth
      [round(d[0][j] + d[1][j] + d[2][j], 2) for j in range(len(all_entries))]
    )
    # try:
    #   d.append( # investment ratio
    #     [round(d[1][j]/(d[0][j] + d[1][j]), 2) for j in range(len(all_entries))]
    #   )
    # except ZeroDivisionError:
    #   await ctx.send("YOUR NET WORTH IS ZERO LMAOOOO I QUIT")
    #   return
    d.append( # winnings
      [round(d[3][j] - d[1][j], 2) for j in range(len(all_entries))]
    )

    # lookups[i] returns the name of the player, which is the key of the entries_by_player dict
    entries_by_player[lookups[i]] = d
    
  return entries_by_player

async def calculateGlobal(self, ctx, person):

  await ctx.send(f'```⚽ RESULTS FOR {person.upper()}```')
  
  all_bets = []
  all_odds = []
  
  all_bets = await open_file("Data/bets.txt",  ctx)
  all_odds = await open_file("Data/odds.txt", ctx)
  
  #check if match results were input into odds
  for i in range(len(all_odds)):
    match_odd = all_odds[i].split()       
    print(match_odd)
    #if len(match_odd) != 10:
    #  await ctx.send(f"```❌ pls enter all match results before calculating```")
    #  return 
  
  person = person.lower()

  #finds wallet for person
  wallet = await statsCalculator(self, ctx, person, "wallet")
  
  #finds necessary bet data
  organized_bet_data = [[this_bet.split()[h] for h in range(2, 6)] for this_bet in all_bets if this_bet.split()[1] == person] 

  #error check
  fredCounter = False
  
  if person not in lookups:
    await ctx.send(f'❌ {person} is not registered as a player')
    return
  elif organized_bet_data == []:

    #### FRED AUTOBET SYSTEM ####

    ### write bet into file
    current_date = date.today()
    odds = await open_file('Data/odds.txt', ctx)
    player_wallet = await statsCalculator(self, ctx, person, "wallet")

    #finds a random match and team
    uB = len(odds)-1
    randomOdd = random.randint(0, uB)
    match = odds[randomOdd].replace(".v.", " ").split()
    randomTeam = random.randint(0, 4)
    if randomTeam < 2:
      team1 = match[4]
      team2 = match[5]
      result = "win"
    elif randomTeam == 2:
      team1 = match[4]
      team2 = match[5]
      result = "draw"
    else:
      team1 = match[5]
      team2 = match[4]
      result = "win"

    bet = f"{current_date} {person} {round(0.1*player_wallet, 2)} {team1} {result} {team2} \n"

    await ctx.send(f'```AUTOBET: {bet.split()[2]} {bet.split()[3]} {bet.split()[4]} {bet.split()[5]}```')

    fredCounter = True

    try:
        with open("Data/bets.txt", 'a') as fp:
          fp.write(bet)
        fp.close()
    except:
        await ctx.send("❌ File error occured! Please try again later.")

    bet = bet.split()
    bet2 = [bet[2], bet[3], bet[4], bet[5]]

    organized_bet_data = [bet2]
    
    ## OLD SYSTEM ##
    
    #await remove10Global(self, ctx, person)
    #newWallet = await statsCalculator(self, ctx, person, "wallet")
    #await ctx.send(f'```{person} placed no bets bruh```')
    #await ctx.send(f'```{person.upper()}s WALLET: {round(newWallet)}MB```')
    #return

  #cleans odds
  for i in range(len(all_odds)):
    try:
      all_odds[i] = all_odds[i].replace(".v.", " ").replace(":","").replace("]", "").replace("[", "").replace("(", "").replace(")", "").split()
    except:
      await ctx.send(f'❌ bracket reading error in match results')
  
  #finding necessary odds (non listcomp version):
  organized_odds_data = []
  for bet in organized_bet_data:
    for odd in all_odds:
      if bet[1] in odd and bet[3] in odd:
        organized_odds_data.append(odd)

  #error check
  if organized_odds_data == []:
    await ctx.send(f'```❌ something went wrong \ncan\'t find odds matching any bets```')
    #await remove10Global(self, ctx, person)
    #newWallet = await statsCalculator(self, ctx, person, "wallet")
    #await ctx.send(f'```{person.upper()}s WALLET: {round(newWallet)}MB```')
    return
    
  calc_data = []
  not_calculated = []
  fredWin = False
  
  for bet in organized_bet_data:
    calcOdd = None
    
    for odd in organized_odds_data:
      if odd[8] == "postponed":
        not_calculated.append(bet)
        continue
      #if win success
      elif bet[1] == odd[8] and bet[2] == "win" and bet[3] in odd:
        #await ctx.send(f"```✅ {person}'s bet on {bet[1]} to {bet[2]} for {bet[0]}MB won!```")
        if fredCounter == True:
          fredWin = True
        
        if odd[3] == odd[8]:
          calcOdd = odd[5]
          
          break
        if odd[4] == odd[8]:
          calcOdd = odd[7]
          
          break

      #if draw success
      elif odd[8] == "draw" and bet[2] == "draw" and odd.count(bet[1]) == 1 and bet[3] in odd:
        calcOdd = odd[6]
        #await ctx.send(f"```✅ {person}'s bet on {bet[1]} to {bet[2]} for {bet[0]}MB won!```")
        if fredCounter == True:
          fredWin = True
        
        break

      #if failed draw or win predict
      elif ((bet[1] != odd[8] and bet[1] in odd) or (bet[2] == "draw" and bet[2] != odd[8] and bet[1] in odd)) and bet[3] in odd:
        calcOdd = "Loss"
        #await ctx.send(f"```❌ {person}'s bet on {bet[1]} to {bet[2]} for {bet[0]}MB failed```")
        if fredCounter == True:
          fredWin = False
        
        
        break
      
    if calcOdd != None:
      calc_data.append([bet[0], calcOdd, bet[1], bet[2]])

  print(not_calculated)

  profit_results = []
  winCount = 0
  lossCount = 0
  for i in range(len(calc_data)):
    amt = float(calc_data[i][0])
    if '+' in calc_data[i][1]:
      odd = calc_data[i][1].replace('+', '').replace(',', '')
      amt = (amt/100)*int(odd)
    elif '-' in calc_data[i][1]:
      odd = calc_data[i][1].replace('-', '').replace(',', '')
      amt = (amt/int(odd))*100
    elif calc_data[i][1] == 'Loss':
      amt = 0 - amt
    try:
      amt = round(amt, 2)
    except:
      await ctx.send("```⚠️ error in amount type while calculating profit results```")
      return

    try:
      if amt >= 0:
        winCount = winCount +1
      elif amt < 0:
        lossCount = lossCount + 1
    except:
      await ctx.send("```⚠️ error in win and loss reporting```")
      
    profit_results.append(amt)

  print_profit_results = ""
  for i in range(len(profit_results)):
      print_result = f'{profit_results[i]} on {calc_data[i][2]} to {calc_data[i][3]}\n'
      print_profit_results = print_profit_results + print_result
  await ctx.send(f'```PROFIT PER BET FOR {person.upper()}: \n{print_profit_results}```')

  try:
    await ctx.send(f'```WINS: {winCount}\nLOSSES: {lossCount}```')
  except:
    await ctx.send("```⚠️ win loss report fail```")

  totalSum = 0
  for i in profit_results:
    totalSum = totalSum + i
  wallet = round(wallet + totalSum, 2)

  
  if totalSum < 0:
    await ctx.send(f'```NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
  elif totalSum > 0:
    await ctx.send(f'```NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
  else:
    await ctx.send(f'```NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
    
  #UPDATE FRED TRACKER
  if fredWin == True:
    try:
        with open("Data/fred_autobets.txt", 'a') as fp:
          fp.write(f"{organized_bet_data[0]} [W]")
        fp.close()
    except:
        await ctx.send("❌ File error occured! Please try again later.")
  elif fredWin == False:
    try:
        with open("Data/fred_autobets.txt", 'a') as fp:
          fp.write(f"{organized_bet_data[0]} [L]")
        fp.close()
    except:
        await ctx.send("❌ File error occured! Please try again later.")
    
  #FINALLY woot woot 
  await ctx.send(f'```WALLET FOR {person.upper()}: \n{wallet}```')

  await bankUpdate(self, ctx, "wallet", person, wallet)





async def globalCheckStake(self, ctx, person):
  person = person.lower()
  if (not person) or (person not in lookups):
    await ctx.send("you did not enter a player; which player would you like to check?")
    return
  betsData = await open_file("Data/bets.txt", ctx)
  atStake = [float(line.split()[2]) for line in betsData if line.split()[1] == person]
  atStake = str(round(sum(atStake), 2))
  await ctx.send(f"```{person.title()} has bet {atStake} so far in this round.```")


async def globalNet(self, ctx, person):
  person = person.lower()
  await globalCheckStake(self, ctx, person)
  if (not person) or (person not in lookups):
    await ctx.send("you did not enter a player; which player would you like to check?")
    return
  betsData = await open_file("Data/bets.txt", ctx)
  atStake = [float(line.split()[2]) for line in betsData if line.split()[1] == person]
  atStake = str(round(sum(atStake), 2))
  if atStake == 0:
    #await ctx.send(f"```{person.title()} has bet {atStake} so far in this round.```")
    return "fail"
  else:
    #await ctx.send(f"```{person.title()} has bet {atStake} so far in this round.```")

    all_bets = []
    all_odds = []
    
    all_bets = await open_file("Data/bets.txt",  ctx)
    all_odds = await open_file("Data/odds.txt", ctx)
    bet_record_file = await open_file("Data/bet_record.txt", ctx)
    bet_win_record = []
    bet_loss_record = []
    for bet in bet_record_file:
      bet = bet.split()
      if bet[0] == "W":
        bet_win_record.append(bet)
      else:
        bet_loss_record.append(bet)
    
    person = person.lower()
  
    #finds wallet for person
    wallet = await statsCalculator(self, ctx, person, "wallet")
    
    #finds necessary bet data
    organized_bet_data = [[this_bet.split()[h] for h in range(2, 6)] for this_bet in all_bets if this_bet.split()[1] == person] 
  
    #cleans odds
    for i in range(len(all_odds)):
      try:
        all_odds[i] = all_odds[i].replace(".v.", " ").replace(":","").replace("]", "").replace("[", "").replace("(", "").replace(")", "").split()
      except:
        await ctx.send(f'❌ bracket reading error in match results')
    
    #finding necessary odds (non listcomp version):
    organized_odds_data = []
    for bet in organized_bet_data:
      for odd in all_odds:
        if bet[1] in odd and bet[3] in odd:
          organized_odds_data.append(odd)
      
    calc_data = []
    potential_calc_data = []
    roundComplete = "yes"
    unknownResult = 0
    
    for bet in organized_bet_data:
      calcOdd = None
      calcOddP = None
      recordOdd = None
      
      for odd in organized_odds_data:
        if len(odd) < 9:
          roundComplete = "no"

          #if draw          
          if bet[2] == "draw" and bet[1] in odd and bet[3] in odd:
            calcOddP = odd[6]
            break

          #if win
          elif bet[1] == odd[3] and bet[2] == "win" and bet[3] in odd:
            calcOddP = odd[5]
            break
          elif bet[1] == odd[4] and bet[2] == "win" and bet[3] in odd:
            calcOddP = odd[7]
            break
          
          continue
        else:
          
          #if win success
          if bet[1] == odd[8] and bet[2] == "win" and bet[3] in odd:
            #await ctx.send(f"```✅ {person}'s bet on {bet[1]} to {bet[2]} for {bet[0]}MB won!```")
            if odd[3] == odd[8]:
              calcOdd = odd[5]
                  
              
    
              
              break
            if odd[4] == odd[8]:
              calcOdd = odd[7]
              
                
              
              break
    
          #if draw success
          elif odd[8] == "draw" and bet[2] == "draw" and odd.count(bet[1]) == 1 and bet[3] in odd:
            calcOdd = odd[6]
            #await ctx.send(f"```✅ {person}'s bet on {bet[1]} to {bet[2]} for {bet[0]}MB won!```")
            
    
            break
    
          #if failed draw or win predict
          elif ((bet[1] != odd[8] and bet[1] in odd) or (bet[2] == "draw" and bet[2] != odd[8] and bet[1] in odd)) and bet[3] in odd:
            calcOdd = "Loss"
            if odd[4] == bet[1]:     
              recordOdd = odd[7].replace(",", "")
            elif odd[3] == bet[1]:
              recordOdd = odd[5].replace(",", "")
            elif bet[2] == "draw":
              recordOdd = odd[6].replace(",", "")
            #await ctx.send(f"```❌ {person}'s bet on {bet[1]} to {bet[2]} for {bet[0]}MB failed```")
            
            break
        
      if calcOdd != None:
        calc_data.append([bet[0], calcOdd, bet[1], bet[2], bet[3], recordOdd])
      elif calcOddP != None:
        potential_calc_data.append([bet[0], calcOddP, bet[1], bet[2], bet[3]])
        unknownResult = unknownResult + 1

    
    profit_results = []
    winCount = 0
    lossCount = 0
    for i in range(len(calc_data)):
      amt = float(calc_data[i][0])
      originalAmt = amt
      atStake = round(float(atStake) - amt, 2)
      if '+' in calc_data[i][1]:
        odd = calc_data[i][1].replace('+', '').replace(',', '')
        amt = (amt/100)*int(odd)
      elif '-' in calc_data[i][1]:
        odd = calc_data[i][1].replace('-', '').replace(',', '')
        amt = (amt/int(odd))*100
      elif calc_data[i][1] == 'Loss':
        amt = 0 - amt
        
      try:
        amt = round(amt, 2)
      except:
        await ctx.send("```⚠️ error in amount type while calculating profit results```")
        return
      
      #for record in bet_win_record:
      #  if amt > float(record[6]):
      #    await ctx.send(f"```🎉 {person}'s audacious {originalAmt}mb bet on {calc_data[i][2]} to {calc_data[i][3]} against {calc_data[i][4]} somehow won a {amt}mb profit\nnow it's rank {record[1].replace('.', '')} in the best profits of all time!```")
      #    bet_win_record[bet_win_record.index(record)] = ["W", record[1], person, calc_data[i][2], calc_data[i][3], calc_data[i][4], originalAmt, amt, calc_data[i][1]]

      #    record[1] = int(record[1].replace(".", ""))
      #    for i in range(5-record[1], len(bet_win_record)):
      #      old = bet_win_record[record[1]]
      #      bet_win_record[record[1]][1] = f'{str(int(int(bet_win_record[record[1]][1].replace(".", "")) + 1))}.'
      #      if int(bet_win_record[record[1]][1].replace(".", "")) > 5:
      #        bet_win_record.remove(old)
      #    break
                                                 
      #for record in bet_loss_record:
      #  if (0-originalAmt) < (0-float(record[6])):
      #    await ctx.send(f"```💀 {person} tried to bet {originalAmt}mb on {calc_data[i][2]} to {calc_data[i][3]} against {calc_data[i][4]}\nliterally rank {record[1].replace('.', '')} in the worst bets of all time```")
      #    bet_loss_record[bet_loss_record.index(record)] = ["L", record[1], person, calc_data[i][2], calc_data[i][3], calc_data[i][4], originalAmt, calc_data[i][5]]
      #    break

      #print(bet_win_record)
      #print(bet_loss_record)
      
  
      try:
        if amt >= 0:
          winCount = winCount +1
        elif amt < 0:
          lossCount = lossCount + 1
      except:
        await ctx.send("```⚠️ error in win and loss reporting```")
        
      profit_results.append(amt)
  
    #try:
    print_profit_results = ""
    for i in range(len(profit_results)):
        print_result = f'{profit_results[i]} on {calc_data[i][2]} to {calc_data[i][3]}\n'
        print_profit_results = print_profit_results + print_result
    #await ctx.send(f'```PROFIT PER BET: \n{print_profit_results}```')
    #except:
    #  await ctx.send("```⚠️ unknown error in new profit result format```")
    
    totalSum = 0
    for i in profit_results:
      totalSum = totalSum + i
    wallet = round(wallet + totalSum, 2)
  
    
    potential_profit_results = []
    for i in range(len(potential_calc_data)):
      amtP = float(potential_calc_data[i][0])
      if '+' in potential_calc_data[i][1]:
        oddP = potential_calc_data[i][1].replace('+', '').replace(',', '')
        amtP = (amtP/100)*int(oddP)
      elif '-' in potential_calc_data[i][1]:
        oddP = potential_calc_data[i][1].replace('-', '').replace(',', '')
        amtP = (amtP/int(oddP))*100
      else:
        await ctx.send("```wtf...```")
      try:
        amtP = round(amtP, 2)
      except:
        await ctx.send("```⚠️ error in amount type while calculating profit results```")
        return

      potential_profit_results.append(amtP)

    totalSumP = 0
    for i in potential_profit_results:
      totalSumP = round(totalSumP + i, 2)

    print_potential_profit_results = ""
    for i in range(len(potential_profit_results)):
        print_potential_result = f'{potential_profit_results[i]} on {potential_calc_data[i][2]} to {potential_calc_data[i][3]}\n'
        print_potential_profit_results = print_potential_profit_results + print_potential_result
    await ctx.send(f'```TOTAL POTENTIAL FOR UPCOMING BETS: {totalSumP}```')

    try:
      await ctx.send(f'```WINS: {winCount}\nLOSSES: {lossCount}\nNO RESULT YET: {unknownResult}\nREMAINING AT STAKE: {atStake}```')
    except:
      await ctx.send("```⚠️ win loss report fail```")
    
    
    if roundComplete == "yes":
      if totalSum < 0:
        await ctx.send(f'```🔻 NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
      elif totalSum > 0:
        await ctx.send(f'```💰 NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
      else:
        await ctx.send(f'```😑 NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
    else:
      if totalSum < 0:
        await ctx.send(f'```🔻 CURRENT NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
      elif totalSum > 0:
        await ctx.send(f'```💰 CURRENT NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
      else:
        await ctx.send(f'```😑 CURRENT NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
  
      
    
    #FINALLY woot woot 
    if roundComplete == "yes":       
      await ctx.send(f'```💸 CURRENT POTENTIAL WALLET FOR {person.upper()}: {wallet}```')
    else:
      await ctx.send(f'```💸 NEW WALLET FOR {person.upper()}: {wallet}```')

    bet_record = []
    for record in bet_win_record:
      for i in range(len(record)):
        record[i] = str(record[i])
      record = " ".join(record)
      bet_record.append(record)
    for record in bet_loss_record:
      for i in range(len(record)):
        record[i] = str(record[i])
      record = " ".join(record)
      bet_record.append(record)

    bet_record = "\n".join(bet_record)

    try:
      with open("Data/bet_record.txt", 'w') as fp:
        fp.write(bet_record)
    except:
      await ctx.send(":x: file error, please try again later")



async def globalCheckAllBets(self, ctx, person):
  person = person.lower()
  if (not person) or (person not in lookups):
    await ctx.send("you did not enter a player; which player would you like to check?")
    return
  betsData = await open_file("Data/bets.txt", ctx)
  atStake = [float(line.split()[2]) for line in betsData if line.split()[1] == person]
  atStake = str(round(sum(atStake), 2))
  if atStake == 0:
    await ctx.send(f"```{person.title()} has bet {atStake} so far in this round.```")
    return "fail"
  else:
    await ctx.send(f"```{person.title()} has bet {atStake} so far in this round.```")

    all_bets = []
    all_odds = []
    
    all_bets = await open_file("Data/bets.txt",  ctx)
    all_odds = await open_file("Data/odds.txt", ctx)
    
    person = person.lower()
  
    #finds wallet for person
    wallet = await statsCalculator(self, ctx, person, "wallet")
    
    #finds necessary bet data
    organized_bet_data = [[this_bet.split()[h] for h in range(2, 6)] for this_bet in all_bets if this_bet.split()[1] == person] 
  
    #cleans odds
    for i in range(len(all_odds)):
      try:
        all_odds[i] = all_odds[i].replace(".v.", " ").replace(":","").replace("]", "").replace("[", "").replace("(", "").replace(")", "").split()
      except:
        await ctx.send(f'❌ bracket reading error in match results')

    #finding necessary odds (non listcomp version):
    organized_odds_data = []
    for bet in organized_bet_data:
      for odd in all_odds:
        if bet[1] in odd and bet[3] in odd:
          organized_odds_data.append(odd)
      
    calc_data = []
    potential_calc_data = []
    roundComplete = "yes"
    unknownResult = 0
    
    for bet in organized_bet_data:
      calcOdd = None
      calcOddP = None
      
      for odd in organized_odds_data:
        if len(odd) < 9:
          roundComplete = "no"

          #if draw          
          if bet[2] == "draw" and bet[1] in odd and bet[3] in odd:
            calcOddP = odd[6]
            break

          #if win
          elif bet[1] == odd[3] and bet[2] == "win" and bet[3] in odd:
            calcOddP = odd[5]
            break
          elif bet[1] == odd[4] and bet[2] == "win" and bet[3] in odd:
            calcOddP = odd[7]
            break
          
          continue
        else:
          
          #if win success
          if bet[1] == odd[8] and bet[2] == "win" and bet[3] in odd:
            #await ctx.send(f"```✅ {person}'s bet on {bet[1]} to {bet[2]} for {bet[0]}MB won!```")
            if odd[3] == odd[8]:
              calcOdd = odd[5]
              
    
              
              break
            if odd[4] == odd[8]:
              calcOdd = odd[7]
              
    
              
              break
    
          #if draw success
          elif odd[8] == "draw" and bet[2] == "draw" and odd.count(bet[1]) == 1 and bet[3] in odd:
            calcOdd = odd[6]
            #await ctx.send(f"```✅ {person}'s bet on {bet[1]} to {bet[2]} for {bet[0]}MB won!```")
            
    
            break
    
          #if failed draw or win predict
          elif ((bet[1] != odd[8] and bet[1] in odd) or (bet[2] == "draw" and bet[2] != odd[8] and bet[1] in odd)) and bet[3] in odd:
            calcOdd = "Loss"
            #await ctx.send(f"```❌ {person}'s bet on {bet[1]} to {bet[2]} for {bet[0]}MB failed```")
            
            break
        
      if calcOdd != None:
        calc_data.append([bet[0], calcOdd, bet[1], bet[2]])
      elif calcOddP != None:
        potential_calc_data.append([bet[0], calcOddP, bet[1], bet[2]])
        unknownResult = unknownResult + 1

    
    profit_results = []
    winCount = 0
    lossCount = 0
    for i in range(len(calc_data)):
      amt = float(calc_data[i][0])
      atStake = round(float(atStake) - amt, 2)
      if '+' in calc_data[i][1]:
        odd = calc_data[i][1].replace('+', '').replace(',', '')
        amt = (amt/100)*int(odd)
      elif '-' in calc_data[i][1]:
        odd = calc_data[i][1].replace('-', '').replace(',', '')
        amt = (amt/int(odd))*100
      elif calc_data[i][1] == 'Loss':
        amt = 0 - amt
      try:
        amt = round(amt, 2)
      except:
        await ctx.send("```⚠️ error in amount type while calculating profit results```")
        return
      
  
      try:
        if amt >= 0:
          winCount = winCount +1
        elif amt < 0:
          lossCount = lossCount + 1
      except:
        await ctx.send("```⚠️ error in win and loss reporting```")
        
      profit_results.append(amt)
  
    #try:
    print_profit_results = ""
    for i in range(len(profit_results)):
        print_result = f'{profit_results[i]} on {calc_data[i][2]} to {calc_data[i][3]}\n'
        print_profit_results = print_profit_results + print_result
    if print_profit_results == "":
      print_profit_results = "N/A"
    await ctx.send(f'```PROFIT PER BET: \n{print_profit_results}```')
    #except:
    #  await ctx.send("```⚠️ unknown error in new profit result format```")
  
    totalSum = 0
    for i in profit_results:
      totalSum = totalSum + i
    wallet = round(wallet + totalSum, 2)
  
    
    potential_profit_results = []
    for i in range(len(potential_calc_data)):
      amtP = float(potential_calc_data[i][0])
      if '+' in potential_calc_data[i][1]:
        oddP = potential_calc_data[i][1].replace('+', '').replace(',', '')
        amtP = (amtP/100)*int(oddP)
      elif '-' in potential_calc_data[i][1]:
        oddP = potential_calc_data[i][1].replace('-', '').replace(',', '')
        amtP = (amtP/int(oddP))*100
      else:
        await ctx.send("```wtf...```")
      try:
        amtP = round(amtP, 2)
      except:
        await ctx.send("```⚠️ error in amount type while calculating profit results```")
        return

      potential_profit_results.append(amtP)

    totalSumP = 0
    for i in potential_profit_results:
      totalSumP = round(totalSumP + i, 2)

    print_potential_profit_results = ""
    for i in range(len(potential_profit_results)):
        print_potential_result = f'{potential_profit_results[i]} on {potential_calc_data[i][2]} to {potential_calc_data[i][3]}\n'
        print_potential_profit_results = print_potential_profit_results + print_potential_result
    if print_potential_profit_results == "":
      print_potential_profit_results = "N/A"
    await ctx.send(f'```POTENTIAL PROFIT PER UPCOMING BET: \n{print_potential_profit_results}\nTOTAL POTENTIAL: {totalSumP}```')

    try:
      await ctx.send(f'```WINS: {winCount}\nLOSSES: {lossCount}\nNO RESULT YET: {unknownResult}\nREMAINING AT STAKE: {atStake}```')
    except:
      await ctx.send("```⚠️ win loss report fail```")
    
    
    if roundComplete == "yes":
      if totalSum < 0:
        await ctx.send(f'```🔻 NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
      elif totalSum > 0:
        await ctx.send(f'```💰 NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
      else:
        await ctx.send(f'```😑 NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
    else:
      if totalSum < 0:
        await ctx.send(f'```🔻 CURRENT NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
      elif totalSum > 0:
        await ctx.send(f'```💰 CURRENT NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
      else:
        await ctx.send(f'```😑 CURRENT NET PROFIT FOR {person.upper()}: {round(totalSum, 2)}```')
  
      
    
    #FINALLY woot woot 
    if roundComplete == "yes":    
      await ctx.send(f'```💸 CURRENT POTENTIAL WALLET FOR {person.upper()}: {wallet}```')
    else:
      await ctx.send(f'```💸 NEW WALLET FOR {person.upper()}: {wallet}```')

async def globalCheckPotential(self, ctx, person):
  person = person.lower()
  if (not person) or (person not in lookups):
    await ctx.send("you did not enter a player; which player would you like to check?")
    return
  # pointless = 0
  # if pointless != 0:
  #   print('Whoops! This is pointless.')
  else:

    all_bets = []
    all_odds = []
    
    all_bets = await open_file("Data/bets.txt",  ctx)
    all_odds = await open_file("Data/odds.txt", ctx)
    
    person = person.lower()
    
    #finds necessary bet data
    organized_bet_data = [[this_bet.split()[h] for h in range(2, 6)] for this_bet in all_bets if this_bet.split()[1] == person] 
  
    #cleans odds
    for i in range(len(all_odds)):
      try:
        all_odds[i] = all_odds[i].replace(".v.", " ").replace(":","").replace("]", "").replace("[", "").replace("(", "").replace(")", "").split()
      except:
        await ctx.send(f'❌ bracket reading error in match results')
    
    #finding necessary odds (non listcomp version):
    organized_odds_data = []
    for bet in organized_bet_data:
      for odd in all_odds:
        if bet[1] in odd and bet[3] in odd:
          organized_odds_data.append(odd)
    potential_calc_data = []
    
    for bet in organized_bet_data:
      calcOddP = None
      
      for odd in organized_odds_data:
        if len(odd) < 9:

          #if draw          
          if bet[2] == "draw" and bet[1] in odd and bet[3] in odd:
            calcOddP = odd[6]
            break

          #if win
          elif bet[1] == odd[3] and bet[2] == "win" and bet[3] in odd:
            calcOddP = odd[5]
            break
          elif bet[1] == odd[4] and bet[2] == "win" and bet[3] in odd:
            calcOddP = odd[7]
            break
          
          continue
        else:
          
          continue
        
      if calcOddP != None:
        potential_calc_data.append([bet[0], calcOddP, bet[1], bet[2]])
  
    
    potential_profit_results = []
    for i in range(len(potential_calc_data)):
      amtP = float(potential_calc_data[i][0])
      if '+' in potential_calc_data[i][1]:
        oddP = potential_calc_data[i][1].replace('+', '').replace(',', '')
        amtP = (amtP/100)*int(oddP)
      elif '-' in potential_calc_data[i][1]:
        oddP = potential_calc_data[i][1].replace('-', '').replace(',', '')
        amtP = (amtP/int(oddP))*100
      else:
        await ctx.send("```wtf...```")
      try:
        amtP = round(amtP, 2)
      except:
        await ctx.send("```⚠️ error in amount type while calculating profit results```")
        return

      potential_profit_results.append(amtP)

    totalSumP = 0
    for i in potential_profit_results:
      totalSumP = round(totalSumP + i, 2)

    print_potential_profit_results = ""
    for i in range(len(potential_profit_results)):
        print_potential_result = f'{potential_profit_results[i]} on {potential_calc_data[i][2]} to {potential_calc_data[i][3]}\n'
        print_potential_profit_results = print_potential_profit_results + print_potential_result
    if print_potential_profit_results == "":
      print_potential_profit_results = "N/A"
    await ctx.send(f'```POTENTIAL PROFIT PER UPCOMING BET: \n{print_potential_profit_results}\nTOTAL POTENTIAL: {totalSumP}```')


async def remove10Global(self, ctx, person):
      """
      [person] removes 10mb from specified wallet
      """
      currentwallet = await statsCalculator(self, ctx, person, "wallet")
      currentwallet = currentwallet - 10
      
      await bankUpdate(self, ctx, 'wallet', person, currentwallet)
      await ctx.send(f"```10 MB subtracted from {person}```")

async def showBetGlobal(self, ctx, player, only_return):
    
    player = player.lower()
      
    try:
      with open('Data/bets.txt', 'r') as fp:
        bet_list = fp.read().splitlines()
    except:
      await ctx.send("❌ File error occured! Please try again later.")

    try:
      with open('Data/odds.txt', 'r') as fp:
        odd_list = fp.read().splitlines()
    except:
      await ctx.send("❌ File error occured! Please try again later.")

    for odd in odd_list:
      odd2 = odd
      odd = odd.split()
      odd_list[odd_list.index(odd2)] = odd

    #odd_list = await open_file('Data/odds.txt', 'r')
    
    async def betOddFound(bet, bet_list_new):
      if type(bet) == list:
        bet = " ".join(bet)
      bet_list_new.append(bet)
      return bet_list_new
    
    bet_list_new = []
    for bet in bet_list:
      #print(bet_list_new)
      matchOdd = ""
      for odd in odd_list:
        if bet.split()[3] in odd[4].replace(".", " ") and bet.split()[5] in odd[4].replace(".", " ") and len(odd) == 10:
          matchOdd = odd
      if matchOdd == "":
        bet_list_new = await betOddFound(bet, bet_list_new)
        continue

      bet = bet.split()
      #if bet won
      if bet[3] == matchOdd[9].replace("[", "").replace("]", "") and bet[4] == "win":
        bet.append("✅")
        bet_list_new = await betOddFound(bet, bet_list_new)
        continue
      elif bet[4] == "draw" and matchOdd[9].replace("[", "").replace("]", "") == "draw":
        bet.append("✅")
        bet_list_new = await betOddFound(bet, bet_list_new)
        continue
      #if bet lost
      elif matchOdd[9].replace("[", "").replace("]", "") == "postponed":
        bet.append("[postponed]")
        bet_list_new = await betOddFound(bet, bet_list_new)
      else:
        bet.append("❌")
        bet_list_new = await betOddFound(bet, bet_list_new)
        continue      
        

    printBet = [[]] # list of chunks
    
    for bet in bet_list_new: # for every bet in the data doc
      if len(printBet[-1]) > 30: # if the current chunk of printBet is too large, add another chunk
        printBet.append([])
      if player == "all" or player == "": # if there is no search term
        printBet[-1].append(bet) # add this line to the current chunk
      else:
        if str(player) in str(bet): # if the search term is in this line
          printBet[-1].append(bet) # add this line to the current chunk

    if only_return:
      return printBet
    
    for i, chunk in enumerate(printBet):
      embed = discord.Embed(
        title='Current Bets ' + str(i+1) + '/' + str(len(printBet)),
        description='\n'.join(chunk), 
        color=discord.Colour.green()
        )
      await ctx.send(embed=embed)

async def checkDate(ctx, date, entry, index1, index2):
      entry = entry.split()
      odds = await open_file('Data/odds.txt', ctx)
      
      betOdd = []
      for odd in odds:
        if entry[index1] in odd and entry[index2] in odd:
          betOdd = odd.split()
          
      if betOdd == []:
        await ctx.send("❌ entry a bet for a valid match")
        return False
      else:
        currentDateTime = datetime.now()
        matchDateTime = betOdd[1]+" "+betOdd[2]
        matchDateTime = datetime.strptime(matchDateTime, '%Y-%m-%d %H:%M:%S')
        print(currentDateTime)
        print(matchDateTime)
        if currentDateTime > matchDateTime:
          await ctx.send("❌ Sorry! It's too late to do that.")
          return False