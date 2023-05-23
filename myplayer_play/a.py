with open('b.py', 'r') as f:
    move = int(f.read())
    print(move)

move +=2

with open('b.py', 'w') as f:
    f.write(str(move))

