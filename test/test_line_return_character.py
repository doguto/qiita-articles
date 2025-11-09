for i in range(10):
    print(i, end='\r')  # Carriage return to overwrite the line

print()
print("Done!")  # Final output after the loop

for i in range(10):
    print(i, end='\n')  # New line after each number

print("Done!")  # Final output after the loop

for i in range(10):
    print(i, end='\r\n')  # CRLF line ending, each number on a new line

print("Done!")  # Final output after the loop
