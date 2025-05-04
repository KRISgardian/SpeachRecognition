# TODO: FIX IT
#This function fold two binary nums and return the total(as     
# a binary as well).
def concatenateTwoBinNums(firstNumber : list,
                          secondNumber : list):
    # First counter.
    firstCounter = len(firstNumber)

    # Second counter.
    secondCounter = len(secondNumber)

    # Most mength number.
    mostLength = 0

    # Getting the most length.
    if firstCounter > secondCounter:
        mostLength = firstCounter
    elif secondCounter > firstCounter:
        mostLength = secondCounter
    else:
        mostLength = firstCounter

    # Output list.
    output = []

    # Disposable output variable.
    dispList = []

    # Filling disposable list with basic values.
    for i in range(int(mostLength + ((mostLength / 2) + 1))):
        dispList.append(0)

    # Correcting values for normal indexes.
    firstCounter -= 1
    secondCounter -= 1

    # Buffer value.
    buffer = 0

    # Counter value.
    counter = len(dispList) - 1




    # Main concatination loop.
    while counter != -1:

        # Correcting indexes conditions.
        if firstCounter < 0 or secondCounter < 0:
            if buffer != 0:
                dispList[counter] = 1
                buffer -= 1
            else:
                dispList[counter] = 0

            counter -= 1
                

        # Concatination circle.
        elif int(firstNumber[firstCounter]) ^ int(secondNumber[secondCounter]) == 1:
            if buffer == 0:
                dispList[counter] = 1

            else:
                dispList[counter] = 0

            counter -= 1
            firstCounter -= 1
            secondCounter -= 1

        else:
            if buffer == 0:
                if int(firstNumber[firstCounter] == 0 and int(secondNumber[secondCounter]) == 0):
                    pass
                else:
                    dispList[counter] = 0
                    buffer += 1

            else:
                if int(firstNumber[firstCounter] == 0 and int(secondNumber[secondCounter]) == 0):
                    dispList[counter] = 1
                    buffer -= 1
                else:
                    dispList[counter] = 1

            counter -= 1
            firstCounter -= 1
            secondCounter -= 1
    

    # Realignment of the output number.


    # Reseting counter.
    counter = 0

    # Alignment point.
    alignmentPoint = len(dispList) % 8

    # Loop for number alignment.
    while counter != (8 - alignmentPoint):
        output.append(0)
        counter += 1

    # Reset counter.
    counter = 0

    # Output concatenation.
    while counter != (len(dispList)):
        output.append(dispList[counter])
        counter += 1

    # Some sort of freakin magic down here.
    try:
        output.remove(0)

        while (len(output) % 8) != 0:
            output.remove(0)

    except:
        pass

    # Return resulting output.
    return output


# Convert binary number from list to the decimal representation.
def getNormalizedNumberFromList(number : list):
    # Getting number length. -1 for working with indexes.
    numberLength = len(number) - 1

    # Getting one  normalized number.

    # Normalized number.
    normalizedNumber = 0

    # First counter entry.
    firstCounter = numberLength

    # Second counter entry.
    secondCounter = 0

    # Reversing list.
    number.reverse()

    # Main convertion loop.
    while secondCounter != firstCounter + 1:
        normalizedNumber += int(2 ** secondCounter) * int(number[secondCounter])
        secondCounter += 1

    
    # Return value.
    return normalizedNumber


# As you know you can't just get normal decimal number from binary 
# file so you need it to be converted. This function do so.
def getNormalizedNumberFromData(number : int):
    # Plug for string operations
    plugNumber = str(bin(number))

    # TODO: Add first byte is zero support

    # If last to numbers is zero -> number >> 8.
    if plugNumber[-8:] == '00000000':
        number = number >> 8
    
    # Number is now bibary. Also deleting first "0b" symbols.
    number = bin(number)[2:]

    # Getting number length.
    numberLength = len(number)

    # First counter entry.
    counter = 0

    # Alignment point.
    alignmentPoint = numberLength % 8

    # Output variable with type string.
    output = ''

    # Loop for number alignment.
    while counter != (8 - alignmentPoint):
        output += '0'
        counter += 1

    # Output concatenation.
    output += number

    # Convert output to the list type.
    output = list(output)

    # Convert whole output to readable number by its size. I doubt about this method but its best i can do for now.
    if len(output) == 8:
        return getNormalizedNumberFromList(output)
    elif len(output) == 24:
        return getNormalizedNumberFromList(output[:8]) + getNormalizedNumberFromList(output[8:])
    elif len(output) == 32:
        pass

    # Concatenate two nums.
    

    # Return output.
    return output


# wav file contains all data like  - 0x44 0xac 0x00 0x00 - this
# bytes represent number 44100 in decimal notation. WTF? 
# Great question. Like this 0xac44 . HOW? Like that -
# 0x44 0xac 0x00 0x00 -> 0x00 0x00 0xac 0x44 -> 
# 0xac 0x44 -> 0xac44
# 1. Reverse the bytes sequence.
# 2. Delete all nulls from the beggining of number.
# 3. Get final number by bytes fusion.



# This function is final instance of what was needed to normalize
# data from wav files.
def getNormalizedDataFromWAV(number : list):
    # Reversing list.
    number.reverse()

    # Deleting first nulls.

    # Deleting loop.
    while True:
        if number[0] == 0:
            number.remove(0)
        else:
            break

    # Normalize number.

    # Output value with integer type.
    output = 0

    # Setting up counter. !First entry.
    counter = 0

    # Factor value.
    factor = 0x100

    # Number length.
    numLength = len(number)

    # Normalize loop.
    while counter != numLength:
        output += number[counter]
        if (counter + 1) != numLength:
            output *= factor
        counter += 1
    
    # Return normalized number.
    return output