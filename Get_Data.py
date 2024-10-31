from re import A
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt


class Data_Frame:

    def __init__(self, link = None):
        self.df = pd.read_csv(link)

    def calculate_points(self):
        scoring_weights = {
            'receptions': 0.5, # half-PPR
            'receiving_yds': 0.1,
            'receiving_td': 6,
            'rushing_yds': 0.1,
            'rushing_td': 6,
            'passing_yds': 0.04,
            'passing_td': 4,
            'int': -2
        }
        self.df['FantasyPoints'] = (
           self.df['Receptions']*scoring_weights['receptions'] + self.df['ReceivingYds']*scoring_weights['receiving_yds'] + \
           self.df['ReceivingTD']*scoring_weights['receiving_td'] + \
           self.df['RushingYds']*scoring_weights['rushing_yds'] + self.df['RushingTD']*scoring_weights['rushing_td'] + \
           self.df['PassingYds']*scoring_weights['passing_yds'] + self.df['PassingTD']*scoring_weights['passing_td'] + \
           self.df['Interceptions']*scoring_weights['int'] )
        col = ['Player','Team','Pos','FantasyPoints', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'RushingAtt', 'RushingYds', 'RushingTD']
        self.df = self.df.loc[:,col]

    def rb_df(self):
        basic_col = ['Player','Team','Pos']
        rb_col = ['FantasyPoints', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'RushingAtt', 'RushingYds', 'RushingTD']
        self.rb_df = self.df.loc[self.df['Pos'] == 'RB',basic_col+rb_col]
        # print(self.rb_df.sort_values(by='RushingYds', ascending=False).head())
        # print(self.rb_df.describe())
        # print(self.rb_df.describe().transpose())
        self.rb_df['RushingTDRank'] = self.rb_df['RushingTD'].rank(ascending=False)
        # print(self.rb_df.sort_values(by='RushingTDRank').head(5))
        # print(self.rb_df.values[:5])

    def wr_df(self):
        basic_col = ['Player','Team','Pos']
        wr_col = ['FantasyPoints', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'RushingAtt', 'RushingYds', 'RushingTD']
        self.wr_df = self.df.loc[self.df['Pos'] == 'WR',basic_col+wr_col]
        # print(self.wr_df.sort_values(by='RecievingYds', ascending=False).head())
        # print(self.wr_df.describe())
        # print(self.wr_df.describe().transpose())
        self.wr_df['RecievingTDRank'] = self.wr_df['ReceivingTD'].rank(ascending=False)
        print(self.wr_df.sort_values(by='RecievingTDRank').head(5))
        print(self.wr_df.values[:20])

    def plot_rb_data(self):
        sb.set_style('whitegrid')
        sb.distplot(self.rb_df['RushingAtt']);
        plt.show()

    def get_adp(self,link_adp = None):
        self.adp_df = pd.read_csv(link_adp)
        self.adp_df['ADP RANK'] = self.adp_df['Current ADP'].rank()
        # print(self.adp_df.head())

    def adp_cutoff(self, cutoff = None):
        self.adp_df_cutoff = self.adp_df[:cutoff]
        # print(self.adp_df_cutoff.shape)

    def replacement_players(self): #gets last player (per position) drafted from ADP to calculate VOR
        self.replacement_ply = {'RB': '','QB': '','WR': '','TE': ''}
        for _, row in self.adp_df_cutoff.iterrows():
            position = row['Pos'] # extract out the position and player value from each row as we loop through it
            player = row['Player']
    
            if position in self.replacement_ply: # if the position is in the dict's keys
                self.replacement_ply[position] = player # set that player as the replacement player
        print(self.replacement_ply)

    def replacement_values(self):
        self.replacement_values = {} # initialize an empty dictionary
        for position, player_name in self.replacement_ply.items():
    
            player = self.df.loc[self.df['Player'] == player_name.strip()]
            self.replacement_values[position] = player['FantasyPoints'].tolist()[0] #values needed to calculate VOR
    
        print(self.replacement_values)

    def calculate_VOR(self):
        pd.set_option('chained_assignment', None)
        self.df = self.df.loc[self.df['Pos'].isin(['QB', 'RB', 'WR', 'TE'])]
        self.df['VOR'] = self.df.apply(
            lambda row: row['FantasyPoints'] - self.replacement_values.get(row['Pos']), axis=1
        )
        self.df['VOR RANK'] = self.df['VOR'].rank(ascending=False)
        self.df = self.df.sort_values(by='VOR RANK')
        print(self.df.groupby('Pos')['VOR'].describe())

    def normalize_VOR(self):
        self.df['VOR'] = self.df['VOR'].apply(lambda x: (x - self.df['VOR'].min()) / (self.df['VOR'].max() - self.df['VOR'].min()))
        
    def plot_VOR(self):
        # calculating how many players are in our draft pool.
        num_teams = 12
        num_spots = 16 # 1 QB, 2RB, 2WR, 1TE, 1FLEX, 1K, 1DST, 7 BENCH
        draft_pool = num_teams * num_spots

        self.df_copy = self.df[:100]

        sb.boxplot(x=self.df_copy['Pos'], y=self.df_copy['VOR']);
        plt.show()
    def rename_df_col(self):
        self.df = self.df.rename({
            'VOR': 'Value',
            'VOR RANK': 'Value Rank'
        }, axis=1) # axis = 1 means make the change along the column axis.
        # self.df['Player'] = self.df['Player'].replace({
        #     'Kenneth Walker III': 'Kenneth Walker',
        #     'Travis Etienne Jr.': 'Travis Etienne',
        #     'Brian Robinson Jr.': 'Brian Robinson',
        #     'Pierre Strong Jr.': 'Pierre Strong',
        #     'Michael Pittman Jr.': 'Michael Pittman',
        #     'A.J. Dillon': 'AJ Dillon',
        #     'D.J. Moore': 'DJ Moore'
        # })
        self.adp_df = self.adp_df.rename({
            'PLAYER': 'Player',
            'POS': 'Pos',
            'Current ADP': 'Average ADP',
            'ADP RANK': 'ADP Rank'
        }, axis=1)


    def merge_df(self):
        pd.set_option('display.max_rows', None) # turn off truncation of rows setting inherent to pandas
        self.adp_df = self.adp_df.drop('Team', axis=1)
        self.final_df = self.df.merge(self.adp_df, how='left', on=['Player', 'Pos'])
        # print(self.final_df.loc[self.final_df['Pos'] == 'RB'].describe())
        print(self.final_df.head(100))
        # let's calculate the difference between our value rank and adp rank
        self.final_df['Diff in ADP and Value'] = self.final_df['ADP Rank'] - self.final_df['Value Rank']
        #removing outliers in ADP
        self.final_df = self.final_df.loc[self.final_df['ADP Rank'] <= 212]
        print(self.final_df.head(100))

    def draft_pool(self):
        self.draft_pool = self.final_df.sort_values(by='ADP Rank')[:196]
        print(self.draft_pool.head(100))
        self.rb_draft_pool = self.draft_pool.loc[self.draft_pool['Pos'] == 'RB']
        self.qb_draft_pool = self.draft_pool.loc[self.draft_pool['Pos'] == 'QB']
        self.wr_draft_pool = self.draft_pool.loc[self.draft_pool['Pos'] == 'WR']
        self.te_draft_pool = self.draft_pool.loc[self.draft_pool['Pos'] == 'TE']
        print(self.rb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10])
        print(self.qb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10])
        print(self.wr_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10])
        print(self.te_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10])


def main():
    link_df = 'https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/refs/heads/master/2023/06-Data%20Munging/01-Fantasy%20Pros%20Projections%20-%20(2023.08.17).csv'
    link_adp = 'https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/refs/heads/master/2023/06-Data%20Munging/02-ADP%20Data%20-%20(2023.08.17).csv'
    ff = Data_Frame(link_df)
    ff.calculate_points()
    # ff.rb_df()
    # ff.wr_df()
    #ff.plot_rb_data()
    ff.get_adp(link_adp)
    ff.adp_cutoff(cutoff = 100)
    ff.replacement_players()
    ff.replacement_values()
    ff.calculate_VOR()
    ff.normalize_VOR()
    # ff.plot_VOR()
    ff.rename_df_col()
    ff.merge_df()
    ff.draft_pool()

if __name__ == "__main__":
    main()
        
