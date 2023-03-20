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

    def on(self):
        if self._is_on:
            return

        # todo
        print("!!! Display on !!!")

        self._is_on = True
        return

    def off(self):
        if not self._is_on:
            return

        # todo
        print("!!! Display off !!!")

        self._is_on = False
        return

    def print_lines(self, lines: list[str]):
        if not self._is_on:
            return

        # Temp: LCD start
        print("-"*self._columns)

        line_count = 0
        for line in lines:

            if line_count == self._rows:
                break

            line_count += 1

            if len(line) > self._columns:
                line = line[:self._columns - 3].strip() + "..."

            self._lcd[line_count-1] = line
            print(line)

        # Temp: LCD end
        print("-"*self._columns)
