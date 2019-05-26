import pandas as pd
import copy
import sys


def construct_table():
    return pd.DataFrame([[2500, 4000, 3500],
                         [4000, 6000, 3500],
                         [2000, 4000, 2500]], columns=['Delhi', 'Kerela', 'Mumbai'],
                        index=['Jaipur', 'Pune', 'Bangalore'])


if __name__ == '__main__':
    # ===== Create the Table =====
    table = construct_table()
    op_table = copy.deepcopy(table)

    # Implement Hungarian Algorithm
    # ===== Step 1: Subtract minimum from each row =====
    for index, row in op_table.iterrows():
        op_table.loc[index] = row.subtract(row.min())

    # ===== Step 2: Subtract minimum from each row =====
    for index, column in op_table.iteritems():
        op_table[index] = column.subtract(column.min())

    # ===== Step 3: Draw Lines =====
    ticked_rows = []
    ticked_columns = []
    zero_locations = (op_table == 0)
    total_lines = 0
    # Draw Lines for rows
    for index, row in zero_locations.iterrows():
        tick = zero_locations.loc[index][zero_locations.loc[index] == True].index
        check_column_ticked = [True if i in ticked_columns else False for i in list(tick)]
        ticked_rows += [index]
        if not any(check_column_ticked):
            total_lines += 1
            ticked_columns += list(tick)
        else:
            total_lines += 1

    # Draw for columns
    for index, column in zero_locations.iteritems():
        tick = zero_locations[index][zero_locations[index] == True].index
        check_row_ticked = [True if i in ticked_rows else False for i in list(tick)]
        check_column_ticked = [True if i in ticked_columns else False for i in [index]]
        if not any(check_column_ticked) and not any(check_row_ticked):
            total_lines += 1
            ticked_columns += list(tick)

    # Check if lines drawn is equal to size of matrix
    if not total_lines == len(op_table):
        print('Number of lines drawn is not equal to size of Matrix.')
        print('Matrix is not optimal. Exiting. In future, we may try to optimize matrix if not optimal...')
        sys.exit(0)
    else:
        print('We have optimal Matrix, continuing to find optimal cost...')
        for index, row in zero_locations.iterrows():
            row_with_single_zero = zero_locations.loc[index][zero_locations.loc[index] == True]
            if len(row_with_single_zero) > 1:
                continue
            else:

                for j, cell in zero_locations[row_with_single_zero.index].iterrows():
                    if j != index:
                        zero_locations.loc[j, zero_locations[row_with_single_zero.index].columns] = \
                            zero_locations.loc[j, zero_locations[row_with_single_zero.index].columns].replace({True: False})

    print('The optimal cost is...')
    print(table[zero_locations].fillna(0).sum().sum())
    print('The locations where salespeople will be sent is...')
    for index, column in table[zero_locations].fillna(0).iteritems():
        print('From {} to {} with a cost of {}'.format(column[column > 0].index[0], index, str(column[column > 0][0])))

