from cleaners.gamechanger_cleaner import clean_gamechanger_text
from detectors.event_detector import detect_event_types
from translators.base_translator import detected_events_to_baseball_event

raw_text = """
Back to Schedule
Home
Support

DJ
david.k.jones1970@gmail.com

Get the App

Try our Family Plan
Thu Mar 5, 6:00 PM - 8:00 PM CT
Final
 
BRNC
YKNM
1	2	3	4	5
0	0	0	0	0
0	1	2	5	X
R	H	E
0	5	1
8	8	0
8
0
Bronchos
Yukon Millers Varsity logo
Yukon Millers Varsity logo live
Yukon Millers Varsity
Recap
Box Score
Plays
Videos
Info
Plays
All Plays
Scoring Plays
Outs

Player

Reverse Chronological
Bottom 5th - Yukon Millers Varsity
Eddie Fish at bat
Top 5th - Bronchos
Strikeout
3 Outs
Foul, Ball 1, Strike 2 looking, Ball 2, Ball 3, Strike 3 looking.
Cooper Willis strikes out looking, Wyatt Jones pitching.
Hit By Pitch
Lineup changed: Preston Klose in at pitcher, Strike 1 swinging, Ball 1, Ball 2, Ball 3, Ball 4.
Cooper Suarez is hit by pitch, Wyatt Jones pitching, Cruz Burleson advances to 3rd, Karter Thomas advances to 2nd.
Strikeout
2 Outs
Ball 1, Foul, Strike 2 swinging, Strike 3 swinging.
Brody McLaren strikes out swinging, Preston Klose pitching, Cruz Burleson remains at 2nd, Karter Thomas remains at 1st.
Single
Courtesy runner Cruz Burleson in for Ozzie Brown, Ball 1, Foul, Strike 2 looking, In play.
Karter Thomas singles on a hard ground ball to center fielder Wyatt Jones, Cruz Burleson advances to 2nd.
Single
Lineup changed: Ozzie Brown in for batter Cruz Burleson, Ball 1, Strike 1 swinging, In play.
Ozzie Brown singles on a ground ball to center fielder Wyatt Jones.
Ground Out
1 Out
Ball 1, Ball 2, In play.
Damyen Aguilar grounds out to second baseman Drake Pace.
Bottom 4th - Yukon Millers Varsity
Pop Out
3 Outs
In play.
Zayden Khalil pops out to right fielder Cruz Burleson.
Error
BRNC 0 - YKNM 8
Courtesy runner Wyatt Ruzicka in for Owen Blair, Ball 1, Strike 1 looking, In play.
Caleb Schneider hits a fly ball and reaches on an error by center fielder Cooper Suarez, Wyatt Ruzicka scores.
Double
BRNC 0 - YKNM 7
In play.
Owen Blair doubles on a fly ball to center fielder Cooper Suarez, Cade Geiger scores.
Ground Out
BRNC 0 - YKNM 6 | 2 Outs
Strike 1 looking, Cade Geiger steals 2nd, Strike 2 swinging, Foul, Ball 1, In play.
Brayden Trogdon grounds out to second baseman Brody McLaren, Caleb Cargal scores, Cade Geiger advances to 3rd.
Single
BRNC 0 - YKNM 5
In play.
Cade Geiger singles on a line drive to right fielder Cruz Burleson, Drake Pace scores, Caleb Cargal advances to 3rd, Eddie Fish scores.
Pop Out
1 Out
Courtesy runner Caleb Cargal in for Wyatt Jones, Ball 1, Strike 1 looking, In play.
Clayton Strange pops out to shortstop Karter Thomas, Eddie Fish remains at 3rd, Drake Pace remains at 2nd, Caleb Cargal remains at 1st.
Walk
Ball 1, Ball 2, Ball 3, Strike 1 looking, Foul, Ball 4.
Wyatt Jones walks, Jayden Rose pitching, Eddie Fish remains at 3rd, Drake Pace remains at 2nd.
Single
Ball 1, In play.
Drake Pace singles on a line drive to right fielder Cruz Burleson, Eddie Fish advances to 3rd on the throw, Drake Pace advances to 2nd on the throw.
Walk
Ball 1, Ball 2, Ball 3, Ball 4.
Eddie Fish walks, Jayden Rose pitching.
Top 4th - Bronchos
Pop Out
3 Outs
Strike 1 looking, Ball 1, Ball 2, Ball 3, In play.
Jayden Rose pops out to shortstop Eddie Fish.
Strikeout
2 Outs
Strike 1 looking, Foul, Strike 3 swinging.
Maximus Loyd strikes out swinging, Preston Klose pitching, Cooper Willis remains at 2nd.
Ground Out
1 Out
Foul, Ball 1, Foul, In play.
C Sydnes grounds out to pitcher Preston Klose, Cooper Willis advances to 2nd.
Single
Ball 1, Ball 2, In play.
Cooper Willis singles on a hard ground ball to left fielder Caleb Schneider.
Bottom 3rd - Yukon Millers Varsity
Strikeout
3 Outs
Ball 1, Foul, Foul, Strike 3 swinging.
Zayden Khalil strikes out swinging, Maximus Loyd pitching.
Single
Courtesy runner Wyatt Ruzicka in for Owen Blair, Strike 1 swinging, Ball 1, Ball 2, In play.
Caleb Schneider singles on a line drive to left fielder Brody Wright, Wyatt Ruzicka advances to 2nd.
Single
BRNC 0 - YKNM 3
Ball 1, Cade Geiger advances to 3rd on wild pitch, Brayden Trogdon advances to 2nd on the same pitch, Ball 2, Strike 1 looking, In play.
Owen Blair singles on a line drive to left fielder Brody Wright, Brayden Trogdon scores, Cade Geiger scores.
Walk
Ball 1, Ball 2, Ball 3, Cade Geiger steals 2nd, Strike 1 looking, Ball 4.
Brayden Trogdon walks, Maximus Loyd pitching, Cade Geiger remains at 2nd.
Single
In play.
Cade Geiger singles on a fly ball to center fielder Cooper Suarez.
Fly Out
2 Outs
Ball 1, Ball 2, In play.
Clayton Strange flies out to center fielder Cooper Suarez.
Pop Out
1 Out
Ball 1, Foul, Foul, Foul, In play.
Wyatt Jones pops out in foul territory to catcher.
Top 3rd - Bronchos
Strikeout
3 Outs
Strike 1 looking, Ball 1, Ball 2, Karter Thomas advances to 2nd on wild pitch, Strike 2 swinging, Strike 3 swinging.
Cooper Suarez strikes out swinging, Preston Klose pitching.
Pop Out
2 Outs
Ball 1, Strike 1 looking, Strike 2 looking, In play.
Brody McLaren pops out to second baseman Drake Pace, Karter Thomas remains at 1st.
Walk
Ball 1, Ball 2, Ball 3, Strike 1 looking, Ball 4.
Karter Thomas walks, Preston Klose pitching.
Strikeout
1 Out
Foul, Strike 2 swinging, Strike 3 swinging.
Cruz Burleson strikes out swinging, Preston Klose pitching.
Bottom 2nd - Yukon Millers Varsity
Pop Out
3 Outs
Ball 1, Ball 2, In play.
Drake Pace pops out to shortstop Karter Thomas.
Walk
Ball 1, Ball 2, Ball 3, Strike 1 looking, Foul, Ball 4.
Eddie Fish walks, Damyen Aguilar pitching, Caleb Schneider remains at 2nd.
Strikeout
2 Outs
Ball 1, Strike 1 looking, Foul, Ball 2, Ball 3, Strike 3 swinging.
Zayden Khalil strikes out swinging, Damyen Aguilar pitching, Caleb Schneider remains at 2nd.
Double
BRNC 0 - YKNM 1
Courtesy runner Wyatt Ruzicka in for Owen Blair, Ball 1, Wyatt Ruzicka advances to 2nd on passed ball, Ball 2, In play.
Caleb Schneider doubles on a line drive to center fielder Cooper Suarez, Wyatt Ruzicka scores.
Single
In play.
Owen Blair singles on a bunt to third baseman Jayden Rose.
Pop Out
1 Out
Strike 1 looking, In play.
Brayden Trogdon pops out to left fielder Brody Wright.
Top 2nd - Bronchos
Runner Out
3 Outs
Strike 1 swinging, Ball 1, Ball 2, Damyen Aguilar caught stealing 2nd, second baseman Drake Pace.
Half-inning ended by out on the base paths.
Single
In play.
Damyen Aguilar singles on a line drive to right fielder Cade Geiger.
Pop Out
2 Outs
In play.
Jayden Rose pops out to first baseman Brayden Trogdon.
Strikeout
1 Out
Ball 1, Strike 1 swinging, Strike 2 swinging, Ball 2, Strike 3 looking.
Maximus Loyd strikes out looking, Preston Klose pitching.
Bottom 1st - Yukon Millers Varsity
Pop Out
3 Outs
Ball 1, Foul, Foul, In play.
Cade Geiger pops out to shortstop Karter Thomas.
Walk
Ball 1, Ball 2, Ball 3, Ball 4.
Clayton Strange walks, C Sydnes pitching, Zayden Khalil remains at 3rd, Wyatt Jones advances to 2nd.
Walk
Ball 1, Ball 2, Ball 3, Ball 4.
Wyatt Jones walks, C Sydnes pitching, Zayden Khalil remains at 3rd.
Pop Out
2 Outs
Strike 1 looking, Ball 1, In play.
Drake Pace pops out in foul territory to catcher Maximus Loyd, Zayden Khalil remains at 3rd.
Ground Out
1 Out
Zayden Khalil steals 2nd, Strike 1 looking, Ball 1, Foul, Ball 2, In play.
Eddie Fish grounds out to shortstop Karter Thomas, Zayden Khalil advances to 3rd.
Hit By Pitch
Connor Sydnes in for pitcher C Sydnes, Strike 1 looking, Ball 1.
Zayden Khalil is hit by pitch, C Sydnes pitching.
Top 1st - Bronchos
Line Out
3 Outs
Strike 1 looking, Ball 1, Foul, Foul, Foul, Foul, In play.
Connor Sydnes lines out to left fielder Caleb Schneider.
Pop Out
2 Outs
Strike 1 looking, Ball 1, In play.
Cooper Willis pops out in foul territory, catcher Owen Blair to first baseman Brayden Trogdon, Karter Thomas remains at 2nd, Brody McLaren remains at 1st.
Strikeout
1 Out
Foul, Ball 1, Ball 2, Foul, Strike 3 swinging.
Cooper Suarez strikes out swinging, Preston Klose pitching, Karter Thomas remains at 2nd, Brody McLaren remains at 1st.
Walk
Strike 1 looking, Ball 1, Ball 2, Ball 3, Ball 4.
Brody McLaren walks, Preston Klose pitching, Karter Thomas remains at 2nd.
Double
Strike 1 looking, Foul, Ball 1, Foul, In play.
Karter Thomas doubles on a fly ball to left fielder Caleb Schneider.
Get the App
Status
Privacy
Terms
CA Disclosures
Your Privacy Choices
Dick's Sporting Goods logo
GameChanger is a proud member of the DICK'S Sporting Goods Family.
© GameChanger Media, Inc. All rights reserved. US Patent No. 8,731,458
"""

cleaned_lines = clean_gamechanger_text(raw_text)

valid = 0
invalid = []

for index, line in enumerate(cleaned_lines, start=1):
    detected = detect_event_types(line)
    baseball_event = detected_events_to_baseball_event(detected)

    if baseball_event:
        valid += 1
    else:
        invalid.append((index, line))

print(f"Cleaned lines: {len(cleaned_lines)}")
print(f"Valid BaseballEvents: {valid}")
print(f"Invalid cleaned lines: {len(invalid)}")

for index, line in invalid:
    print("=" * 70)
    print(f"Line #{index}")
    print(line)
