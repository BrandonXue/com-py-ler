# A wrapper class for file reading that keeps track of line and character position
class Reader:
    def __init__(self, filename, mode="r"):
        self.__file = open(filename, mode)
        self.__line = 1
        self.__char = 0

    # Close the file
    def close(self):
        self.__file.close()

    # Call the readline() of the file object
    # and change line and character position accordingly
    def readline(self, size=-1):
        curr_line = self.__file.readline(size)
        self.__line += 1
        self.__char += len(curr_line)
        return curr_line
    
    # Getter method for the line number of the file
    def line(self):
        return self.__line

    # Getter method for the character position  within the line
    def char(self):
        return self.__char

    # Call the tell() of the file object
    def tell(self):
        return self.__file.tell()

    # Read the specified characters
    # and change line and character position accordingly
    def read(self, chars=1):
        buffer = self.__file.read(chars)
        for char in buffer:
            if char == "\n":
                self.__char = 0
                self.__line += 1
            elif char == "\t":
                self.__char += 8
            else:
                self.__char += 1
        return buffer

    def seek(self, pos):
        # First keep track of current position
        curr_pos = self.__file.tell()

        # Now go to pos and read until current position
        num_chars = curr_pos - pos
        self.__file.seek(pos)
        buffer = self.__file.read(num_chars)

        # Find the number of lines and subtract
        lines = buffer.count("\n")
        self.__line -= lines

        # Go back one more line so we can find the position
        # of pos on that line
        temp_pos = pos - 1
        while temp_pos >= 0:
            self.__file.seek(temp_pos)
            char = self.__file.read(1)
            if char == "\n":
                break
            temp_pos -= 1
        temp_pos += 1
        # now temp_pos will hold the position of the newline prior to
        # our desired location, so we can calculate the char position
        self.__char = pos - temp_pos

        # Finally, seek back to the inputted pos
        self.__file.seek(pos)