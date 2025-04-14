import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        if len(self.cells) == self.count:
            return self.cells
        if mines <= self.cells:
            return mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes = set()
        if self.count == 0:
            return self.cells
        if safes <= self.cells:
            return safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            subtraction(self.cells, cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            subtraction(self.cells, cell)

    def __sub__(self, other):
        new_cells = self.cells - other.cells
        new_count = self.count - other.count
        new_sentence = Sentence(new_cells, new_count)
        return new_sentence

    def __gt__(self, other):
        return self.cells > other.cells and self.count >= other.count

    def __lt__(self, other):
        return self.cells < other.cells and self.count <= other.count

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # cell là toạ độ an toàn đã được mở, count là số mìn xung quanh cell
        # cell is the safe that has been opened, count is the number of mines around the cell
        # Xác định các ô xung quanh cell
        # Identify the cells surrounding the cell
        self.moves_made.add(cell)
        self.safes.add(cell)
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))

        # Xác định những ô đã mở hoặc bị đánh dấu có mìn
        # Identify open or marked mine cells
        neighbors, count = self.find(neighbors, count)
        if len(neighbors) == 0:
            return

        # Xác định sentence
        # Define sentence
        sentence = Sentence(neighbors, count)
        sentence = self.determining(sentence)
        if sentence:
            self.knowledge.append(sentence)

        # Infer
        self.infer()


    # Suy luận ra kết quả mới từ sentence và knowledge base
    # Infer new results from sentences and knowledge base
    def infer(self):
        new_sentences = []
        parent = []
        tpls = itertools.combinations(self.knowledge, 2)
        for sent in tpls:
            if sent[0] < sent[1]:
                x = sent[1] - sent[0]
                new_sentences.append(x)
                parent.append(sent[1])

            elif sent[0] > sent[1]:
                x = sent[0] - sent[1]
                new_sentences.append(x)
                parent.append(sent[0])

            else:
                self.knowledge.remove(sent[0])
                self.knowledge.append(sent[0])

        if len(parent) > 0:
            rmv = []
            for prt in parent:
                if prt not in rmv:
                    self.knowledge.remove(prt)
                    rmv.append(prt)
            parent.clear()
            for child in new_sentences:
                new_child = self.determining(child)
                if new_child:
                    self.knowledge.append(new_child)
        self.check_knowledge()
        return


    def check_knowledge(self):
        count = 0
        for sentence in self.knowledge.copy():
            x = self.determining(sentence)
            if not x:
                self.knowledge.remove(sentence)
                count += 1
        if count > 0:
            self.check_knowledge()
        else:
            return


    # Loại bỏ các cells đã xác định là mine/safe khỏi tập cells (neighbor)
    # Remove cells identified as mine/safe from the cell set (neighbor)
    def find(self, neighbors, count):
        subtract = set()
        for neighbor in neighbors:
            if neighbor in self.mines:
                count -= 1
                subtract.add(neighbor)
            elif neighbor in self.safes:
                subtract.add(neighbor)
        neighbors -= subtract
        return neighbors, count

    # Xác định cell trong set() là safe or mine, trả về sentence
    # Determine whether the cell in set() is safe or mine, return sentence
    def determining(self, sentence: Sentence):
        neighbors = sentence.cells
        count = sentence.count
        # Tất cả đều là mines
        # All are mines
        if len(neighbors) == count:
            for neighbor in neighbors.copy():
                self.mark_mine(neighbor)
            sentence = None
        # Tất cả đều là safe
        # All are safes
        elif count == 0:
            for neighbor in neighbors.copy():
                self.mark_safe(neighbor)
            sentence = None
        # Nếu đã kết luận đc chính xác số mine thì return None, còn ko thì sentence không đổi
        # If the number of mines is correctly concluded, return None, otherwise the sentence remains unchanged.
        return sentence

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        board = set()
        for i in range(self.height):
            for j in range(self.width):
                board.add((i, j))
        for i in self.mines:
            subtraction(board, i)
        for j in self.moves_made:
            subtraction(board, j)
        move = board & self.safes
        return list(move)[0] if move else None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        board = set()
        for i in range(self.height):
            for j in range(self.width):
                board.add((i, j))
        for i in self.mines:
            subtraction(board, i)
        for j in self.moves_made:
            subtraction(board, j)
        return list(board)[0] if len(board & self.safes) == 0 and len(board) > 0 else None


def subtraction(st: set, cell):
    c = set()
    c.add(cell)
    st -= c
    return st

