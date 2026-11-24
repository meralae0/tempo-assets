import random, csv
random.seed(12)
rows=[]
def add(d,l,a): rows.append((f"2026-10-{d:02d}",l,a))
add(1,"VIREMENT SALAIRE OCTOBRE",2450.00)
add(2,"PRLV LOYER APPARTEMENT",-780.00)
add(3,"PRLV ELECTRICITE",-64.20)
add(5,"PRLV FORFAIT MOBILE",-12.99)
add(5,"PRLV BOX INTERNET",-29.99)
add(8,"PRLV ASSURANCE HABITATION",-18.40)
add(10,"PRLV ABONNEMENT STREAMING",-13.49)
add(10,"PRLV ABONNEMENT MUSIQUE",-10.99)
add(15,"PRLV SALLE DE SPORT",-34.90)
add(27,"VIR EPARGNE LIVRET",-200.00)
add(18,"REMBOURSEMENT MUTUELLE",42.30)
shops=[("CB SUPERMARCHE DU CENTRE",(35,95),"Courses"),("CB EPICERIE DU COIN",(6,22),"Courses"),("CB BOULANGERIE",(3,9),"Courses"),
("CB STATION ESSENCE",(45,70),"Transport"),("CB TICKET BUS",(1.8,1.8),"Transport"),
("CB RESTAURANT",(18,48),"Sorties"),("CB CAFE",(2.5,7),"Sorties"),("CB CINEMA",(9.5,12),"Sorties"),
("CB PHARMACIE",(6,28),"Santé"),("CB VETEMENTS",(25,60),"Shopping"),("CB LIVRES",(12,25),"Shopping")]
cnt={"CB SUPERMARCHE DU CENTRE":5,"CB EPICERIE DU COIN":4,"CB BOULANGERIE":6,"CB STATION ESSENCE":3,"CB TICKET BUS":4,"CB RESTAURANT":4,"CB CAFE":5,"CB CINEMA":2,"CB PHARMACIE":2,"CB VETEMENTS":1,"CB LIVRES":1}
for name,(lo,hi),cat in shops:
  for i in range(cnt[name]):
    add(random.randint(1,31),name,-round(random.uniform(lo,hi),2))
add(22,"RETRAIT DAB",-60.00)
rows.sort()
with open("releve-octobre.csv","w",newline="") as f:
  w=csv.writer(f,delimiter=";"); w.writerow(["date","libelle","montant"])
  for r in rows: w.writerow([r[0],r[1],f"{r[2]:.2f}".replace(".",",")])
print(len(rows))
