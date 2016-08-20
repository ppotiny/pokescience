__author__ = 'Praneetha'

import pandas as pd

main_csv = pd.read_csv('veekun_data/pokemon_species.csv')

# drop unnecessary columns
main_csv = main_csv.drop(['evolves_from_species_id', 'color_id', 'shape_id', 'is_baby', 'hatch_counter',
                          'growth_rate_id', 'forms_switchable', 'order', 'conquest_order'], axis=1)


def merge_ids(csv1, csv2, left, right, drops):
    csv2 = csv2.drop(drops, axis=1)
    csv1 = pd.merge(csv1, csv2, left_on=left, right_on=right)
    csv1 = csv1.drop([right], axis=1)
    return csv1


csv1= pd.read_csv('veekun_data/pokemon_types.csv')
csv2 = pd.read_csv('veekun_data/types.csv')
csv1 = merge_ids(csv1, csv2, 'type_id', 'id', ['generation_id', 'damage_class_id'])
csv1 = csv1.sort(columns='pokemon_id')
csv1 = csv1.pivot(index='pokemon_id', columns='slot', values='identifier')
csv1 = csv1.reset_index()
main_csv = merge_ids(main_csv, csv1, 'id', 'pokemon_id', [])

csv1= pd.read_csv('veekun_data/pokemon_stats.csv').drop(['effort'], axis=1)
csv2 = pd.read_csv('veekun_data/stats.csv')
csv1 = merge_ids(csv1, csv2, 'stat_id', 'id', ['damage_class_id', 'is_battle_only', 'game_index'])
csv1 = csv1.sort(columns='pokemon_id')
csv1 = csv1.pivot(index='pokemon_id', columns='identifier', values='base_stat')
csv1 = csv1.reset_index()
#csv1 = csv1[csv1.identifier != 'pokemon_id']
main_csv = merge_ids(main_csv, csv1, 'id', 'pokemon_id', [])

csv1 = pd.read_csv('veekun_data/pokemon_habitats.csv')
csv1 = csv1.rename(columns=({'id': 'hab_id'}))
main_csv = merge_ids(main_csv, csv1, 'habitat_id', 'hab_id', [])

main_csv.drop(['habitat_id'], axis=1)
main_csv = main_csv.rename(columns=({'identifier_x': 'species', 1: 'type1', 2: 'type2',
                                     'identifier_y': 'habitat'}))

print main_csv.head()

main_csv.to_csv('pokemon_data.csv', index=False)