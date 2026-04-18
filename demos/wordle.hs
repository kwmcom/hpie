Set secret to "hpie"
Set attempts to 0
Set max to 5

To define get_hint(guess, secret):
    Set s_list to Call split(secret, "")
    Set hint to ""
    
    # Logic: Show first letter if guessed correctly, else _
    # (Simplified for the first letter as requested h___)
    Set hint to s_list[0] and "___"
    Say "Hint: " and hint

Say "Welcome to Wordle-lite!"

While attempts is less than max:
    Say "Guess a 4-letter word:"
    Ask for guess
    
    If guess is secret then:
        Say "Correct! You win!"
        Set attempts to max
    Otherwise:
        Call get_hint(guess, secret)
        Increase attempts by 1
        Set remaining to max - attempts
        Say "Incorrect. Attempts remaining: " and remaining

If attempts is max then:
    Say "Game Over. The word was hpie"
