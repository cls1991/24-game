# 24-game
24 point game implemented in Python, just for fun!

![https://asciinema.org/a/i4aAC6Fp3cnRL1zMqLULz3ynV](https://asciinema.org/a/i4aAC6Fp3cnRL1zMqLULz3ynV.png)

## Quickstart

connect to game:

	$ nc 127.0.0.1 12345
	$ telnet 127.0.0.1 12345

start the game, give a random list consisted of four cards:

	$ start
	`8 10 2 5`

guess whether these four cards can make up 24 points or not, and submit your guess:

	$ submit yes
	$ submit y
	`submit no
	You're wrong, one of the solutions is `((13 + 1) + 7) + 3`.
	`

query your profile:

	$ info
	`
	Your connection is 127.0.0.1:59262, your score is 1.
	`
show the rank info:

	$ rank
	`
	Score ranks: 1 1 1.
	`

quit the game:

	$ quit
	$ CTRL+C

## Usage

	Play 24 point game.
  
	Commands:
	  start   Start the game.
	  submit  Commit your guess(yes/y for solutions, others for no solutions).
	  rank    Show the first three of score rank.
	  info    Show player info.
	  quit    Quit the game.
	  help    Show this message.

## Test

I have deployed one instance to the public internet, you can visit at `106.75.56.232:12345`.

   
## TODO

- A more beautiful ui.
- Add pk mode.
- Rank auto refresh.
