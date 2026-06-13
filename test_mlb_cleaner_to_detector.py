from cleaners.mlb_cleaner import clean_mlb_text
from detectors.event_detector import detect_event_types
from translators.base_translator import detected_events_to_baseball_event

raw_text = """
Top 1st
First Pitch
7:12 PM EDT
Fenway Park
Joc Pederson headshot
Single
Joc Pederson singles on a ground ball to left fielder Jarren Duran.
Josh Jung headshot
Single
Josh Jung singles on a sharp line drive to left fielder Jarren Duran. Joc Pederson to 3rd.
Brandon Nimmo headshot
Strikeout
Brandon Nimmo called out on strikes. 1 Out
Sonny Gray strikes out Brandon Nimmo
00:07
Wyatt Langford headshot
Single
Wyatt Langford singles on a ground ball to left fielder Jarren Duran. Joc Pederson scores. Josh Jung to 2nd.
TEX 1,BOS 0
Wyatt Langford's RBI single
00:12
Ezequiel Duran headshot
Strikeout
Ezequiel Duran strikes out swinging. 2 Outs
Evan Carter headshot
Strikeout
Evan Carter strikes out swinging. 3 Outs
Bottom 1st
Mickey Gasper headshot
Walk
Mickey Gasper walks.
Ceddanne Rafaela headshot
Forceout
Ceddanne Rafaela grounds into a force out, shortstop Ezequiel Duran to second baseman Nicky Lopez. Mickey Gasper out at 2nd. Ceddanne Rafaela to 1st. 1 Out

Challenging Team
ABS Challenge
Pitch 6: Overturned
Stolen Base 2B
Ceddanne Rafaela steals (7) 2nd base. Ceddanne Rafaela to 3rd. Ceddanne Rafaela advances to 3rd, on a throwing error by catcher Kyle Higashioka.
Wilyer Abreu headshot
Sac Fly
Wilyer Abreu out on a sacrifice fly to left fielder Wyatt Langford. Ceddanne Rafaela scores. 2 Outs
TEX 1,BOS 1
Wilyer Abreu's sacrifice fly scores Ceddanne Rafaela
00:21
Willson Contreras headshot
Home Run
Willson Contreras homers (14) on a fly ball to center field.
TEX 1,BOS 2
Willson Contreras' solo home run (14)
00:30
Jarren Duran headshot
Single
Jarren Duran singles on a line drive to first baseman Jake Burger.
Caleb Durbin headshot
Lineout
Caleb Durbin lines out to center fielder Evan Carter. 3 Outs
Top 2nd
Jake Burger headshot
Groundout
Jake Burger grounds out, third baseman Caleb Durbin to first baseman Willson Contreras. 1 Out
Kyle Higashioka headshot
Pop Out
Kyle Higashioka pops out to second baseman Isiah Kiner-Falefa. 2 Outs
Nicky Lopez headshot
Flyout
Nicky Lopez flies out to center fielder Ceddanne Rafaela. 3 Outs
Bottom 2nd
Isiah Kiner-Falefa headshot
Single
Isiah Kiner-Falefa singles on a soft line drive to first baseman Jake Burger.
Marcelo Mayer headshot
Groundout
Marcelo Mayer grounds out, pitcher Jack Leiter to first baseman Jake Burger. Isiah Kiner-Falefa to 2nd. 1 Out
Connor Wong headshot
Lineout
Connor Wong lines out to first baseman Jake Burger. 2 Outs
Mickey Gasper headshot
Flyout
Mickey Gasper flies out to center fielder Evan Carter. 3 Outs
Top 3rd
Joc Pederson headshot
Pop Out
Joc Pederson pops out to third baseman Caleb Durbin. 1 Out
Josh Jung headshot
Lineout
Josh Jung lines out to left fielder Jarren Duran. 2 Outs
Brandon Nimmo headshot
Strikeout
Brandon Nimmo strikes out swinging. 3 Outs
Bottom 3rd
Ceddanne Rafaela headshot
Double
Ceddanne Rafaela hits a ground-rule double (13) on a line drive to right field.
Wilyer Abreu headshot
Pop Out
Wilyer Abreu pops out to third baseman Josh Jung. 1 Out
Willson Contreras headshot
Strikeout
Willson Contreras strikes out swinging, catcher Kyle Higashioka to first baseman Jake Burger. Ceddanne Rafaela to 3rd. 2 Outs
Jarren Duran headshot
Strikeout
Jarren Duran strikes out swinging. 3 Outs
Jack Leiter strikes out Jarren Duran
00:08
Top 4th
Wyatt Langford headshot
Flyout
Wyatt Langford flies out to right fielder Wilyer Abreu. 1 Out
Ezequiel Duran headshot
Groundout
Ezequiel Duran grounds out, shortstop Marcelo Mayer to first baseman Willson Contreras. 2 Outs
Evan Carter headshot
Strikeout
Evan Carter strikes out swinging. 3 Outs
Bottom 4th
Caleb Durbin headshot
Pop Out
Caleb Durbin pops out to second baseman Nicky Lopez. 1 Out
Isiah Kiner-Falefa headshot
Flyout
Isiah Kiner-Falefa flies out to center fielder Evan Carter. 2 Outs
Evan Carter's INSANE diving catch
00:26
Marcelo Mayer headshot
Walk
Marcelo Mayer walks.
Connor Wong headshot
Strikeout
Connor Wong strikes out on a foul tip. 3 Outs
Top 5th
Jake Burger headshot
Strikeout
Jake Burger strikes out on a foul tip. 1 Out
Kyle Higashioka headshot
Groundout
Kyle Higashioka grounds out, third baseman Caleb Durbin to first baseman Willson Contreras. 2 Outs
Nicky Lopez headshot
Groundout
Nicky Lopez grounds out, first baseman Willson Contreras to pitcher Sonny Gray. 3 Outs
Bottom 5th
Defensive Switch
Defensive switch from left field to center field for Wyatt Langford.
Defensive Sub
Defensive Substitution: Justin Foscue replaces center fielder Evan Carter, batting 6th, playing second base.
Defensive Switch
Defensive switch from second base to left field for Nicky Lopez.
Mickey Gasper headshot
Double
Mickey Gasper doubles (4) on a fly ball to center fielder Wyatt Langford.
Ceddanne Rafaela headshot
Double
Ceddanne Rafaela doubles (14) on a sharp line drive to left fielder Nicky Lopez. Mickey Gasper scores.
TEX 1,BOS 3
Ceddanne Rafaela's RBI double
00:16
Wilyer Abreu headshot
Double
Wilyer Abreu doubles (14) on a fly ball to left fielder Nicky Lopez. Ceddanne Rafaela scores.
TEX 1,BOS 4
Wilyer Abreu's RBI double
00:33
Willson Contreras headshot
Single
Willson Contreras singles on a ground ball to third baseman Josh Jung. Wilyer Abreu scores. Willson Contreras to 2nd. Throwing error by third baseman Josh Jung.
TEX 1,BOS 5
Willson Contreras' single scores Wilyer Abreu
00:32
Game Advisory
Injury Delay.
Jarren Duran headshot
Groundout
Jarren Duran grounds out, second baseman Justin Foscue to first baseman Jake Burger. Willson Contreras to 3rd. 1 Out
Caleb Durbin headshot
Sac Fly
Caleb Durbin out on a sacrifice fly to center fielder Wyatt Langford. Willson Contreras scores. 2 Outs
TEX 1,BOS 6
Caleb Durbin's sacrifice fly scores Willson Contreras
00:17
Isiah Kiner-Falefa headshot
Lineout
Isiah Kiner-Falefa lines out to center fielder Wyatt Langford. 3 Outs
Top 6th
Joc Pederson headshot
Single
Joc Pederson singles on a ground ball to left fielder Jarren Duran.
Josh Jung headshot
Lineout
Josh Jung lines out to center fielder Ceddanne Rafaela. 1 Out
Brandon Nimmo headshot
Strikeout
Brandon Nimmo strikes out swinging. 2 Outs
Wyatt Langford headshot
Double
Wyatt Langford doubles (5) on a fly ball to left fielder Jarren Duran. Joc Pederson to 3rd.
Ezequiel Duran headshot
Groundout
Ezequiel Duran grounds out, shortstop Marcelo Mayer to first baseman Willson Contreras. 3 Outs
Ball 1 overturned after ABS Challenge
00:23
Bottom 6th
Pitching Substitution
Pitching Change: Cal Quantrill replaces Jack Leiter.
Marcelo Mayer headshot
Flyout
Marcelo Mayer flies out to right fielder Brandon Nimmo. 1 Out
Connor Wong headshot
Hit By Pitch
Connor Wong hit by pitch.
Mickey Gasper headshot
Pop Out
Mickey Gasper pops out softly to pitcher Cal Quantrill. 2 Outs
Ceddanne Rafaela headshot
Flyout
Ceddanne Rafaela flies out to right fielder Brandon Nimmo. 3 Outs
Top 7th
Pitching Substitution
Pitching Change: Tyron Guerrero replaces Sonny Gray.
Justin Foscue headshot
Flyout
Justin Foscue flies out to right fielder Wilyer Abreu. 1 Out
Jake Burger headshot
Groundout
Jake Burger grounds out, pitcher Tyron Guerrero to first baseman Willson Contreras. 2 Outs
Kyle Higashioka headshot
Groundout
Kyle Higashioka grounds out softly to first baseman Willson Contreras. 3 Outs
Bottom 7th
Wilyer Abreu headshot
Home Run
Wilyer Abreu homers (8) on a fly ball to center field.
TEX 1,BOS 7
Wilyer Abreu's solo home run (8)
00:33
Willson Contreras headshot
Hit By Pitch
Willson Contreras hit by pitch.
Jarren Duran headshot
Strikeout
Jarren Duran strikes out swinging. 1 Out
Caleb Durbin headshot
Lineout
Caleb Durbin lines out to center fielder Wyatt Langford. 2 Outs

Challenging Team
ABS Challenge
Pitch 1: Overturned
Isiah Kiner-Falefa headshot
Forceout
Isiah Kiner-Falefa grounds into a force out, fielded by second baseman Justin Foscue. Willson Contreras out at 2nd. 3 Outs
Top 8th
Pitching Substitution
Pitching Change: Danny Coulombe replaces Tyron Guerrero.
Nicky Lopez headshot
Single
Nicky Lopez singles on a line drive to left fielder Jarren Duran.
Offensive Substitution
Offensive Substitution: Pinch-hitter Elias Díaz replaces Joc Pederson.
Elias Díaz headshot
Groundout
Elias Díaz grounds out, pitcher Danny Coulombe to first baseman Willson Contreras. Nicky Lopez to 2nd. 1 Out
Josh Jung headshot
Lineout
Josh Jung lines out to center fielder Ceddanne Rafaela. 2 Outs
Brandon Nimmo headshot
Groundout
Brandon Nimmo grounds out to first baseman Willson Contreras. 3 Outs
Bottom 8th
Defensive Switch
Elias Díaz remains in the game as the designated hitter.
Defensive Sub
Defensive Substitution: Michael Helman replaces right fielder Brandon Nimmo, batting 3rd, playing center field.
Defensive Switch
Defensive switch from center field to left field for Wyatt Langford.
Defensive Switch
Defensive switch from left field to right field for Nicky Lopez.
Pitching Substitution
Pitching Change: Luis Curvelo replaces Cal Quantrill.
Marcelo Mayer headshot
Pop Out
Marcelo Mayer pops out to third baseman Josh Jung. 1 Out
Connor Wong headshot
Walk
Connor Wong walks.
Mickey Gasper headshot
Groundout
Mickey Gasper grounds out softly, pitcher Luis Curvelo to first baseman Jake Burger. Connor Wong to 2nd. 2 Outs
Ceddanne Rafaela headshot
Home Run
Ceddanne Rafaela homers (7) on a fly ball to left center field. Connor Wong scores.
TEX 1,BOS 9
Ceddanne Rafaela's two-run homer (7)
00:31
Wilyer Abreu headshot
Double
Wilyer Abreu doubles (15) on a line drive to center fielder Michael Helman.
Willson Contreras headshot
Double
Willson Contreras doubles (10) on a line drive to center fielder Michael Helman. Wilyer Abreu scores.
TEX 1,BOS 10
Willson Contreras' RBI double
00:22
Jarren Duran headshot
Flyout
Jarren Duran flies out sharply to center fielder Michael Helman. 3 Outs
Top 9th
Pitching Substitution
Pitching Change: Tommy Kahnle replaces Danny Coulombe.
Wyatt Langford headshot
Flyout
Wyatt Langford flies out sharply to center fielder Ceddanne Rafaela. 1 Out
Ezequiel Duran headshot
Strikeout
Ezequiel Duran strikes out swinging. 2 Outs
Justin Foscue headshot
Pop Out
Justin Foscue pops out to first baseman Willson Contreras. 3 Outs
"""

blocks = clean_mlb_text(raw_text)

print(f"Cleaned blocks: {len(blocks)}")

for index, block in enumerate(blocks, start=1):
    detected = detect_event_types(block)
    baseball_event = detected_events_to_baseball_event(detected)

    print("=" * 70)
    print(f"PA #{index}")
    print(block)
    print(detected)
    print(baseball_event)