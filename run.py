def compress_message(message):
    if not message:
        return ""

    output = ""
    count = 1

    for i in range(1, len(message)):
        if message[i] == message[i - 1]:
            count += 1
        else:
            output += message[i - 1]
            if count > 1:
                output += str(count)
            count = 1

    # נוסיף את התו האחרון והרצה שלו
    output += message[-1]
    if count > 1:
        output += str(count)

    return output

print(compress_message("aaabbc"))  # a3b2c
print(compress_message("abc"))     # abc
print(compress_message("aabbcc"))  # a2b2c2
