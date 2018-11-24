# mao-bot
An AI Framework that plays Mao. Lit.

## architecture and to-dos
* we need to make an infrastructure. The way I see it, we should do this in a primarily class based approach

### Files & Classes:
* infrastructure.py
	* Card
		* labelled "C", "H", "D" "S" for suit, & 2-14 for values.
	* Deck 
		* supports shuffling, resetting, and drawing
* Game Class
	* constraints -- specifies the rules of the game. each constraint is a rule
	* infrastructure class? (ie cards)
	* etc
* Constraint Class?
	* tbd
* Player Class

* Agent class (inherits from player?)
	* Computation and decision making on top of player class
