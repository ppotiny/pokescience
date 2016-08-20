__author__ = 'Praneetha'

# All of the files used in this program belong to 'https://github.com/veekun'

# I picked out the data that I thought was interesting and merged into one large data-set

# Files such as 'types.csv' only gave an id to each pokemon type. Therefore,
# files that contained the pokemon species' id along with the id of their stat/type/etc. were merged
# with files that actually contained the name of stat/type/etc. respectively.

# This is to make it easier for me to show what is going on with each feature in the data

import pandas as pd

main_csv = pd.read_csv('pokemon_species.csv')

# drop unnecessary columns from main file
main_csv = main_csv.drop(['evolves_from_species_id', 'color_id', 'shape_id', 'is_baby', 'hatch_counter',
                          'growth_rate_id', 'forms_switchable', 'order', 'conquest_order'], axis=1)


def merge_ids(csv1, csv2, left, right, drops):
    """ Merges two csv files based on a column and
    drops some unnecessary columns """
    csv2 = csv2.drop(drops, axis=1)
    csv1 = pd.merge(csv1, csv2, left_on=left, right_on=right)
    csv1 = csv1.drop([right], axis=1)
    return csv1

# Pokemon type files are read in
csv1= pd.read_csv('pokemon_types.csv')
csv2 = pd.read_csv('types.csv')
# These files are merged by their id
csv1 = merge_ids(csv1, csv2, 'type_id', 'id', ['generation_id', 'damage_class_id'])
csv1 = csv1.sort(columns='pokemon_id')  # Sort by pokemon species id
csv1 = csv1.pivot(index='pokemon_id', columns='slot', values='identifier') # Make each type a column
csv1 = csv1.reset_index()  # Pivot got rid of our index column, let's add it again
main_csv = merge_ids(main_csv, csv1, 'id', 'pokemon_id', [])  # Merge with the main file

# Pokemon stats files are read in
csv1= pd.read_csv('pokemon_stats.csv').drop(['effort'], axis=1)
csv2 = pd.read_csv('stats.csv')
csv1 = merge_ids(csv1, csv2, 'stat_id', 'id', ['damage_class_id', 'is_battle_only', 'game_index'])
csv1 = csv1.sort(columns='pokemon_id')
csv1 = csv1.pivot(index='pokemon_id', columns='identifier', values='base_stat')
csv1 = csv1.reset_index()
main_csv = merge_ids(main_csv, csv1, 'id', 'pokemon_id', [])

# Pokemon habitat file is read in
csv1 = pd.read_csv('pokemon_habitats.csv')
csv1 = csv1.rename(columns=({'id': 'hab_id'}))
main_csv = merge_ids(main_csv, csv1, 'habitat_id', 'hab_id', [])

main_csv.drop(['habitat_id'], axis=1)
main_csv = main_csv.sort(columns='id')

# Some features had common names, adjusted based on preference of names
main_csv = main_csv.rename(columns=({'identifier_x': 'species', 1: 'type1', 2: 'type2',
                                     'identifier_y': 'habitat'}))

# Print first 5 rows of main file to check if everything is correct
print main_csv.head()

# Create new csv file with updated data
main_csv.to_csv('pokemon_data.csv', index=False)