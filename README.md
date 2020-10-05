# **DnD5e SRD Discord Bot**

Playing around with Discord Bots and API calls. 

## Currently Implemented
- *!roll* : Simple Dice Roller 
- *!spell* : Spell Lookup
- *!spellcasting* : Class Spell Lists

**All commands bound to the '!' character*

### **Dice Roller** *!roll*
Roll dice and see the results! The syntax used is the same in the SRD and when talking about rolling dice in the 5e system.

Thus the syntax is pretty specific but it allows for quickly rolling a large number of dice. All *!roll* commands must contain the 'd' character to delineate the difference between the number of dice and the number of sides on the dice. An optional '+####' can be appended to the end of the command to add the to the sum of the dice rolls. 

Examples:
`!roll 2d6+4` or `!roll 2d6`

**Quick Breakdown of the command:**

Number of dice: 2

Number of Sides: 6 

Optional Modifier: 4*

**This is added to the sum of the rolled dice*


```
2d6+4
Dice Rolls:        2,4
Result:             10
```


### **Spell Lookup** *!spell*
Look up 5e SRD spells using a simple bot command. 

Example: `!spell fire bolt`

```
Fire Bolt | Evocation, cantrip
Casting Time: 1 action
Range: 120 feet
Components: V, S 
Duration: Instantaneous
You hurl a mote of fire at a creature or object within range. 
Make a ranged spell attack against the target. 
On a hit, the target takes 1d10 fire damage. 
A flammable object hit by this spell ignites if it isn't being worn or carried.
This spell's damage increases by 1d10 when you reach 5th level (2d10), 11th level (3d10), and 17th level (4d10).
```
If you were to mistype, there is basic handling for similar spell names.

Example: `!spell firebolt`

Would result in:
```
Did you mean one of the following: !spell fire bolt / !spell fireball?
```



### **Class Spell Lists** *!spellcasting*
Sends a DM to the user of all available spells, sorted by level, for the requested class. This way there is no unecessary clutter in the main channel and the user can continue to make requets to the bot in the DM if necessary (ie. a followup !spell command). 

Example: `!spellcasting cleric`

Returns:
```
106 Cleric Spells Found.
Sending full list as a DM to avoid clutter, thanks for understanding!
 ```
In the same context as the command was sent. And then sends the rest of the information directly to the user's DMs, like so:
```
Cleric
Spellcasting Ability: WIS
Spells:
To learn more about a specific spell, use the command !spell.
ex. !spell Spare the Dying
Level 0: Guidance / Light / Mending / Resistance / Sacred Flame / Spare the Dying / Thaumaturgy
Level 1: Bane / Bless / Command / Create or Destroy Water / Cure Wounds / Detect Evil and Good / Detect Magic / Detect Poison and Disease / Guiding Bolt / Healing Word / Inflict Wounds / Protection from Evil and Good / Purify Food and Drink / Sanctuary / Shield of Faith
Level 2: Augury / Blindness/Deafness / Calm Emotions / Continual Flame / Enhance Ability / Find Traps / Gentle Repose / Hold Person / Lesser Restoration / Locate Object / Prayer of Healing / Protection from Poison / Silence / Spiritual Weapon / Warding Bond / Zone of Truth
Level 3: Beacon of Hope / Bestow Curse / Clairvoyance / Create Food and Water / Daylight / Dispel Magic / Glyph of Warding / Magic Circle / Mass Healing Word / Meld into Stone / Protection from Energy / Remove Curse / Revivify / Sending / Speak with Dead / Spirit Guardians / Tongues / Water Walk
Level 4: Banishment / Control Water / Death Ward / Freedom of Movement / Guardian of Faith / Locate Creature / Stone Shape
Level 5: Contagion / Dispel Evil and Good / Flame Strike / Geas / Greater Restoration / Hallow / Insect Plague / Legend Lore / Mass Cure Wounds / Planar Binding / Raise Dead / Scrying
Level 6: Create Undead / Find the Path / Forbiddance / Harm / Heal / Heroes' Feast / Planar Ally / True Seeing / Word of Recall
Level 7: Divine Word / Etherealness / Fire Storm / Plane Shift / Regenerate / Resurrection / Symbol
Level 8: Control Weather / Earthquake / Holy Aura
Level 9: Gate / Mass Heal / True Resurrection
```
A random spell from the list is picked and added as an example *!spell* command to prompt the user to get more information if necessary. 