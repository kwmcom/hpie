To define add(a, b):
    Return a + b

To define factorial(n):
    If n is less than 2 then:
        Return 1
    Otherwise:
        Set result to Call factorial(n - 1)
        Return n * result

Say "Testing function calls:"

Set x to Call add(5, 7)
Say "5 + 7 = " and x

Set y to Call factorial(5)
Say "factorial(5) = " and y

Say "Loop + function interaction test:"

Set i to 1
While i is less than 4:
    Set val to Call add(i, i)
    Say "double of " and i and " is " and val
    Increase i by 1

Say "Done."
