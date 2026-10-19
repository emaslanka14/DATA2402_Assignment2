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
            for row in reader:
                if not row:
                    continue             
                for name, value in zip(header, row):
                    try:
                        self.data[name].append(float(value))
                    except ValueError:
                        self.data[name].append(None)

    def calc_missing_val(self, historicalDataTable = None):
        
        if historicalDataTable is None:
            means = {}
            for name, values in self.data.items():
                if name == "TumorType":
                    continue
                good = [v for v in values if v is not None]
                means[name] = sum(good) / len(good)
        else:
            means = historicalDataTable.get_means()

        for name, values in self.data.items():
            for i in range(len(values)):
                if values[i] is None:
                    values[i] = means[name]
        return means

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

    def get_means(self) -> dict:
        """
          returns a dict where key is column name and value is the average of that column
        """
        means = {}
        for name in self.get_column_names():
            means[name] = self.get_column_average(name)
        return means

    def __str__(self):
        lines = []
        for i in range(self.get_num_rows()):
            row = self.get_row(i)
            lines.append(", ".join(str(v) for v in row.values()))
        return "\n".join(lines)


