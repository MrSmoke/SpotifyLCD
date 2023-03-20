from as_drivers.hd44780.alcd import LCD
from machine import Pin, PWM
import math

# 100 = Number of brightness steps
# 65535 = Max value of brightness
R = (100 * math.log10(2)) / math.log10(65535)

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
        self._backlightPWM = PWM(Pin(22, Pin.OUT))
        self._brightness = 50

    # Sets the display brightness
    def set_brightness(self, percent: float):
        # This is lifted from https://diarmuid.ie/blog/pwm-exponential-led-fading-on-arduino-or-other-platforms
        brightness = int(math.pow(2, percent / R))
        self._backlightPWM.duty_u16(brightness)

    # Turns on the display
    def on(self):
        if self._is_on:
            return

        # todo
        print("!!! Display on !!!")

        # Clear the screen to make sure nothing old is displayed
        self.clear();

        # Then set the display as on
        self.set_brightness(self._brightness)
        self._is_on = True
        return

    # Turns off the display
    def off(self):
        if not self._is_on:
            return

        # Clear the screen so thers nothing to display
        self.clear();

        # todo
        print("!!! Display off !!!")

        # Set the display as off
        self._backlightPWM.duty_u16(0)
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
