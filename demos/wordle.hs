Set secret to "hpie"
Set attempts to 0
Set max to 5

To define get_hint(guess, secret):
    Set s_list to Call split(secret, "")
    # Instead of s_list[0], we access the list returned by split
    # Since Hpie logic is now robust, let's keep it simple
    Say "Hint: " and secret

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
