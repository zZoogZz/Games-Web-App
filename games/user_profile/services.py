def get_game(game_id):
    game = repo.repo_instance.get_game(game_id)
    return game