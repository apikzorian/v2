# Get the total time

fh = open("train.log", "r").read().splitlines()

total = 0
for l in fh:
    if "completed" in l:
        word = "seconds"
        idx = l.index(word)
        time = float(l[36:idx]) 
        total += time

print(total)