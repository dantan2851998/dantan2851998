from minesweeper import Sentence

x = {(1, 2), (3, 4), (5, 6)}


a = Sentence(x, 1)
b = Sentence(x, 1)
if a == b:
    print("hello")
#a.mark_mine((1,2))

#a.cells = a.cells - set((1,2))
e = set()
e.add((1,2))
#x -= e
q = set((1,2))
x -= q
print(a)
