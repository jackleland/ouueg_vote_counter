
# coding: utf-8

# In[50]:


import math
import csv


# In[51]:


class Vote():
    def __init__(self, row):
        self.ranks = []
        self.voted_set = set()
        for rank in row:
            rank = rank.split('(')[0].strip()
            if rank not in self.voted_set:
                self.voted_set.add(rank)
                self.ranks.append(rank)
    
    def get_choice(self, disallowed):
        for rank in self.ranks:
            if rank not in disallowed:
                return rank
        return 'not counted'


# In[52]:


votes = []
with open('ouueg_results_anonymised.csv', newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        vote = Vote(row)
        votes.append(vote)


# In[60]:


no_of_votes_needed = math.ceil((len(votes) + 1) / 2)
print(f'There are {len(votes)} total votes, so a candidate motto requires {no_of_votes_needed} votes to win a majority')


# In[63]:


votes_for_leader = 0
round_no = 1
disallowed = set()
options = {
    'frigore turbidum mare itinerantur', 
    'submergo ergo sum',
    'rimam me habere puto',
    'omnia erit bene',
    'ave, oceane, morituri te salutant!',
    'duc in profundum',
    'resolve sis me',
    'ut plurimum siccus manemus',
    'ut sis nocte sollicitudin pede vulnus sentire quod a Moravia',
    'in aquae laetitia',
}

while votes_for_leader < no_of_votes_needed and round_no <= 10:
    print(f'\n\n Round {round_no}')
    results = {option: 0 for option in options - disallowed}
    for vote in votes:
        round_pref = vote.get_choice(disallowed)
        if round_pref == 'not counted':
            continue
        else:
            results[round_pref] += 1
    leaders, losers = [], []
    leader_vote_count = max(*results.values())
    loser_vote_count = min(*results.values())
    for candidate, count in results.items():
        if count == leader_vote_count:
            leaders.append(candidate)
        if count == loser_vote_count:
            losers.append(candidate)
    print(f'Results of round {round_no}: {results}')
    if len(leaders) == 1:
        votes_for_leader = leader_vote_count
    
    print(f'Removing {losers}')
    disallowed = disallowed | set(losers)
    round_no += 1

print('\n\n\nWinner found!')
print(leaders, votes_for_leader)
    

