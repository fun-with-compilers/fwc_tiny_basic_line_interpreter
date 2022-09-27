REM load hangman picture
READ pic$, "hangman.pic"
REM hangman picture height is defined in the first line
pic_height = INT(pic$(0))
if (ALEN(pic$) - 1) MOD pic_height <> 0 THEN PRINT "Error: error in hangman.pic":END
REM max lives is the number of pictures in hangman.pic
max_lives = INT((ALEN(pic$)-1) / pic_height - 1)
lives = max_lives

REM load dictionary
READ words$, "hangman.txt"
num_words = alen(words$)
PRINT num_words, "words found in the dictionary"
REM pick a random word
word_index = RND(num_words)
word$ = words$(word_index)

REM disp is an array that displays the guessed part of the word
REM technically we could use just a string, but I wanted to use an array
letters = 0
DIM disp$(len(word$))
FOR i=0 TO len(word$)-1
  is_letter = "a" <= MID$(word$, i) AND MID$(word$, i) <= "z"
  if is_letter THEN GOSUB HANDLE_LETTER
  if not is_letter THEN GOSUB HANDLE_SPACE
NEXT

CLS
PRINT "--- THE GAME BEGINS.... ---"
GOTO ROUND_START

HANDLE_LETTER:
	disp$(i)="_"
	letters = letters + 1
	RETURN
	
HANDLE_SPACE:
    disp$(i)=MID$(word$, i)
	RETURN
	
HANGMAN:
	pic_start = 1 + (max_lives-lives)*pic_height
	for i = pic_start to pic_start + pic_height - 1
		print pic$(i)
	next i
	return

PRINT_TAB:
	GOSUB HANGMAN
	FOR i=0 TO alen(disp$)-1
		print disp$(i),
	NEXT
	PRINT " -- (LIVES LEFT: "; lives; ")"
	RETURN
	
FOUND_MATCH:
	disp$(i)=guess$
	letters = letters - 1
	found = 1
	RETURN
	
CHECK_GUESS:
	found = 0
	FOR i=0 TO len(word$)-1
		IF MID$(word$, i) = guess$ AND disp$(i) = "_" THEN GOSUB FOUND_MATCH
	NEXT
	RETURN

ERROR_WRONG:
	PRINT "HAHAHA! Wrong guess: "; guess$
	GOTO ERROR
ERROR_LEN:
	PRINT "GUESS MUST BE EXACTLY ONE LETTER!"
	GOTO ERROR
ERROR:
	lives = lives - 1
	PRINT "LIVES LEFT: ", lives
	if lives <= 0 THEN GOTO GAME_OVER
	RETURN
	
HINT:
	index = RND(letters)
	FIND_UNMATCHED:
		IF index < alen(disp$) AND disp$(index) <> "_" THEN index = index + 1 : GOTO FIND_UNMATCHED
	IF index >= alen(disp$) OR index >= len(word$) THEN RETURN
	guess$ = MID$(word$, index)
	GOSUB ERROR
	RETURN

ROUND_START:
	GOSUB PRINT_TAB
	INPUT "GUESS"; guess$ 
	
	CLS
	
	IF guess$ = "." THEN GOTO GIVE_UP
	IF guess$ = "?" THEN PRINT "YOU CHEATER!!!! WORD IS"; word$: GOTO ROUND_START
	IF guess$ = "" THEN GOSUB HINT
	IF LEN(guess$) <> 1 THEN GOSUB ERROR_LEN
	
	GOSUB CHECK_GUESS
	
	IF NOT found THEN GOSUB ERROR_WRONG
	IF found THEN PRINT "Good guess: ", guess$
	IF letters <= 0 THEN GOTO WIN
	
	GOTO ROUND_START
		
GIVE_UP:
	PRINT "GIVE UP?! HA-HA-HA"

GAME_OVER:
	CLS
	GOSUB HANGMAN
	PRINT ""
	PRINT "GAME OVER, YOU ARE SO DEAD!"
	PRINT "YOU COULDN'T GUESS"; word$;" :))))"
	END

WIN:
	CLS
	PRINT "CONGRATULATIONS!"
	PRINT "YOU HAVE WON!"
	PRINT "Successfully guessed:";word$
	END
	