
Say "Welcome to Hangman!"
Set secret to "hpie"
Set guess_count to 0
Set max_guesses to 5

To define check_guess(guess, secret):
    If guess is secret then:
        Return 1
    Otherwise:
        Return 0

While guess_count is less than max_guesses:
    Say "Guess the word (4 letters):"
    Ask for user_guess
    
    Set is_correct to Call check_guess(user_guess, secret)
    
    If is_correct is 1 then:
        Say "You win! The word was hpie"
        Set guess_count to 10
    Otherwise:
        Increase guess_count by 1
        Set remaining to max_guesses - guess_count
        Say "Wrong! Guesses remaining: " and remaining

If guess_count is 5 then:
    Say "Game Over. The word was hpie"
