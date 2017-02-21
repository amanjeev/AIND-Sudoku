assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for single_unit in unitlist:
        count_dict = {values[x]: {'count': 0, 'box': []} for x in single_unit}
        for box in single_unit:
            if len(values[box]) == 2:
                count_dict[values[box]]['count'] += 1
                count_dict[values[box]]['box'].append(box)

        count_boxes = [count_dict[k]['box'] for k, v in count_dict.items() if count_dict[k]['count'] == 2]
        count_vals = [k for k, v in count_dict.items() if count_dict[k]['count'] == 2]
        import itertools
        chain = itertools.chain(*count_boxes)
        count_boxes = list(chain)

        if len(count_boxes) > 0:
            for box in single_unit:
                if box not in count_boxes and len(values[box]) > 2:
                    for el in count_vals:
                        for digit in el:
                            values[box] = values[box].replace(digit, '')
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# to solve the diagonal we just need to add units for diagonals
# of the grid like the following -
diag_units = [[s[0] + s[1] for s in list(zip(rows, cols))],  # A1 to I9
              [s[0] + s[1] for s in list(zip(rows, cols[::-1]))]]  # I1 to A9
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'.
                    If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    assert len(boxes) == 81, "Input boxes must be a string of length 81 (9x9)"

    grid_list = list(grid)
    grid_list_with_nums = ['123456789' if x == '.' else x for x in
                           grid_list]  # replace '.' with '1234..9'
    return dict(zip(boxes, grid_list_with_nums))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    single_items = []
    for k, v in values.items():  # store all single items first
        if len(v) == 1:
            single_items.append(k)
    for i in single_items:  # go through single items only
        for peer in peers[i]:
            values[peer] = values[peer].replace(values[i], '')
    return values


def only_choice(values):
    for single_unit in unitlist:
        for d in '123456789':
            dp = [box for box in single_unit if d in values[box]]
            if len(dp) == 1:
                values[dp[0]] = d
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)

    # Choose one of the unfilled squares with the fewest possibilities

    # Now use recursion to solve each one of the resulting sudokus,
    # and if one returns a value (not False), return that answer!
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n, s = min([(len(values[s]), s) for s in boxes if len(values[s]) > 1])
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    # try:
    #     from visualize import visualize_assignments
    #
    #     visualize_assignments(assignments)
    #
    # except SystemExit:
    #     pass
    # except:
    #     print(
    #         'We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
