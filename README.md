# **DnD5e Discord Bot**

Playing around with Discord Bots and API calls. 

## Currently Implemented
- *!roll* : Simple Dice Roller 
- *!spell* : Spell Lookup

**All commands bound to the '!' character*

### **Dice Roller** *!roll*
Roll dice and see the results!

Example:
```
!roll 2d6+4
```
```
2d6+4
Dice Rolls:        2,4
Result:             10
```


### **Spell Lookup** *!spell*
Look up 5e SRD spells using a simple bot command. 

Example:
```
!spell fire bolt
```

```
Fire Bolt | Evocation, cantrip
Casting Time: 1 action
Range: 120 feet
Components: V, S 
Duration: Instantaneous
You hurl a mote of fire at a creature or object within range. Make a ranged spell attack against the target. On a hit, the target takes 1d10 fire damage. A flammable object hit by this spell ignites if it isn't being worn or carried.This spell's damage increases by 1d10 when you reach 5th level (2d10), 11th level (3d10), and 17th level (4d10).
```
If you were to mistype, there is basic handling for similar spell names such that a command like so:
```
!spell firebolt
```
Would result in:
```
Did you mean one of the following: !spell fire bolt / !spell fireball?
```