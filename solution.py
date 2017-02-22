import itertools
from utils import rows, cols, boxes, unitlist, peers

assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def get_counts(values, single_unit):
    """
    get the counts of twins and their values to help in naked_twins
    :param values: value dictionary
    :param single_unit: a unit of boxes
    :return: a tuple of counts of twins and values
    """
    # a dict that keeps a trak of the counts of duplicates
    # and which boxes it pertains to
    count_dict = {values[x]: {'count': 0, 'box': []} for x in single_unit}
    for box in single_unit:  # travers over each box in this unit
        if len(values[box]) == 2:
            count_dict[values[box]]['count'] += 1  # update count for the box value
            count_dict[values[box]]['box'].append(box)  # update the box number

    count_twins = [count_dict[k]['box'] for k, v in count_dict.items() if
                   count_dict[k]['count'] == 2]  # get the boxes with count = 2

    chain = itertools.chain(*count_twins)  # flatten the list [[a, b]] => [a, b]
    count_twins = list(chain)
    count_vals = [k for k, v in count_dict.items() if count_dict[k]['count'] == 2]  # vals
    return (count_twins, count_vals)


def replace_twin_digits(values, single_unit, count_twins, count_vals):
    """
    replaces the digits in other bozxes given the twins' digits
    :param values: value dictionary
    :param single_unit: a unit of boxes
    :return: values dictionary updated digits removal
    """
    if len(count_twins) > 0:
        for box in single_unit:  # traverse again, to remove elements
            # do only boxes that are not the twins
            if box not in count_twins and len(values[box]) > 2:
                for el in count_vals:
                    for digit in el:
                        values[box] = values[box].replace(digit, '')  # replace each digit
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

    for single_unit in unitlist:  # start with all the unit lists, one at a time
        (count_twins, count_vals) = get_counts(values, single_unit)
        values = replace_twin_digits(values, single_unit, count_twins, count_vals)
    return values


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
    """Eliminate values from peers of each box with a single value.

        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.

        Args:
            values: Sudoku in dictionary form.
        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
    """
    single_items = []
    for k, v in values.items():  # store all single items first
        if len(v) == 1:
            single_items.append(k)
    for i in single_items:  # go through single items only
        for peer in peers[i]:
            values[peer] = values[peer].replace(values[i], '')
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
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

        #  Use naked twins strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    perform the actual search, recursively using depth-first search and propagation,
    create a search tree and solve the sudoku.
    :param values: the values boxes dictionary
    :return:
    """
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

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print(
            'We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
