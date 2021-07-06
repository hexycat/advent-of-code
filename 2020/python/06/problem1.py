from typing import List
import pprint

def load_group(answers_list: List[str]):
  group_answers = ''
  for person_answers in answers_list:
    if person_answers == '\n':
      yield group_answers
      group_answers = ''
    group_answers += person_answers.strip()
  yield group_answers

def parse_groups_answers(answers_list: List[str]) -> int:
  groups_yes = {}
  for group_id, group_answers in enumerate(load_group(answers_list)):
    groups_yes[group_id] = len(set(list(group_answers)))
  return groups_yes

if __name__ == "__main__":
  with open('input.txt', 'r') as file:
    answers_list = file.readlines()
  groups_yes = parse_groups_answers(answers_list)
  pprint.pprint(groups_yes)
  print(f'Total yes: {sum(groups_yes.values())}')
  