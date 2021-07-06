import time

start = time.time()

with open('input', 'r') as file:
    line = file.readline()
    n_players = int(line.split(' players')[0])
    max_worth = int(line.split(' ')[-2])


class Node:
    def __init__(self, value=0, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


    def destruct(self):
        ''' remove links to the current node
            use condition just to be safe '''

        if self.prev is not None:
            self.prev.next = self.next # destruct link from previous node
        if self.next is not None:
            self.next.prev = self.prev # destruct link from next node



class Game:
    def __init__(self, n_players=9, max_worth=25):
        self.n_players = n_players
        self.max_worth = max_worth
        self.scores = dict.fromkeys(range(self.n_players), 0)
        self.head = None
        self.current_marble = None
        self.marble = 0
        self.player = 0


    def init(self):
        ''' create first node and set init state '''

        start_node = Node(self.marble, None, None)
        # init state
        self.marble += 1
        self.head = start_node
        self.current_marble = self.head
        # make links from first node to itself (make a loop ^^)
        self.current_marble.next = self.head
        self.current_marble.prev = self.head


    def insert(self):
        ''' insert node just after current one '''

        new_node = Node(self.marble, self.current_marble, self.current_marble.next)
        self.current_marble.next.prev = new_node # change link from next node
        self.current_marble.next = new_node # change link from current one
        self.current_marble = self.current_marble.next # change current node to just inserted one


    def delete(self):
        ''' delete current node '''

        self.current_marble.destruct() # remove (change) links from nearest nodes
        self.current_marble = self.current_marble.next # change current node to the next one


    def play(self):
        ''' play the game '''

        self.init()
        for marble in range(1, self.max_worth + 1):
            self.marble = marble # current number
            self.player = (self.marble - 1) % self.n_players # current player

            if marble % 23 == 0:
                # get a prize (some points) for lucky number :)
                for _ in range(7): # calculate additional bonus :)
                    self.current_marble = self.current_marble.prev
                self.scores[self.player] += self.marble + self.current_marble.value # send prize to player
                self.delete() # remove "bonus" node
            else:
                # or just add new marble to the circle
                self.current_marble = self.current_marble.next # define the insertion place
                self.insert()


    def max_score(self):
        return max(self.scores.values())


    def winner(self):
        sorted_players = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_players[0][0] + 1 # [0] - winner; [0] - player id; '+ 1' - actual player number

    def circle(self):
        ''' return entire circle as list '''

        current_position = self.head.next
        circle = [self.head.value, ]
        while self.head != current_position:
            circle.append(current_position.value)
            current_position = current_position.next
        return circle

# test case (answer 8317):
# n_players = 10
# max_worth = 1618

max_worth *= 100 # part 2 condition

marble_game = Game(n_players=n_players, max_worth=max_worth)
marble_game.play()

print('Game results:')
print('Winner: {}'.format(marble_game.winner()))
print('Max score: {}\n'.format(marble_game.max_score()))
# print('Entire circle: {}'.format(marble_game.circle))
print('Evaluating time: {}'.format(time.time() - start))






# shitty first solution (DO NOT DO IT LIKE THIS!)

# import numpy as np

# circle = np.array([0, ])
# scores = dict.fromkeys(range(n_players), 0)

# def place(current_marble, marble, player, circle, scores):
#     circle_len = circle.size
#     if marble % 23 == 0:
#         current_marble = (current_marble - 7) % circle_len
#         scores[player] += marble + circle[current_marble]
#         circle = np.delete(circle, current_marble)
#         # correct id after deletion
#         current_marble = current_marble % (circle_len - 1)
#     else:
#         current_marble = (current_marble + 2) % circle_len
#         if current_marble == 0:
#             current_marble = circle_len
#         circle = np.insert(circle, current_marble, marble)

#     return current_marble, circle, scores


# current_marble = 0
# for marble in range(1, max_worth + 1):
#     player = marble % n_players
#     current_marble, circle, scores = place(current_marble, marble, player, circle, scores)

# print(circle)
# print('Part 1: {}'.format(max(scores.values())))
