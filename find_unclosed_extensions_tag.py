def find_mismatched_extensions_tags(gpx_file_path):
    with open(gpx_file_path, "r") as file:
        extensions_count = 0
        line_number = 0

        for line in file:
            line_number += 1

            if "<extensions>" in line:
                extensions_count += 1
            elif "</extensions>" in line:
                extensions_count -= 1

                if extensions_count < 0:
                    print(f"Found extra </extensions> tag at line {line_number}.")
                    break

        if extensions_count > 0:
            print(f"Found {extensions_count} unclosed <extensions> tag(s).")
        elif extensions_count == 0:
            print("No mismatched <extensions> tags found.")

if __name__ == "__main__":
    gpx_file_path = "/Users/dwalter/Documents/projects/bm2023.gpx"
    find_mismatched_extensions_tags(gpx_file_path)
