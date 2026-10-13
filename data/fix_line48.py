with open("data/train.jsonl", encoding="utf-8") as f:
    lines = f.readlines()

print(f"before: {len(lines)} lines")
print(f"line 48 length: {len(lines[47])}")

# Line 48 is at index 47. It contains two JSON objects glued together.
# They end with `}` and start with `{`. Split at `}{`.
line = lines[47].rstrip("\n")
# Find the boundary between the two JSON objects
split_at = line.find("}{")
if split_at == -1:
    print("No glued objects found. Nothing to fix.")
else:
    first = line[: split_at + 1]
    second = line[split_at + 1 :]
    lines[47] = first + "\n"
    lines.insert(48, second + "\n")
    print(f"after: {len(lines)} lines")

    with open("data/train.jsonl", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("fixed")