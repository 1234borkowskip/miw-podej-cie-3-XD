import treelib

def generate_drzewo(koniec, ruchy):
    drzewo = treelib.Tree()
    drzewo.create_node(tag="0", identifier="0", data = [0, None, False])      # data = [wartosc liscia, wynik, is_this_parent_red]
    generate_galezie(drzewo, koniec, ruchy, "0")
    return drzewo

def generate_galezie(drzewo, koniec, ruchy, parent_id, parent_value=0):
    for current_value in ruchy:
        if(parent_value >= koniec):
            break
        else:
            drzewo.create_node(tag=parent_value + current_value, identifier=parent_id + "+" + str(current_value), parent=parent_id, data= [parent_value + current_value, None, False])
            generate_galezie(drzewo, koniec, ruchy, parent_id + "+" + str(current_value), parent_value + current_value)

def min_max(drzewo, koniec, ruchy, nazwa_aktualnego_node = "0"):
    aktualny_node = drzewo.get_node(nazwa_aktualnego_node)
    wartosc_aktualnego_node = aktualny_node.data[0]
    aktualny_poziom_glebokosci = drzewo.depth(aktualny_node)
    aktualny_player = (aktualny_poziom_glebokosci % 2) + 1  # 1 - protagonista, 2 - antagonista
    wynik = None

    if (drzewo.children(nazwa_aktualnego_node) == []):  # jeżeli aktualny liść jest końcowym (koniec gry)
        if(wartosc_aktualnego_node == koniec): # remis
            wynik = 0
        else:   # przegrana gracza który wykonał ostatni ruch
            if(aktualny_player == 1):   # ruch należałby do protagonisty (ale już nic nie może zrobić, przegrywający ruch wykonał antagonista)
                wynik = 1  # wygrał protagonista
            else:   # ruch należałby do antagonisty (ale już nic nie może zrobić, przegrywający ruch wykonał protagonista)
                wynik = -1   # wygrał antagonista

    else:   # jezeli aktualny liść nie jest końcowym
        if (aktualny_player == 1):  # ruch należy do protagonisty
            pozadany_wynik = 1  # pożądany wynik dla protagonisty
        else:  # ruch należy do antagonisty
            pozadany_wynik = -1  # pożądany wynik dla antagonisty

        for x in ruchy: # petla przechodzaca po kazdym dziecku aktualnego liscia
            wynik_dziecka_x = min_max(drzewo, koniec, ruchy, nazwa_aktualnego_node + "+" + str(x))   # wynik dla aktualnie badanego dziecka
            if(wynik_dziecka_x==pozadany_wynik): # jezeli wynik badanego dziecka jest pozadany
                wynik = wynik_dziecka_x # ustawienie wyniku dziecka jako wyniku rodzica
            elif(wynik_dziecka_x == 0 and wynik!=pozadany_wynik):  # jeżeli wynikiem badanego dziecka jest remis i w aktualnym wyniku nie ma już pożądanego wyniku
                wynik = 0   # ustawienie remisu jako aktualnego wyniku
            elif(wynik!=0 and wynik!=pozadany_wynik): # jezeli dziecko nie posiada pozadanego wyniku ani remisu i aktualny wynik ciągle nie został ustawiony
                wynik = wynik_dziecka_x # ustawienie wyniku dziecka jako wyniku rodzica

    drzewo.update_node(aktualny_node.identifier, data=[aktualny_node.data[0], wynik, aktualny_node.data[2]])  # wpisanie aktualnego wyniku do aktualnie badanego liścia
    return wynik    # zwrócenie wyniku aktualnie badanego liścia

def graph(drzewo, filename = "output.txt"):
    file = open(filename, "w")
    file.write('digraph tree {\n')
    wszystkie_node = drzewo.all_nodes() # zebranie wszystkich liści do obiektu
    for x in wszystkie_node:    # pętla dla wszystkich liści
        if(x.identifier != "0"):    # jeżeli dany liść nie jest korzeniem
            rodzic = drzewo.parent(x.identifier)    # ustalenie rodzica danego liścia
            tekst_rodzica = rodzic.identifier
            tekst_dziecka = x.identifier
            if (x.data[1] == rodzic.data[1] and rodzic.data[2] == False):    # jeśli jest połączenie między dzieckiem, a rodzicem (w sensie: taki sam wynik) i dany rodzic nie jest już połączony z innym dzieckiem
                file.write('    "'+tekst_rodzica+'" -> "'+ tekst_dziecka+'" [label = "'+x.identifier[-1]+'" color = "red"];\n') # łączenie kolorowane na czerwono
                rodzic.data[2] = True
            else:   # w przeciwnym wypadku - łączenie normalne
                file.write('    "' + tekst_rodzica + '" -> "' + tekst_dziecka + '" [label = "'+x.identifier[-1]+'"];\n')

    for x in wszystkie_node:    # opisanie każdego liścia na wykresie w logiczny sposób
        if(drzewo.children(x.identifier)==[]):
            gracz = "koniec"
        elif(drzewo.depth(x) % 2 == 0):
            gracz = "prot"
        else:
            gracz = "ant"
        wynik = "wynik: "+str(x.data[1])
        file.write('    "'+x.identifier+'" [label = "'+gracz+';\\nsuma: '+str(eval(x.identifier))+';\\n'+wynik+'"];\n')
    file.write('}\n')
    file.close()

# limit_koniec = 11
# mozliwe_ruchy = [4, 5, 6]

print("\nZadanie 5")

print("\nPodaj wartość graniczną: ")
limit_koniec = int(input())
print("\nPodaj możliwe ruchy oddzielając liczby spacją: ")
mozliwe_ruchy = list(map(int, input().strip().split(' ')))
print("\nPodaj nazwę pliku wynikowego dla skryptu GraphVis: ")
filename = input()

# print(mozliwe_ruchy)
drzewo3 = generate_drzewo(limit_koniec, mozliwe_ruchy)
min_max(drzewo3, limit_koniec, mozliwe_ruchy)
graph(drzewo3, filename)


