import tkinter as tk
from tkinter import ttk
import time

# Définition de la table de transition de l'automate qui
table = {
    # 1: {'a': 2, 'b': 1},
    # 2: {'a': 2, 'b': 3},
    # 3: {'a': 4, 'b': 1},
    # 4: {'a': 4, 'b': 4}
}



def create_automaton():
    for child in transition_frame.winfo_children():
        child.destroy()
    # tree.delete(*tree.get_children())
    # récupérer les données de l'utilisateur
    alphabet = alphabet_entry.get().split(",")
    n_states = int(states_entry.get())
    
    # créer la table de transition vide
    global table
    table = {}
    for i in range(n_states):
        table[i+1] = {}
        for symbol in alphabet:
            table[i+1][symbol] = None

    # ajouter le Treeview à la fenêtre principale
    tree = ttk.Treeview(transition_frame)
    tree.grid(row=0, column=1, padx=20, pady=20)

    # créer le Treeview pour la table de transition
    tree.configure(columns=[str(i) for i in range(len(alphabet)+1)], show="headings")
    for i in range(len(alphabet)):
        tree.heading(str(i+1), text=str(alphabet[i]))
    for i in range(len(alphabet)+1):
        tree.column(str(i), width=50)

    # ajouter les entrées pour chaque transition
    for i in range(n_states):
        tree.insert("", "end", values=[i+1])

    # définir la fonction de modification de cellule
    def edit_cell(event):
        # récupérer les indices de la cellule sélectionnée
        row_id = tree.selection()[0]
        col_id = tree.identify_column(event.x)

        # ouvrir l'éditeur de cellule
        cell_editing_window = tk.Toplevel(root)
        cell_editing_window.title(f"Edit Cell ({row_id}, {col_id})")

        # ajouter une entrée pour la valeur de la cellule
        cell_value_entry = tk.Entry(cell_editing_window)
        cell_value_entry.pack()

        # ajouter un bouton pour sauvegarder la valeur
        def save_cell_value():
            value = cell_value_entry.get()
            tree.set(row_id, col_id, value)
            cell_editing_window.destroy()

        save_button = tk.Button(cell_editing_window,text="Save", command=save_cell_value)
        save_button.pack()

    # lier la fonction de modification de cellule au clic gauche
    tree.bind("<Double-1>", edit_cell)

    # ajouter un bouton pour récupérer les données depuis le Treeview
    def get_table_data():
         # Récupère la table de transition depuis le Treeview.
        for i in range(n_states):
            for symbol in alphabet:
                cell_value = tree.item(tree.get_children()[i], "values")[alphabet.index(symbol)+1]
                table[i+1][symbol] = int(cell_value)
        
        # Creation de l'animation
        create_widgets()

    get_data_button = tk.Button(transition_frame, text="Create Automate", command=get_table_data)
    get_data_button.grid(row=2, column=1, padx=10)







def saisie():
    global cpt,table
    cpt=0

    # Définition de l'état initial
    etat = int(initial_state_entry.get())

    # Saisie de la chaîne à vérifier
    chaine = entry_mot.get()

    # Parcours de la chaîne et transition entre les états et regarde si la chaine contient "aba"
    for lettre in chaine:
        if lettre not in table[etat]:
            message["text"] = "La chaîne n'est pas acceptée"
            message["fg"] = "red"
            return False
        etat = table[etat][lettre]

    # Vérification de l'état final
    if etat in [int(state) for state in final_states_entry.get().split(",")] :
        message["text"] = "La chaîne est acceptée"
        message["fg"] = "green"
    else:
        message["text"] = "La chaîne n'est pas acceptée"
        message["fg"] = "red"


def create_widgets():
    global states

    # Effacer le canvas
    canvas.delete("all")
    
    # Recuperer le nombre d'Etat et les etats initiaux
    etats=int(states_entry.get())
    etat_final = [int(state) for state in final_states_entry.get().split(",")]
    
    # Donner à chaque etat une position sur le canvas
    positions={}
    inc=0
    for i in range(1,etats+1):
        if i%2==0:
            positions[i]=(75+inc, 250)
        else:
            positions[i]=(75+inc, 100)
        inc+=150

    # Ajouter des états
    states=[]
    for i in range(1,etats+1):
        x, y = positions[i]
        if i in etat_final:
            canvas.create_oval(x-25-10, y-25-10, x+25+10, y+25+10, outline="black")
        states.append(canvas.create_oval(x-25, y-25, x+25, y+25, fill="white",tags="final" if i in etat_final else ""))
        canvas.create_text(x, y, text=str(i))

        

    # Ajouter des transitions
    transitions = []
    for orig, trans in table.items():
        x1, y1 = positions[orig]
        for lettre, dest in trans.items():
            x2, y2 = positions[dest]
            if dest==orig:
                print("boucle")
            else:
                if x1>x2:
                    transitions.append(canvas.create_line(x1-30, y1, x2+30, y2, arrow="last",width=1))
                else: 
                    transitions.append(canvas.create_line(x1+30, y1, x2-30, y2, arrow="last",width=1))
                canvas.create_text((x1+x2)/2+5, (y1+y2)/2+15, text=lettre)



def Recup_Etats_Chaine():


    global table

    # Définition de l'état initial
    etat = int(initial_state_entry.get())

    # recuperation de la chaîne à vérifier
    chaine = entry_mot.get()

    # Recuperer les differentes transition dans un tableau
    tab_etat=[states[0]]

    bande=[]

    # Parcours de la chaîne et transition entre les états et regarde si la chaine contient "aba"
    for lettre in chaine:
        if lettre not in table[etat]:
            tab_etat.append(False)
            bande.append([lettre,etat])
            return (tab_etat,bande)
        etat = table[etat][lettre]
        tab_etat.append(states[etat-1])
        bande.append([lettre,etat])
    return (tab_etat,bande)


def step():
    global current_state,cpt,t_bandes
    
    # Initialiser le tableau de transition
    tab,bande=Recup_Etats_Chaine()
    # Mettre à jour l'état actuel
    current_state = tab[cpt]
    if cpt!=len(tab):
        cpt+=1
    

    # Mettre à jour la couleur de l'état actuel
    for state in tab:
        if state == current_state and current_state==False :
            canvas.itemconfig(tab[-2], fill="red")
        elif state == current_state and canvas.itemcget(state, "tags")!="final" and cpt==len(tab) :
            canvas.itemconfig(state, fill="red")
        elif state == current_state and canvas.itemcget(state, "tags")=="final" and cpt==len(tab) :
            canvas.itemconfig(state, fill="green")
        elif state == current_state:
            canvas.itemconfig(state, fill="white")
            canvas.update()
            time.sleep(1/50)
            canvas.itemconfig(state, fill="orange")
        else:
            canvas.itemconfig(state, fill="white")
    

    x, y= 100, 330
    for lettre,etat in bande:
        t_bandes.append(canvas.create_rectangle(x,y,x+50,y+50, fill='orange', outline="white"))
        # Ajouter la lettre
        t_bandes.append(canvas.create_text((x+x+50)/2, (y+y+50)/2, text=str(lettre), font=('Arial', 24)))
        t_bandes.append(canvas.create_text((x+x+50)/2, (y+y+50)/2+50, text=str(etat), font=('Arial', 24)))
        x+=50



def reset():
    global current_state,cpt,t_bandes
    # Réinitialiser l'état actuel
    current_state = states[0]
    cpt=0
    # Réinitialiser la couleur de tous les états
    for state in states:
        canvas.itemconfig(state, fill="white")
    
    for bande in t_bandes:
        canvas.delete(bande)


# Créer la fenêtre principale
root = tk.Tk()

canvas_frame = ttk.LabelFrame(root, text="Simulation de la lecture par l\'automate")
canvas_frame.grid(row=0, column=1,padx=10, pady=2)
canvas_frame.place(x=320,y=0)

# Créer le canevas
canvas = tk.Canvas(canvas_frame,scrollregion=(0, 0, 2000, 600))
canvas.config(width=900, height=500)
canvas.grid(row=0, column=1, columnspan=2)

scrollbar_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar_y.grid(row=0, column=0)

scrollbar_x = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar_x.grid(row=0, column=0)

canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)


# Ajouter du champ de saisie
entry_mot = tk.Entry(canvas_frame,font=8)
entry_mot.grid(row=1, column=2)


message = tk.Label(canvas_frame, width=100, height=3, font=12,)
message.grid(row=2, column=2)

# Ajouter des boutons
button_step = tk.Button(canvas_frame, text="Step", command=step)
button_step.grid(row=3, column=1)

button_submit = tk.Button(canvas_frame, text="Submit", command=saisie)
button_submit.grid(row=3, column=2)

button_reset = tk.Button(canvas_frame, text="Reset", command=reset)
button_reset.grid(row=3, column=3)

# Initialisaton des globals
states = []
cpt = 0
t_bandes = []

input_frame = ttk.LabelFrame(root, text="Paramètres d'entrée")
input_frame.grid(row=0, column=0)
input_frame.place(x=0,y=0)

transition_frame = ttk.LabelFrame(root, text="Table de transition")
transition_frame.grid(row=1, column=0, pady=10)
transition_frame.place(x=0,y=270)

# ajouter les champs de saisie pour l'utilisateur
alphabet_label = tk.Label(input_frame, text="Alphabet:")
alphabet_label.grid(row=0, column=1,padx=5, pady=5)
alphabet_entry = tk.Entry(input_frame)
alphabet_entry.grid(row=1, column=1)

states_label = tk.Label(input_frame, text="Number of States:")
states_label.grid(row=2, column=1,padx=5, pady=5)
states_entry = tk.Entry(input_frame)
states_entry.grid(row=3, column=1)

initial_state_label = tk.Label(input_frame, text="Initial State:")
initial_state_label.grid(row=4, column=1,padx=5, pady=5)
initial_state_entry = tk.Entry(input_frame)
initial_state_entry.grid(row=5, column=1)

final_states_label = tk.Label(input_frame, text="Final States (comma-separated):")
final_states_label.grid(row=6, column=1,padx=5, pady=5)
final_states_entry = tk.Entry(input_frame)
final_states_entry.grid(row=7, column=1)

# ajouter un bouton pour créer l'automate
create_button = tk.Button(input_frame, text="Get Table", command=create_automaton)
create_button.grid(row=8, column=1,padx=5, pady=5)

# Démarrer la boucle d'événements tkinter
root.mainloop()
