class Cellule():
    """
    Classe représentant une cellule, donc une personne.
    -params:
        -is_alive:bool, la cellule est-elle vivante ?
        -is_contaminated:bool, la cellule est-elle contaminée ?
        -is_immune:bool, le cellule est-elle immunisée ?
        -time:int, temps passé par la cellule en étant contaminé (1update = 1time)
    """

    def __init__(self,is_alive=True,is_contaminated=False, is_immune=False, time=0):
        self.is_alive = is_alive
        self.is_contaminated = is_contaminated
        self.is_immune = is_immune
        self.time = time