# EN4 : rapport fictif de 24 pages (port inventé) avec 5 faits cachés + 1 piège (réponse absente)
import random
random.seed(17)
topics=['berth scheduling','cargo handling','ferry operations','staff training','maintenance','safety drills','customer service','IT systems','energy use','tenant relations','security patrols','waste management','road access','rail sidings','winter readiness','community events','procurement','water quality','lighting upgrades','signage','parking','cold storage','pilot boats','tug fleet']
verbs=['improved','was reviewed','remained stable','was expanded','was simplified','received new guidance','was audited','was reorganised']
s1=["During the year, {t} {v} across all three terminals.","The team responsible for {t} met every month to track progress.","Feedback from tenants on {t} was mostly positive, with a few requests for clearer timetables.","A short internal review of {t} found no major issues but listed several small improvements.","Work on {t} continued as planned, with most milestones reached on time.","Managers noted that {t} depends heavily on good communication between shifts.","In the second half of the year, {t} {v} after a series of workshops with staff.","The board asked for a simpler monthly summary of {t}, which is now shared by email.","Seasonal demand affected {t}, especially during the summer holiday weeks.","New checklists for {t} were introduced and staff were trained on them in small groups.","Visitors often commented on {t}, and their comments were logged for the next review.","The Authority expects {t} to stay a priority for the coming two years.","Several suppliers were invited to present ideas for {t}, though no contract was signed yet.","A pilot project on {t} ran for six weeks at the East Quay and will be evaluated next spring.","Staff surveys showed that most employees understood the new rules for {t}."]
needles={4:"Total passengers carried by the ferry service in the first quarter were 41,250.",
 7:"Ferry passengers in the second quarter reached 58,900, helped by an early start to the tourist season.",
 9:"Fuel for the ferry fleet in the third quarter cost 96,330 euros, for 71,400 passengers carried in that quarter.",
 12:"Note 14: any dredging contract above 2 million euros must be approved by the Harbour Finance Committee, not by the Director alone.",
 15:"Ferry passengers in the fourth quarter fell to 36,850 because of the December storms.",
 18:"The North Crane, in service since 1994, will be retired on 30 June 2027 and replaced by a mobile unit.",
 3:"The Authority currently operates 412 berths across its three terminals.",
 23:"Errata: the berth count given on page 3 is out of date. After the West Basin works, the correct number is 408 berths."}
out=["NORTHWIND HARBOUR AUTHORITY — ANNUAL OPERATIONS REPORT 2025","(fictional organisation, test document)",""]
for p in range(1,25):
    out.append(f"--- Page {p} ---")
    out.append(f"{p}. {topics[p-1].capitalize()}")
    paras=[]
    for k in range(4):
        sents=[random.choice(s1).format(t=random.choice(topics),v=random.choice(verbs)) for _ in range(random.randint(4,6))]
        paras.append(' '.join(sents))
    if p in needles:
        k=random.randint(1,3); paras[k]=paras[k]+' '+needles[p]+' '+random.choice(s1).format(t=topics[p-1],v=random.choice(verbs))
    out+=paras; out.append("")
txt='\n'.join(out); open('report.txt','w').write(txt)
print(len(txt.split()),'words',len(txt),'chars')
