# Global variables that we can access in other files

LIGHT_GREEN = [169 / 256, 221 / 256, 175 / 256, 1]
GREEN = [62 / 256, 182 / 256, 75 / 256, 1]
DARK_GREEN = [16 / 256, 118 / 256, 0, 1]
LIGHT_RED = [256/256,187/256,187/256,1]
RED = [237/256,79/256,79/256,1]
DARK_RED = [170/256,14/256,14/256,1]
LIGHT_BLUE = [182 / 256, 229 / 265, 246 / 256, 1]
BLUE = [112 / 256, 159 / 265, 256 / 256, 1]
DARK_BLUE = [82 / 256, 129 / 265, 256 / 256, 1]
SAND = [219/256,195/256,151/256,1]
WHITE = [1, 1, 1, 1]
BLACK = [0, 0, 0, 1]
TRANSPARENT = [1, 1, 1, 0]
SEMI_TRANSPARENT = [1, 1, 1, 0.3]
MAROON = [115/256, 63/256, 11/256, 1]

LNG = "en"

D_text_button = {
    "pressText":{"en":" Press when you \nfinished your move","fr":" Appuie queand tu\nas fini de jouer"},
    "releaseText":{"en":"Ned is playing...","fr":"Ned est en train de jouer"},
    "restartText":{"en":"Remove the pieces\nto play again","fr":"Enleve les pieces\npour recommencer"},
    "level_intermediate": {"en": "Intermediate", "fr": "Intermédiaire"},
    "level_expert":{"en":"Expert","fr":"Expert"},
    "play_2nd":{"en":"Play 2nd","fr":"Jouer en 2"},
    "play_again":{"en":"Play again","fr":"Jouer encore"},
    "train":{"en":"Train","fr":"Entraîner"},
    "ai":{"en":"AI","fr":"IA"},
    "minimax":{"en":"Minimax","fr":"Minimax"},
    "confirm":{"en":"Confirm","fr":"Valider"},
    "novice":{"en":"Novice","fr":"Novice"},
    "beginner":{"en":"Beginner","fr":"Débutant"},
    "intermediate":{"en":"Intermediate","fr":"Intermédiaire"},
    "expert":{"en":"Expert","fr":"Expert"},
    "custom":{"en":"Custom","fr":"Personnalise"},
    "parameter_language":{"en":"Language","fr":"Langue"},
    "tic_tac_toe":{"en":"Tic tac toe","fr":"Morpion"},
    "connect_4":{"en":"Connect 4","fr":"Puissance 4"},
    "chess":{"en":"Chess","fr":"Echecs"},
    "":{"en":"","fr":""},


    }

D_text_train = {
    "model_name":{"en":"Name of the model: ","fr":"Nom du modèle: "},
    "n_layers":{"en":"Number of layers","fr":"Nombre de couches"},
    "n_epochs":{"en":"Number of epochs: ","fr":"Nombre d'epoques: "},
    "n_neurons":{"en":"Number of neurons per layer","fr":"Nombre de neurones par couche"},
    "loading_info_error":{"en":"Error loading the informations.","fr":"Erreur de chargement des informations."},
    "learning_rate":{"en":"Learning rate: ","fr":"Taux d'apprentissage: "},
    "discount_factor":{"en":"Discount factor: ","fr":"Facteur de reduction:"},
    "train_the_model":{"en":"Train the model","fr":"Entraîne le modele"},
    "":{"en":"","fr":""},

}


D_text_log = {
    # errors
    "error_name_str":{"en":"[ERROR] The model could not be created \nGive a valid name to your model","fr":"[ERREUR] Le modele n'a pas pu etre créé \nDonne un nom valide à ton modele"},
    "error_name_empty":{"en":"[ERROR] The model name cannot be empty.","fr":"[ERREUR] Le nom du modele ne peut pas etre vide."},
    "error_name_already_exists":{"en":"[ERROR] The model could not be created \nThis name is already taken!","fr":"[ERREUR] Le modele n'a pas pu etre créé \nCe nom est deja pris !"},
    "error_n_neurons_inf":{"en":"[ERROR] The model could not be created \nThe model cannot have 0 neurons!","fr":"[ERREUR] Le modele n'a pas pu etre créé \nLe modele ne peut pas avoir 0 neurone !"},
    "error_n_neurons_sup":{"en":"[ERROR] The model could not be created \nThe model cannot have more than 512 neurons per layer!","fr":"[ERREUR] Le modele n'a pas pu etre créé \nLe modele ne peut pas avoir plus de 512 neurones par couche !"},
    "error_n_neurons_interval":{"en":"[ERROR] The number of neurons must be between 1 and 512.","fr":"[ERREUR] Le nombre de neurones doit être compris entre 1 et 512."},
    "error_n_layers_inf":{"en":"[ERROR] The model could not be created \nThe model cannot have 0 neuron layers!","fr":"[ERREUR] Le modele n'a pas pu etre créé \nLe modele ne peut pas avoir 0 couche de neurones !"},
    "error_n_layers_sup":{"en":"[ERROR] The model could not be created \nThe model cannot have more than 10 layers!","fr":"[ERREUR] Le modele n'a pas pu etre créé \nLe modele ne peut pas avoir plus de 10 couches !"},
    "error_n_layers_interval":{"en":"[ERROR] The number of layers must be between 1 and 10.","fr":"[ERREUR] Le nombre de couches doit être compris entre 1 et 10."},
    "error_unknown":{"en":"[ERROR] The model could not be created \nUnknown error!","fr":"[ERREUR] Le modele n'a pas pu etre créé \nErreur inconnue !"},
    "error_model_delete":{"en":"[ERROR] Unable to delete the model","fr":"[ERREUR] Impossible de supprimer le modele"},
    "error_default_model_delete":{"en":"[ERROR] Unable to delete default models","fr":"[ERREUR] Impossible de supprimer les modeles presents par defaut"},
    "error_n_epochs_interval":{"en":"[ERROR] The number of epochs must be between 1 and 10000.","fr":"[ERREUR] Le nombre d'epoques doit être compris entre 1 et 10000."},
    "error_learning_rate_interval":{"en":"[ERROR] The learning rate must be between 0.00001 and 0.1.","fr":"[ERREUR] Le taux d'apprentissage doit être compris entre 0.00001 et 0.1."},
    "error_discount_factor_interval":{"en":"[ERROR] The discount factor must be between 0.1 and 0.999","fr":"[ERREUR] Le facteur de réduction doit être compris entre 0.1 et 0.999"},
    "error_invalid_input":{"en":"[ERROR] You must fill all fields with valid values before starting training.","fr":"[ERREUR] Tu dois remplir tous les champs avec une valeur valide avant de lancer l'entrainement."},
    "error_model_already_training":{"en":"[ERROR] This model is already in training.","fr":"[ERREUR] Ce modèle est déjà en cours d'entrainement."},
    "error_too_much_models_training":{"en":"[ERROR] You cannot train more than 3 models at once.","fr":"[ERREUR] Tu ne peux pas entrainer plus de 3 modeles a la fois."},
    "":{"en":"","fr":""},
    "":{"en":"","fr":""},
    "":{"en":"","fr":""},

    # infos

    "info_successful_model_creation":{"en":"[INFO] Model successfully created:","fr":"[INFO] Création réussie du modèle :"},
    "info_successful_model_delete":{"en":"[INFO] Model successfully deleted:","fr":"[INFO] Suppression réussie du modèle:"},
    "info_successful_started_training":{"en":"[INFO] Training successfully started for model:","fr":"[INFO] Entraînement lancé avec succès du modèle:"},
    "info_successful_finished_training":{"en":"[INFO] Training completed for model:","fr":"[INFO] Entrainement terminé du modèle:"},
    "":{"en":"","fr":""},
    "":{"en":"","fr":""},
    "":{"en":"","fr":""},

}

D_static_texts = {
    "models_list":{"en":"Models list","fr":"Liste des modeles"},
    "model_info":{"en":"Infos about the model","fr":"Infos sur le modele"},
    "model_choice":{"en":"Select Ned's AI model","fr":"Selectionne le modele d'IA de Ned"},
    "custom_model":{"en":"Custom model","fr":"Modele personnalise"},
    "models_in_training":{"en":"Models currently training:","fr":"Modeles en cours d'entrainement:"},
    "explain_minimax_vs_ai":{"en":"The Minimax algorithm was designed by humans to give the computer a winning strategy\n\nThe AI played thousands of games to learn, without needing human help!","fr":"L'algorithme Minimax a été pensé par des humains pour donner une stratégie gagnante à l'ordinateur\n\nL'IA a joué des milliers de parties pour apprendre, sans avoir besoin de l'aide d'un humain !"},
    "question_opponent_choice":{"en":"How to choose your opponent?","fr":"Comment choisir ton adversaire ?"},
    "minimax_pressed":{"en":"Warning, it is impossible to win against an opponent who knows a winning strategy!","fr":"Attention, il est impossible de gagner face à un adversaire qui connaît une stratégie gagnante !"},
    "ai_pressed":{"en":"Against the AI, you have every chance of winning.","fr":"Face à l'IA, tu as toutes tes chances de gagner."},
    "level_choice":{"en":"Choose your opponent's training level!","fr":"Choisis le niveau d'entrainement de ton adversaire !"},
    "question_level_choice":{"en":"Which level to choose?","fr":"Quel niveau choisir ?"},
    "level_choice_ai":{"en":"Choose the AI's training level!","fr":"Choisis le niveau d'entrainement de l'IA !"},
    "level_choice_minimax":{"en":"Choose the Minimax algorithm level!","fr":"Choisis le niveau de l'algorithme Minimax !"},
    "level_choice_ai_advice":{"en":"The higher the selected level, the stronger the AI.\n\nTo be stronger, the AI trained by playing more games, it's that simple!","fr":"Plus le niveau sélectionné est élevé plus l'IA est forte.\n\nPour être plus forte, l'IA s'est entraînée en jouant plus de partie, tout simplement !"},
    "level_choice_minimax_advice":{"en":"The higher the selected level, the more powerful the algorithm.\n\nTo be more efficient, the Minimax algorithm will explore many possible games to determine the move that is most favorable to it!","fr":"Plus le niveau sélectionné est élevé plus l'algorithme est puissant.\n\nPour être plus performant, l'algorithme Minimax va explorer plein de parties possibles pour déterminer le coup qui lui est le plus favorable !"},
    "level_choice_ai_beginner":{"en":"In this mode, the AI has never been trained: it's discovering the game!","fr":"Dans ce mode, l'IA n'a jamais été entraînée : elle découvre le jeu ! "},
    "level_choice_minimax_beginner":{"en":"In this mode, the algorithm only plans one move ahead... not very efficient.","fr":"Dans ce mode, l'algorithme ne prévoit qu'un coup à l'avance... pas très performant. "},
    "level_choice_ai_intermediate":{"en":"In this mode, the AI has only played 1000 games: its learning was very short!","fr":"Dans ce mode, l'IA n'a joué que 1000 parties : son apprentissage a été très court ! "},
    "level_choice_minimax_intermediate":{"en":"In this mode, the algorithm explores 3 moves ahead: it's starting to see your move coming!","fr":"Dans ce mode, l'Algorithme explore 3 coups à l'avance : il commence à voit ton coup venir ! "},
    "level_choice_ai_expert":{"en":"In this mode, the AI has played 5000 games: 5 times more experience than beginner mode.\nUp to you to discover its evolution!","fr":"Dans ce mode, l'IA a joué 5000 parties : 5 fois plus d'expérience qu'au mode débutant.\nA toi de découvrir son évolution ! "},
    "level_choice_minimax_expert":{"en":"Warning... in this mode, the algorithm plays all possible games 5 moves ahead, it reads your game very clearly...","fr":"Attention... dans ce mode, l'algorithme joue toutes les parties possibles avec 5 coups d'avance, il lit très clair dans ton jeu..."},
    "level_choice_ai_custom":{"en":"You can choose the AI model you want to use. To create new ones, you can go to the home page","fr":"Tu peux choisir le modèle d'IA que tu souhaites utiliser. Pour en créer de nouveaux, tu peux aller sur la page d'accueil"},
    "level_choice_minimax_novice":{"en":"In this mode, the algorithm doesn't explore games: it plays randomly","fr":"Dans ce mode, l'algorithme n'explore pas de parties: il joue aléatoirement "},
    "opponent_choice":{"en":"Choose your opponent !","fr":"Choisis ton adversaire !"},
    "":{"en":"","fr":""},
    "":{"en":"","fr":""},
    "":{"en":"","fr":""},
    "":{"en":"","fr":""},
    "":{"en":"","fr":""},

    "parameter_choice":{"en":"Choose the parameter you want to modify","fr":"Choisis le paramètre que tu veux modifier"},
    "parameter_title":{"en":"Settings","fr":"Paramètres"},
    "parameter_language_info":{"en":"For now, only French is available","fr":"Pour le moment, seul le français est disponible"},
    "parameter_tic_tac_toe_info":{"en":"Modify Tic Tac Toe settings!","fr":"Modifier les paramètres du Morpion !"},
    "parameter_connect_4_info":{"en":"Modify Connect 4 settings!","fr":"Modifier les paramètres du Puissance 4 !"},
    "parameter_chess_info":{"en":"Under development...","fr":"En cours de développement..."},
    "":{"en":"","fr":""},
    "":{"en":"","fr":""},



}

ROBOT = False

MODEL_NAME = ""

class var:
    def __init__(self):
        self.MODE = ""
        self.LEVEL = ""
        self.GAME = ""
        self.model_name = ""

    def __str__(self):
        return f"Mode: {self.MODE}, Level: {self.LEVEL}, Game: {self.GAME}, AI Model: {self.model_name}"

var1 = var()

if __name__=="__main__":
    print(D_text["pressText"]["en"])
