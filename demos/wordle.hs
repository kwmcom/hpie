Set secret to "hpie"
Set attempts to 0
Set max to 5

To define get_hint(guess, secret):
    Set g_len to Call length(guess)
    If g_len is 4 then:
        Set s_list to Call split(secret, "")
        Set g_list to Call split(guess, "")
        Set hint to ""
        Set i to 0
        While i is less than 4:
            Set g_char to Call get_item(g_list, i)
            Set s_char to Call get_item(s_list, i)
            
            If g_char is s_char then:
                Set hint to hint and g_char
            Otherwise:
                # Check for yellow (misplaced)
                If Call contains(s_list, g_char) is 1.0 then:
                    Set hint to hint and "?"
                Otherwise:
                    Set hint to hint and "_"
            Increase i by 1
        Say "Hint: " and hint
    Otherwise:
        Say "Hint: Word must be 4 letters."

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
