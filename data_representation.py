import csv

class DataTable:
    def __init__(self, csv_path: str):
        self.data = {}
        self.csv_path = csv_path

        with open(csv_path, newline = "") as f:
            reader = csv.reader(f)
            header = next(reader)
            for name in header:
                self.data[name] = []
            for row_num, row in enumerate(reader, start=2):
                if not row:
                    continue
                try:
                    converted = [float(v) for v in row]
                except ValueError:
                    print(f"Invalid data input in row {row_num}")
                    continue              
                for name, value in zip(header, converted):
                    self.data[name].append(value)


    def get(self, row_idx: int, col_name: str):
        column = self.get_column(col_name)
        return column[row_idx]

    def get_column(self, col_name: str) -> list:
        return self.data[col_name]

    def get_row(self, row_idx: int) -> dict:
        row = {}
        for name, values in self.data.items():
            row[name] = values[row_idx]
        return row

    def get_column_names(self) -> list:
        column_names = []
        for key in self.data:
            column_names.append(key)
        return column_names
        
    def get_num_rows(self) -> int:
        first_name = self.get_column_names()[0]
        rows = self.get_column(first_name)
        return len(rows)

    def get_column_average(self, col_name: str) -> float:
        col_values = self.get_column(col_name)
        return (sum(col_values) / len(col_values))

    def get_column_min(self, col_name: str) -> float:
        col_values = self.get_column(col_name)
        return min(col_values)

    def get_column_max(self, col_name: str) -> float:
        col_values = self.get_column(col_name)
        return max(col_values)
