from as_drivers.hd44780.alcd import LCD

class Display:
    def __init__(self, columns: int, rows: int) -> None:
        if not isinstance(columns, int):
            raise Exception('Columns must be an integer')

        if not isinstance(rows, int):
            raise Exception('Rows must be an integer')

        self._rows = rows
        self._columns = columns
        self._is_on = False
        self._lcd = LCD((16, 17, 18, 19, 20, 21), columns, rows)

    # Turns on the display
    def on(self):
        if self._is_on:
            return

        # todo
        print("!!! Display on !!!")

        # Clear the screen first
        self.clear();

        # Then set the display as on
        self._is_on = True
        return

    # Turns off the display
    def off(self):
        if not self._is_on:
            return

        # todo
        print("!!! Display off !!!")

        self._is_on = False
        return

    # Clears the LCD
    def clear(self):
        self._lcd.lines = [""] * self._rows;

    # Prints passed lines. Will clear all other lines
    def print_lines(self, lines: list[str]):
        if not self._is_on:
            return

        # Temp: LCD start
        print("-"*self._columns)

        line_length = len(lines)

        for row in range(self._rows):
            line = ""

            # Check we have another line to write
            if row < line_length:
                line = lines[row];

            # Check that the line is not too line
            if len(line) > self._columns:
                line = line[:self._columns - 3].strip() + "..."

            # Write line
            self._lcd[row] = line
            print(line)

        # Temp: LCD end
        print("-"*self._columns)
