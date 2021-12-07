import json
import random
import string


class FwfParser:
    """
    For parsing fixed width file of a spec into CSV file.
    """

    def set_spec(self, file_path: str):
        """
        Set the specs of the FWF file.
        """
        with open(file_path) as f:
            spec = json.load(f)

        self.spec = spec

    def generate_fwf(self, to_path: str, rows: int = 1) -> None:
        """
        Generate a fixed with file based on the specs with random values.
        """
        with open(to_path, "w", encoding=self.spec["FixedWidthEncoding"]) as f:
            if self.spec["IncludeHeader"] == "True":
                f.write(
                    (
                        "".join(
                            [
                                col_name.ljust(int(self.spec["Offsets"][i]))
                                for i, col_name in enumerate(self.spec["ColumnNames"])
                            ]
                        )
                        + "\n"
                    )
                )

            for _ in range(rows):
                row = ""

                for offset in self.spec["Offsets"]:
                    offset = int(offset)
                    random_chars = "".join(
                        random.choices(
                            string.ascii_uppercase + string.digits,
                            k=random.randint(0, offset),
                        )
                    )
                    row += random_chars.ljust(offset)

                row += "\n"

                f.write(row)

    def to_csv(self, fw_path: str, to_path: str) -> None:
        """
        Convert a fixed with file based on a spec to a csv file.
        """
        with open(fw_path, "r", encoding=self.spec["FixedWidthEncoding"]) as read_file:
            with open(
                to_path, "w", encoding=self.spec["DelimitedEncoding"]
            ) as write_file:
                while read_file:
                    line = read_file.readline()

                    if line == "":
                        break

                    col_values = []
                    offset_sum = 0
                    for offset in self.spec["Offsets"]:
                        offset = int(offset)

                        col_values.append(
                            line[offset_sum : offset_sum + offset].strip()
                        )

                        offset_sum += offset

                    csv_row = ",".join(col_values)
                    write_file.write(csv_row + "\n")
