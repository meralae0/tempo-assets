import random, csv, json
random.seed(1313)
rows=[]
def add(d,l,a,cat): rows.append([f"2026-10-{d:02d}",l,round(a,2),cat])
add(1,"PAYROLL DEPOSIT ACME LOGISTICS",3120.00,"Income")
add(15,"PAYROLL DEPOSIT ACME LOGISTICS",3120.00,"Income")
add(1,"ONLINE PMT RENT - MAPLE COURT APTS",-1450.00,"Housing")
add(4,"AUTOPAY CITY POWER & LIGHT",-88.37,"Utilities")
add(6,"AUTOPAY NETWAVE INTERNET",-59.99,"Utilities")
add(7,"AUTOPAY BRIGHTCELL WIRELESS",-45.00,"Utilities")
add(9,"AUTOPAY HOMESHIELD RENTERS INS",-16.75,"Insurance")
add(11,"RECURRING STREAMFLIX MONTHLY",-17.99,"Subscriptions")   # price went up from 15.49
add(12,"RECURRING TUNEBOX PREMIUM",-11.99,"Subscriptions")
add(14,"RECURRING CLOUDVAULT 2TB",-9.99,"Subscriptions")
add(19,"RECURRING IRONHOUSE GYM",-39.00,"Subscriptions")
add(23,"RECURRING NEWSDESK DIGITAL",-6.99,"Subscriptions")
add(28,"TRANSFER TO SAVINGS",-400.00,"Savings")
add(20,"REFUND FRESHMART #212",23.48,"Groceries")
shops=[("POS FRESHMART #212",(38,140),"Groceries",7),("POS CORNER MARKET",(6,24),"Groceries",5),("POS GREEN BASKET FARM STAND",(9,30),"Groceries",2),
("POS QUICKFUEL STATION",(38,62),"Transport",4),("METRO TRANSIT FARE",(2.75,2.75),"Transport",6),("RIDESHARE TRIP",(9,26),"Transport",3),
("POS LUNA TRATTORIA",(28,74),"Dining",3),("POS DAILY GRIND CAFE",(3.5,7.8),"Dining",8),("FOOD DELIVERY ORDER",(19,41),"Dining",4),
("POS WELLCARE PHARMACY",(7,32),"Health",2),("ONLINE ORDER MEGAMART",(14,89),"Shopping",4),("POS THREADLINE APPAREL",(29,75),"Shopping",1)]
for name,(lo,hi),cat,n in shops:
  for i in range(n): add(random.randint(2,31),name,-random.uniform(lo,hi),cat)
add(22,"ATM WITHDRAWAL",-80.00,"Cash")
# duplicate charge: same merchant, same day, same amount
add(17,"POS LUNA TRATTORIA",-56.40,"Dining"); add(17,"POS LUNA TRATTORIA",-56.40,"Dining")
# foreign charge + fee
add(25,"INTL POS HOTEL ALMERIA EUR 92.00",-99.82,"Travel"); add(25,"FOREIGN TRANSACTION FEE",-2.99,"Fees")
rows.sort(key=lambda r:(r[0],r[1]))
with open("statement-october.csv","w",newline="") as f:
  w=csv.writer(f); w.writerow(["Date","Description","Amount"])
  for r in rows: w.writerow([r[0],r[1],f"{r[2]:.2f}"])
tot={}
for r in rows: tot[r[3]]=round(tot.get(r[3],0)+r[2],2)
spent=round(sum(r[2] for r in rows if r[2]<0 and r[3]!="Savings"),2)
groc_gross=round(sum(r[2] for r in rows if r[3]=="Groceries" and r[2]<0),2)
truth={"n":len(rows),"by_cat":tot,"groceries_net":tot["Groceries"],"groceries_gross":groc_gross,"spent_excl_savings":spent,
 "subs_monthly":round(-tot["Subscriptions"],2),"subs_yearly":round(-tot["Subscriptions"]*12,2),"duplicate":"2026-10-17 LUNA TRATTORIA 56.40"}
json.dump(truth,open("truth.json","w"),indent=1); print(json.dumps(truth,indent=1))
