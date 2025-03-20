# Operator Precedence High Roller Package

This is a package for a discord bot. I call it High Roller as a play on its original use for TTRPG rolling, as well as a joking reference to gambling. Also recently I added a !gamble command to make the joke more literal.

How to run -
Enter the main directory in terminal.
python -m operator_precedence_high_roller.high_roller

Commands -

! is the general character to put before a discord message to be read by the bot.

Command => '!' [EXPR]

Command => '!gamble'

Command => [BET]

Command => '!' [RECALL]

EXPR => [EXPR] '+' [EXPR]

EXPR => [EXPR] '-' [EXPR]

EXPR => [EXPR] '\*' [EXPR]

EXPR => [EXPR] '/' [EXPR]

EXPR => '(' [EXPR] ')'

EXPR => [NUM]

EXPR => [ROLL]

ROLL => 'd' [NUM]

ROLL => 'e' [NUM]

ROLL => [NUM] 'd' [NUM]

ROLL => [NUM] 'e' [NUM]

NUM => [0..9]+

BET => 'odds'

BET => 'evens'

RECALL => 'h'

RECALL => 'h' '(' [NUM] ',' [ROLL] ')'

Version history -

1.1.2 - everything except RECALL commands works

1.1.3 - now everything works like it should

1.1.4 - small bug-fix

1.2.0 - big update, all unit tests done, general functional changes

1.2.1 - [

- XdYkhZ syntax added
- roll X dice, each of which has Y sides, and keep the highest Z of the results
- X and Z must not be equal
- Z must be greater than 0
- Z can be left blank in the command, in which case it will be set to 1

- disallow rolls with 0 dice

- disallow rolls of dice with 0 sides

- dice roll functions return None instead of (0,0) in the case of errors

- high_roller.py had to be moved to the outermost directory
- i'm not at all sure why, but before making the change, calls made from high_roller.py to functions from other files seemingly referenced old versions of them.
  ]
