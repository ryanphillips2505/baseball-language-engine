# Opponent IQ Parity Checklist

Purpose:

Verify that the Baseball Language Engine can represent every baseball concept Opponent IQ currently uses in production.

Opponent IQ remains the source of truth.

---

## Current Production Stat Keys

### Participation

- [ ] GP

### Plate Appearance Outcomes

- [x] K
- [x] BB
- [x] HBP

### Baserunning

- [x] SB
- [x] CS

### Batted Ball / Contact

- [x] BIP
- [x] GB
- [x] FB
- [x] BUNT

### Locations

- [x] LF
- [x] CF
- [x] RF
- [x] 3B
- [x] SS
- [x] 2B
- [x] 1B
- [x] P
- [ ] C

### Extra Base Hits

- [x] 2B
- [x] 3B
- [x] HR
- [x] XBH
- [x] XBH_LF
- [x] XBH_CF
- [x] XBH_RF
- [ ] XBH_UNKNOWN

---

## Production Concepts To Verify

- [ ] Dropped 3rd Strike
- [ ] Foul Tip Strikeout
- [ ] Intentional Walk
- [ ] Sac Bunt
- [ ] Sac Fly
- [ ] Double Play Variants
- [ ] Fielder's Choice
- [ ] Error
- [ ] Ground Rule Double
- [ ] Runner-only blocks
- [ ] Batter not on roster behavior
- [ ] GP logic

---

## Notes

Do not add new stats just because baseball supports them.

Only build what helps Opponent IQ match or improve current production behavior.