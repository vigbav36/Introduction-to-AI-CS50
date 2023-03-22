import sys

from crossword import *

from copy import deepcopy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        for variable in self.domains :
            words = deepcopy(self.domains[variable])
            for word in words:
                if len(word) != variable.length :
                    self.domains[variable].remove(word)



    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revise =False
        words_x = self.domains[x]
        words_y = self.domains[y]

        if self.crossword.overlaps[x,y] is None:
            return False

        i,j = self.crossword.overlaps[x,y]
        remove = set()
        for word_x in words_x:
            for word_y in words_y:
                count = 0
                if word_x[i] != word_y[j]:
                    revise = True
                    count+=1
            if count == len(words_y):
                remove.add(word_x)

        for word in remove:
            self.domains[x].remove(word)

        return revise
                    

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
    
        """
        queue = []

        if arcs is None:
            for x in self.domains:
                for y in self.domains:
                    if x != y and self.crossword.overlaps[x,y] is not None:
                        queue.append((x,y))
        else:
            queue = arcs

        while len(queue) > 0 :
            x,y = queue.pop()
            if self.revise(x,y):
                if len(self.domains[x]) == 0 :
                    return False
                for z in (self.crossword.neighbors(x) - {y}):
                    queue.append((z, x))
                
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:
            if variable not in assignment or assignment[variable] is None:
                return False;
        return True
        

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        variables = assignment.keys()

        for x in variables:
            if len(assignment[x]) != x.length:
                return False
            for y in variables:
                if x!=y and self.crossword.overlaps[x,y] is not None:
                    i,j = self.crossword.overlaps[x,y]
                    if assignment[x][i] != assignment[y][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        exclude = set()
        for v in assignment:
            exclude.add(assignment[v])
        
        count_dict = dict()
        for word in self.domains[var]:
            count_dict[word] = 0

        neighbors =  self.crossword.neighbors(var) - assignment.keys()
        for word1 in self.domains[var]:
            for neighbor in neighbors:
                i, j  = self.crossword.overlaps[var,neighbor]
                for word2 in self.domains[neighbor]:
                    if word1[i] != word2[j]:
                        count_dict[word1]+=1

        sorted_list = sorted(count_dict.items(), key=lambda x:x[1])
        values = list()

        for x in sorted_list:
            if x[0] not in exclude:
                values.append(x[0])
        return  values



    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        remaining = list(self.crossword.variables - assignment.keys())

        count_values = dict()
        for var in remaining:
            count_values[var] = len(self.domains[var])
            
        count_degree = dict()
        for var in remaining:
            count_degree[var] = len(self.crossword.neighbors(var))

        sorted_list = sorted(remaining, key=lambda x:(count_values[var], -count_degree[var]) )
        return sorted_list[0]
        
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #self.print(assignment)
        if self.assignment_complete(assignment=assignment):
            return assignment

        var = self.select_unassigned_variable(assignment=assignment)
        values = self.order_domain_values(var,assignment)

        for value in values:
            dummy_assignment = deepcopy(assignment)
            dummy_assignment[var] = value
            if self.consistent(dummy_assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                assignment.pop(var, None)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
