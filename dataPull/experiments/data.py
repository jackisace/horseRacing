st = """,1 (12)10.Skysail9/2Dougie CostelloMarcus TregoningDougie CostelloMarcus Tregoning297–66––
,2 (9)½4.Dark Trooper(IRE)12/1David EganEd WalkerDavid EganEd Walker297–64––
,3 (1)1¼[1¾]1.Acai(IRE)10/1Adam KirbyClive CoxAdam KirbyClive Cox297–59––
,4 (3)nse[1¾]13.Vecchio(IRE)9/1Rob HornbyFreddie & Martyn MeadeRob HornbyFreddie & Martyn Meade297–58––
,5 (5)¾[2½]9.Paspaley11/5FTom MarquandWilliam HaggasTom MarquandWilliam Haggas297–55––
,6 (2)½[3]2.Be Frank50/1Dane O'NeillHenry CandyDane O'NeillHenry Candy297–53––
,7 (4)hd[3¼]6.Fast Trek(IRE)33/1David ProbertAndrew BaldingDavid ProbertAndrew Balding297–52––
,8 (6)½[3¾]15.Giddy Aunt66/1Charles BishopJonathan PortmanCharles BishopJonathan Portman292–45––
,9 (7)½[4¼]3.Calypso(IRE)18/1Daniel MuscuttJames FergusonDaniel MuscuttJames Ferguson297–48––
,10 (16)¾[5]8.Muy Muy Guapo50/1Callum ShepherdJim BoyleCallum ShepherdJim Boyle297–45––
,11 (11)2¼[7¼]14.What A Whopper(IRE)13/2Hollie DoyleBrian MeehanHollie DoyleBrian Meehan297–36––
,12 (13)4[11¼]11.Stamford Blue(IRE)22/1Pat DobbsRichard HannonPat DobbsRichard Hannon297–20––
,13 (10)hd[11½]16.Por Ti Volare300/1Josephine GordonBrian BarrJosephine GordonBrian Barr292–14––
,14 (14)6[17½]5.Dropskipandump(IRE)125/1Shane KellyPeter CrateShane KellyPeter Crate297––––
,15 (15)1¾[19¼]12.Trilby5/1Ryan MooreGeorge BougheyRyan MooreGeorge Boughey297––––"""

for line in st.split("\n"):
    horseNum = line.split(" ")[0]
    line = line.replace(horseNum, "")
    horseNum = horseNum[1:]
    print(line)    
    
    print(horseNum)