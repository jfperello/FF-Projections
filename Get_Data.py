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
           self.df['Int']*scoring_weights['int'] )
  
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

    def plot_rb_data(self):
        sb.set_style('whitegrid')
        sb.distplot(self.rb_df['RushingAtt']);
        plt.show()

    def get_adp(self,link_adp = None):
        self.adp_df = pd.read_csv(link_adp)
        self.adp_df['ADP RANK'] = self.adp_df['Current ADP'].rank()
        print(self.adp_df.head())

def main():
    link_df = 'https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/refs/heads/master/2023/06-Data%20Munging/01-FDP%20Projections%20-%20(2023.03.30).csv'
    link_adp = 'https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/master/2023/06-Data%20Munging/02-ADP%20Data%20-%20(2023.03.30).csv'
    #creating an instance of a class
    jj = Data_Frame(link_df)
    jj.calculate_points()
    jj.rb_df()
    #jj.plot_rb_data()
    jj.get_adp(link_adp)

if __name__ == "__main__":
    main()
        
