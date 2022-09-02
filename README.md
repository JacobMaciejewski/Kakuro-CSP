# Kakuro-CSP
Constraint Satisfaction Problem (CSP) theoretical definition and code implementation for Kakuro Puzzle Game 🧩

## Kakuro Game

The canonical [Kakuro puzzle](https://en.wikipedia.org/wiki/Kakuro) is played in a grid of filled and barred cells, **"black"** and **"white"** respectively. Puzzles are usually (`16×16`) in size,
although these dimensions can vary widely. Apart from the top row and leftmost column which are entirely black, the grid is divided into
"entries"—lines of white cells—by the black cells. The black cells contain a diagonal slash from upper-left to lower-right and a number in one
or both halves, such that each horizontal entry has a number in the black half-cell to its immediate left and each vertical entry has a number
in the black half-cell immediately above it. These numbers, borrowing crossword terminology, are commonly called `clues`.

The objective of the puzzle is to insert a **digit from 1 to 9** inclusive into each white cell so that the sum of the numbers in each entry matches
the clue associated with it and that no digit is duplicated in any entry. It is that lack of duplication that makes creating Kakuro puzzles with
unique solutions possible. Like Sudoku, solving a Kakuro puzzle involves investigating combinations and permutations. There is an unwritten rule
for making Kakuro puzzles that each clue must have at least two numbers that add up to it, since including only one number is mathematically trivial
when solving Kakuro puzzles.

An easy Kakuro Puzzle      |  Solution for the above puzzle
:-------------------------:|:-------------------------:
![](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Kakuro_black_box.svg/1024px-Kakuro_black_box.svg.png)  |  ![](https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Kakuro_black_box_solution.svg/1024px-Kakuro_black_box_solution.svg.png)

## CSP Definition:

**Kakuro Puzzle** can be modeled as a **Constraint Satisfaction Problem** (`CSP`) due to the finite number of value that the puzzle cells can take and the
dependencies that appear between them. The only variable aspect of the puzzle are the empty cells that have to be filled with numbers in range [1,9].
In order to make our model a little more rigid, we have to introduce some mathematical notation.

$P$ is the set containing the duplets that express the coordinates of the empty cells that have to be filled. Following the *Kakuro Solver* implementation,
we add $C$ as the set of constraints, represented by duplets of cells $I$ that are affected by the same limitations and a number which is the limit of the sum
of the two cells.

Our CSP variables are the empty cells that have to be filled. So, we define $X_{ij}$  $\forall (i,j) \in P$, the value of the cell at the coordinates [i,j].
The range of such variable is defined by the game to be bound in [1,9]. Now we can define the constraint, as follows:

$C_1 = AllDif[\forall x \in I]  \forall I \in C$, we want all the fields that belong to each constraint group $I$ to be different

$C_2 = ((\sum_{i}  x_i < n, \forall x_i \in I, \forall I \in C, \exists |D(x_i)| = 10) \cup (\sum_{i}  x_i = n, \nexists |D(x_i)| = 10))$, we want
the fields to sum up to the given constraint, if all of the were assigned a value. Οtherwise, the sum should be less than the constraint value.

## Backtracking Algorithms:

CSP Bibliography boasts a wide variety of [Backtracking Search Algorithms](https://www.geeksforgeeks.org/backtracking-algorithms/) that are used
to efficiently traverse the search space and limit the field values of the constraint variables. In this project, we wanted to focus on the theoretically
most powerful ones, namely [MAC](https://www.sciencedirect.com/topics/computer-science/arc-consistency-algorithm#:~:text=A%20constraint%20can%20be%20made,are%20made%20to%20the%20domains.)
(`Maintainig Arcs Consistency`) and [FC](https://ktiml.mff.cuni.cz/~bartak/constraints/propagation.html)(`Forward Checking`) with heuristic method named
[MRV](https://pdf.sciencedirectassets.com/278653/1-s2.0-S1877705812X00043/1-s2.0-S1877705812004092/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIF%2B0gwjQafWXIrfg%2BRAeXN0eGAvK%2Bybu%2FWSK3ys4gmU3AiEAk09YSUT9Bu%2F9kJ8vuofUqQNUvuHNr%2FNuqwWXO4mdBp0q1QQIg%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAFGgwwNTkwMDM1NDY4NjUiDCEvGr8Nld109BJAkCqpBHkg32BWorsPF9kBroEoZXyDvPUemy9OO3ZhTN6K9MC%2FO00%2BEzIpPsSZpLewvNvwbhbU1O%2FP3uC9uoYtqiBlu42LQvZ5GUrYgfvhv2G5L6vIG90rG13y9KHG9qKEvo4sBZTx0SxY1ClCS37QJUmpTWGmFTYn%2B7E6z1NVsqMFXS8xkwkVWPX0XY%2FqGIgsGL7lilIBwITkekRheoXOKMyxaqXmoqlD%2FOLFoPuhqchhUQKfXfT0gcppDRd5%2FMCZjDP1wkrm0DunlB0UdpUzSxtbDR5Hmh706K4K%2Fj2IBjK50XZHxiKxTzucaqa82Y4JikyfavNj8zJgDX1uK6Um0JQYqZkDrsXZX7tbXl5qJFpwTfdvTy7kkMKuTGfMb16cJz2XGKvTNB2ypIcL4%2BGdSD1eMEN0Eb88r7PnhjvnI2oGukJ5Yzx%2FBboCCZw87kFwWoX9x5ZYJ%2Bjx3d9ntKZh%2BrYbLglRhy1Apr8pDAs%2BBne5C26rJ588ccMMWNVaRoto3jn1epGNHrqMUG3ZSwl902uhm5hpvxTVDzrVXhjWZL6MQiYuRlW9Exjg8%2FRVOSU42Wvd6tndk1alQ8Q1Uf31H1AeJtbMKCwAcCCMEzLF3oSTEXDrTjKO%2BEZtiQd1Y5fQ3qKKoRmH29rR1nNidXp3hDNqNCdEii8P1rKj3CkAENHpsC5NM6Khw4z62RpR0TE%2BN%2BInt22wc9kK48Bf%2FtFDuLwWhJ1LjdiiQMOEa9wwxszFmAY6qQEUiMW77unXefi2yDf4I%2BPtubRiFy161XEBolf3qleveYbHRQsUc37SMgjIDLadK%2FsZpEg%2BReZQ1wcOQDe3QcWAITHwpzmvUMQEzw4FBM7dNd4Vz4cKQaexqjD5iWUECeUJlnuCsZXONQ1DeqtcK3idi2%2F0bh6n3xpRuNLT%2BbXEJrz9DThrrDQ6KpJmEOZT7SRY8bdeO7tmFVqMsuq3nWBquPkyw%2BwGJfwG&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220902T024855Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTY2SRTIABG%2F20220902%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=153cca5cd5e60a239e88c3215d9ceeace7c4cb06818aef473debed396076d6dd&hash=304e386cb4ee0138f13644301d26af822322946b77a7e2e53b308c019b14d664&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1877705812004092&tid=spdf-926f1f8d-be80-4c3d-bd48-4dffd2b9099c&sid=6aee5909444666497d0b6c4073e5e3ea2ce5gxrqb&type=client&ua=565a5b520304060852&rr=7442edef7fce38c9)
(Minimum Remaining Values). We aimed to examine the efficiency of those two approaches, namely the retaining of arcs' consistency and the removal
of invalid values from the neighbouring variables. 

We are interested in this setup, as it allows us to discern the search spaces in which each of the algorithms behaves the best:

* **MAC** - aims to  maintain the consistency of the fields of the neighbouring variables and their neighbours' as well, resulting in a quick
limitation of the search space in the tree in the case when we have a big number of neighbouring constraint groups. 

* **FC-MRV** - deletes dynamically the inconsistent values from neighbouring nodes (fast value filling of isolated groups). MRV, giving priority to
variables with the least remaining values, is fast to limit the possible combinations for bigger field groups.

## Code Structure & Design:

Our code contains the following utility files:

* **csp.py** - contains the definition of the class for binary constraints and subclasses referring to some popular problems belonging to that category

* **utils.py** - contains utility functions, mainly used in the code implementing the backtracking algorithms

* **search.py** - contains the definition of the class for space search

* **kakuro.py** - contains the definition of the custom Kakuro Puzzle problem, which is an example of a binary constraint problem

In order to differentiate and store the different constraint groups existent in the initial *Kakuro Board*, we construct a list of lists. In this way,
we are able to efficiently derive the common neighbours of two variables. Our main **constraint function**, using the constructed groups (lists), can infer
at each step the constraints imposed on each of the two examined variables and whether they belong to the same group. If so, evaluates whether the $C_1$
and $C_2$ constraints are satisfied under the proposed value assignment. 

## Execution:

In order to execute the program, you enter the command line within the working directory and type: `python3 kakuro_main.py`.
You will be then able to choose one of the two backtracking algorithms. Finally, 4 custom Kakuro Boards with increasing complexity (size) were hardcoded.
You can choose one of them, inserting the corresponding number.

### Further Informations

We include a **readME** PDF file that contains an extensive description of the project set up, the inner workings of the respective algorithms
and the design choices of the creator, namely me. It also contains extensive mathematical proofs for the remainig theoretical exercises posed by
the AI Course Assignment.

*Built as part of the course: Artificial Intelligence , Winter of 2019. University of Athens, DiT.*




