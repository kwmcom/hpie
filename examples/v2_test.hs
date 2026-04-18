Set result to (1 + 2) * 3
Say "(1 + 2) * 3 is " and result

Set complex to 10 + 5 * 2 - (4 / 2)
Say "10 + 5 * 2 - (4 / 2) should be 18: " and complex

Set count to 1
While count is less than 3:
    Say "Outer loop: " and count
    Set inner to 1
    While inner is less than 3:
        Say "  Inner loop: " and inner
        Set inner to inner + 1
    Set count to count + 1

If result is greater than 5 then:
    Say "Math and logic are working!"
Otherwise:
    Say "Math failed"
