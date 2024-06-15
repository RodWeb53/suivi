# Fonction pour la lecture des fichier excel
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import sqlite3

import pandas as pd

from suiviclient.settings import BASE_DIR


@staff_member_required
def mise_a_jour_base(request):

    # Lecture des fichiers excel
    data_stock_global = pd.read_excel(BASE_DIR / 'base_donnees/StockGlobal.xlsx')
    data_base_nomenclature = pd.read_excel(BASE_DIR / 'base_donnees/BaseNomenclature.xlsx')
    data_base_operation = pd.read_excel(BASE_DIR / 'base_donnees/BaseOperation.xlsx')
    data_base_of = pd.read_excel(BASE_DIR / 'base_donnees/BaseOF.xlsx')
    data_base_portefeuille = pd.read_excel(BASE_DIR / 'base_donnees/BasePortefeuille.xlsx')
    data_base_stock_Pf = pd.read_excel(BASE_DIR / 'base_donnees/BaseStockPF.xlsx')
    data_base_cde_fournisseur = pd.read_excel(BASE_DIR / 'base_donnees/BaseCommandeHA.xlsx')
    # connection à la base de données
    conn = sqlite3.connect(BASE_DIR / 'db.sqlite3')
    # Enregistrement des nouvelles données dans la base
    data_stock_global.to_sql('portefeuille_StockGobal',
                             con=conn, if_exists='replace', index_label='id', index=True)
    data_base_nomenclature.to_sql('portefeuille_BaseNomenclature',
                                  con=conn, if_exists='replace', index_label='id', index=True)
    data_base_operation.to_sql('portefeuille_BaseOperation', con=conn,
                               if_exists='replace', index_label='id', index=True)
    data_base_of.to_sql('portefeuille_BaseOF', con=conn,
                        if_exists='replace', index_label='id', index=True)
    data_base_portefeuille.to_sql('portefeuille_Portefeuille',
                                  con=conn, if_exists='replace', index_label='id', index=True)
    data_base_stock_Pf.to_sql('portefeuille_Stock',
                              con=conn, if_exists='replace', index_label='id', index=True)
    data_base_cde_fournisseur.to_sql('portefeuille_CommandeFournisseur',
                                     con=conn, if_exists='replace', index_label='id', index=True)
    # Commit de l'enregistrement
    conn.commit()
    # Fermeture de la connexion
    conn.close()

    return render(request, 'portefeuille/mise_a_jour.html')
