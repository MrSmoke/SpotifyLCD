class Display:
    def __init__(self, columns, rows) -> None:
        self._rows = rows
        self._columns = columns
        self._is_on = False

    def on(self):
        if self._is_on:
            return

        # todo

        self._is_on = True
        return

    def off(self):
        if not self._is_on:
            return

        # todo

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

            print(line)

        # Temp: LCD end
        print("-"*self._columns)
