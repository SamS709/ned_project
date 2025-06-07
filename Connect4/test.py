import keras

model = keras.models.Sequential([
    keras.layers.Dense(50, input_shape=[50,]),
    keras.layers.Dense(50)
])

layers = model.layers
cfg = model.get_config()
print(layers)
print(cfg)
print(len(cfg['layers']))
n_layers = len(cfg['layers'])
n_neurons_per_layer = cfg['layers'][1]['config']['units']
n_neurons_tot = (n_layers-1)*n_neurons_per_layer
a = f"Le modèle est composé de {str(n_layers)} couches:\n  - La première est une couche d'entrée spécifiant la taille de la grille: ici 6x7 = 42.\n"
a+= f"  - Les autres sont des couches denses de neurones tous reliés entre eux.\nIci, chaque couche est composée de {str(n_neurons_per_layer)} neurones.\nLe modèle est donc composé au total de {str(n_neurons_tot)} neurones !"
print(a)