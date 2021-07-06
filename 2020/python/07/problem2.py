from problem1 import Bag, parse_rules
from typing import Dict

def get_bag_size(bags_db, bag_name):
  total_size = 0
  bag = bags_db[bag_name]
  for sub_bag_name in bag:
    sub_bag_count = bag.inventory.sub_bag_count(sub_bag_name)
    sub_bag_size = get_bag_size(bags_db, sub_bag_name)
    total_size += sub_bag_count * sub_bag_size + sub_bag_count
  return total_size

if __name__ == "__main__":
  with open('input.txt', 'r') as file:
    rules = file.readlines()
  target_bag = 'shiny gold'
  bags_db = parse_rules(rules)
  bag_size = get_bag_size(bags_db, target_bag)
  print(bag_size)