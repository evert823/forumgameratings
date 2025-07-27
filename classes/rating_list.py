import pandas as pd
from datetime import datetime

class RatingList:
    def __init__(self):
        self.myratings: list[tuple[str, int]] = []
        self.mynextgames: list[tuple[datetime, str, str, str]] = []
        self.rating_floor = 1000

    def load_init_ratings_from_df(self, ratings_df: pd.DataFrame, column_name_player: str, column_name_rating: str):
        self.myratings.clear()
        for _, row in ratings_df.iterrows():
            player = row[column_name_player]
            rating = row[column_name_rating]
            self.myratings.append((player, rating))
        self._deduplicate_players()

    def load_next_gamelist_from_df(self, games_df: pd.DataFrame,
                                   column_name_date:str, date_which_format:str,
                                   column_name_white: str, column_name_black: str,
                                   column_name_result: str):
        self.mynextgames.clear()
        for _, row in games_df.iterrows():
            myinputdate = row[column_name_date]
            mydatetime = datetime.strptime(myinputdate, date_which_format)
            white_player = row[column_name_white]
            black_player = row[column_name_black]
            myresult = row[column_name_result]
            self.mynextgames.append((mydatetime, white_player, black_player, myresult))
        self._sort_mynextgames()

    def add_new_players(self):
        for gm in self.mynextgames:
            self._add_players_from_game(gm)
        #self._deduplicate_players()
        self._sort_myratings()

    def _sort_mynextgames(self):
        self.mynextgames.sort(key=lambda x: x[0])

    def _sort_myratings(self):
        self.myratings.sort(key=lambda x: x[0])

    def _deduplicate_players(self):
        unique_players = set()
        deduplicated = []
        for item in self.myratings:
            if item[0] not in unique_players:
                unique_players.add(item[0])
                deduplicated.append(item)
        self.myratings = deduplicated

    def show_list(self, mylist):
        print(mylist[0])
        print(mylist[1])
        print(mylist[2])
        print("...")
        print(mylist[-3])
        print(mylist[-2])
        print(mylist[-1])
        print(f"Count : {len(mylist)}")

    def _add_players_from_game(self, game: tuple[datetime, str, str, str]):
        namelist = set([rt[0] for rt in self.myratings])
        if game[1] not in namelist:
            self.myratings.append((game[1], self.rating_floor))
            namelist.add(game[1])
        if game[2] not in namelist:
            self.myratings.append((game[2], self.rating_floor))
            namelist.add(game[2])

    def _get_myratings_i(self, playername: str):
        for i in range(len(self.myratings)):
            if self.myratings[i][0] == playername:
                return i
        raise Exception(f"Mismatch in _get_myratings_i")
    
    def _get_rating_impact_record(self, rating_impact_table_df:pd.DataFrame,
                                  rating_difference: int):
        for _, row in rating_impact_table_df.iterrows():
            if (row['rating_diff_from'] <= rating_difference and
                row['rating_diff_till'] >= rating_difference):
                return row
        return None

    def _clean_result(self, result):
        if result in ['1-0', '0-1', '0.5-0.5']:
            return result
        if result.find('1-0') > -1:
            return '1-0'
        if result.find('1 - 0') > -1:
            return '1-0'
        if result.find('0-1') > -1:
            return '0-1'
        if result.find('0 - 1') > -1:
            return '0-1'
        if result.find('.5') > -1:
            return '0.5-0.5'
        if result.find('/2') > -1:
            return '0.5-0.5'
        if result.upper().find('R') > -1:
            return '0.5-0.5'
        return None

    def rating_diff_logic(self, rating_impact_row, game_result,
                          old_rating_white, min_rating_white,
                          old_rating_black, min_rating_black):
        myresult = self._clean_result(game_result)
        if myresult == '0.5-0.5':
            if old_rating_white >= old_rating_black:
                new_rating_white = old_rating_white + rating_impact_row['rating_incr_higher_if_draw']
                new_rating_black = old_rating_black + rating_impact_row['rating_incr_lower_if_draw']
            else:
                new_rating_white = old_rating_white + rating_impact_row['rating_incr_lower_if_draw']
                new_rating_black = old_rating_black + rating_impact_row['rating_incr_higher_if_draw']
        elif myresult == '1-0':
            if old_rating_white >= old_rating_black:
                new_rating_white = old_rating_white + rating_impact_row['rating_incr_higher_if_win']
                new_rating_black = old_rating_black + rating_impact_row['rating_incr_lower_if_loss']
            else:
                new_rating_white = old_rating_white + rating_impact_row['rating_incr_lower_if_win']
                new_rating_black = old_rating_black + rating_impact_row['rating_incr_higher_if_loss']
        elif myresult == '0-1':
            if old_rating_white >= old_rating_black:
                new_rating_white = old_rating_white + rating_impact_row['rating_incr_higher_if_loss']
                new_rating_black = old_rating_black + rating_impact_row['rating_incr_lower_if_win']
            else:
                new_rating_white = old_rating_white + rating_impact_row['rating_incr_lower_if_loss']
                new_rating_black = old_rating_black + rating_impact_row['rating_incr_higher_if_win']
        else:
            raise Exception(f"Unknown game result: {game_result}")
        
        if new_rating_white < min_rating_white:
            new_rating_white = min_rating_white
        if new_rating_black < min_rating_black:
            new_rating_black = min_rating_black
        
        return new_rating_white, new_rating_black

    def _alter_rating(self, player_i, new_rating):
        self.myratings[player_i] = (self.myratings[player_i][0], new_rating)

    def _process_game_in_ratings(self, game: tuple[datetime, str, str, str],
                                 rating_impact_table_df:pd.DataFrame):
        whiteplayer = game[1]
        whiteplayer_i = self._get_myratings_i(whiteplayer)
        old_rating_white = self.myratings[whiteplayer_i][1]
        if old_rating_white < self.rating_floor:
            old_rating_white = self.rating_floor
        min_rating_white = (old_rating_white + self.rating_floor) // 2
        blackplayer = game[2]
        blackplayer_i = self._get_myratings_i(blackplayer)
        old_rating_black = self.myratings[blackplayer_i][1]
        if old_rating_black < self.rating_floor:
            old_rating_black = self.rating_floor
        min_rating_black = (old_rating_black + self.rating_floor) // 2
        rating_difference = abs(old_rating_white - old_rating_black)
        rating_impact_row = self._get_rating_impact_record(rating_impact_table_df, rating_difference)
        new_rating_white, new_rating_black = self.rating_diff_logic(rating_impact_row=rating_impact_row,
                                game_result=game[3],
                                old_rating_white=old_rating_white, min_rating_white=min_rating_white,
                                old_rating_black=old_rating_black, min_rating_black=min_rating_black)
        self._alter_rating(whiteplayer_i, new_rating_white)
        self._alter_rating(blackplayer_i, new_rating_black)
        #print(f"{game[0]},{old_rating_white},{old_rating_black},{game[3]},{new_rating_white},{new_rating_black}")

    def execute_rating_cycle(self, rating_impact_table_df:pd.DataFrame):
        for i in range(len(self.mynextgames)):
            self._process_game_in_ratings(self.mynextgames[i], rating_impact_table_df)

