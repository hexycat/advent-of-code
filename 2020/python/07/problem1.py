import pprint
from typing import List, Tuple

class Inventory():
  def __init__(self, content: Tuple[int, str] = None):
    self.inv = {}
    if content:
      self.add_many(content)
    self.size = sum(self.inv.values())
    
  def add_many(self, content: Tuple[int, str] = None):
    for bag_name, bag_count in content:
      self.add(bag_name, bag_count)
    self.size = sum(self.inv.values())

  def add(self, bag_name: str, bag_count: str):
    self.inv[bag_name] = bag_count
    self.size = sum(self.inv.values())

  def __contains__(self, bag_name: str):
    return bag_name in self.inv.keys()

  def names(self):
    return self.inv.keys()

  def counts(self):
    return self.inv.values()
  
  def sub_bag_count(self, sub_bag_name: str):
    return self.inv[sub_bag_name]


class Bag:
  def __init__(self, name: str):
    self.name = name
    self.inventory = Inventory()

  def __contains__(self, bag_name):
    return bag_name in self.inventory

  def __iter__(self):
    return iter(self.inventory.names())

  def add_inventory(self, content: Tuple[int, str] = None):
    self.inventory.add_many(content)


def parse_rules(rules_list: List[str]) -> List[Bag]:
  bags_db = {}
  for rule in rules_list:
    # we are able to parse string using splits 
    rule = rule.strip().replace('.', '').replace('bags', '').replace('bag', '')
    main_bag, conteining_bags = rule.split('contain')
    bag = Bag(main_bag.strip())
    bags_db[bag.name] = bag
    if 'no other' in conteining_bags:
      continue
    inventory_content = []
    for bag_str in conteining_bags.split(','):
      count, bag_name = bag_str.strip().split(' ', 1)
      inventory_content.append((bag_name.strip(), int(count.strip())))
    bags_db[bag.name].add_inventory(inventory_content)
  return bags_db

def is_contain(bags_db: List[Bag], bag: str, search_bag: str) -> None:
  if search_bag in bags_db[bag]:
    return True
  for sub_bag_name in bags_db[bag]:
    contain = is_contain(bags_db, sub_bag_name, search_bag)
    if contain:
      return True
  return False

def get_bag_contianers(bags_db: List[Bag], target_bag: str) -> int:
  containers = [is_contain(bags_db, bag, target_bag) for bag in bags_db]
  return sum(containers)



if __name__ == "__main__":
  with open('input.txt', 'r') as file:
    rules = file.readlines()
  target_bag = 'shiny gold'
  bags_db = parse_rules(rules)
  number_of_bag_containers = get_bag_contianers(bags_db, target_bag)
  pprint.pprint(number_of_bag_containers)