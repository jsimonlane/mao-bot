# mao-bot
An AI Framework that plays Mao. Lit.

## architecture and to-dos
* We need to make an infrastructure. The way I see it, we should do this in a primarily class based approach

### Files & Classes:
* infrastructure.py
	* Card
		* labelled "C", "H", "D" "S" for suit, & 2-14 for values.
	* Deck 
		* supports shuffling, resetting, and drawing
	* Player
		* basic methods for interacting with a deck. need to modify so that it interacts with the game
	
* game.py
	* Game
		* constraints -- specifies the rules of the game. each constraint is a rule
		* deck
		* players
		* order
	* Constraint class
		* constraints are passed into the game to keep track of rules
		* 
	* tbd

* ai.py
	* Agent class (inherits from player?)
		* Computation and decision making on top of player class
		
*Rules
	*Base Rules
		* Wild Cards: maximum of one card at any given time. (Value)
		* Trump Suit: Can Be played at any time (suit)
		* Lower Value: Can only play cards of lower value, not higher
		* Different Suit: Can only play cards of different value, not same
	*Reach Rules
		* Skip Rules: Skipping every x players
		* Face Cards: cards have effects
		* Individiual cards have effects
		* Talking: Choose from a couple of statements every time x card
