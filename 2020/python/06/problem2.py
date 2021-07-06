from typing import List, Callable, Iterable
from collections import Counter

class Group():
  def __init__(self):
    self.answers = ''
    self.size = 0

  def reset(self):
    self.answers = ''
    self.size = 0

  def add_answer(self, answer: str):
    self.answers += answer
    self.size += 1


class Rule():
  @staticmethod
  def apply(group: Group) -> int:
    return 0

class AnsweredByAllRule(Rule):
  @staticmethod
  def apply(group: Group) -> int:
    counts = Counter(group.answers)
    return sum([n_question_answers == group.size for _, n_question_answers in counts.most_common()])


def load_group(answers_list: List[str]):
  group = Group()
  for person_answers in answers_list:
    if person_answers == '\n':
      yield group
      group.reset()
    else:
      group.add_answer(person_answers.strip())
  yield group

def parse_groups_answers(answers_list: List[str], parse_answers_rule: Rule) -> int:
  groups_yes = {}
  for group_id, group in enumerate(load_group(answers_list)):
    groups_yes[group_id] = parse_answers_rule.apply(group)
  return groups_yes

if __name__ == "__main__":
  with open('input.txt', 'r') as file:
    answers_list = file.readlines()
  answered_by_all_rule = AnsweredByAllRule()
  groups_yes = parse_groups_answers(answers_list, answered_by_all_rule)
  print(f'Total yes: {sum(groups_yes.values())}')