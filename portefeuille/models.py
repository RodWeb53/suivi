from django.db import models

# Create your models here.


class Stock(models.Model):
    produit = models.IntegerField(default=0, blank=True)
    nom = models.CharField(max_length=128, blank=True)
    stock = models.IntegerField(default=0, blank=True)
    emplacement = models.CharField(max_length=20, blank=True)
    stock_recalcule = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.produit} ({self.stock})"


class Portefeuille(models.Model):
    num_client = models.IntegerField(default=0, blank=True)
    num_cde = models.IntegerField(default=0, blank=True)
    num_ligne = models.IntegerField(default=0, blank=True)
    date_depart = models.DateField(blank=True)
    date_arrivee = models.DateField(blank=True)
    ferme_prev = models.CharField(max_length=1, blank=True)
    ref_commande = models.CharField(max_length=128, blank=True)
    num_appel = models.CharField(max_length=128, blank=True)
    poste = models.IntegerField(default=0, blank=True)
    produit = models.IntegerField(default=0, blank=True)
    ref_interne = models.CharField(max_length=128, blank=True)
    nom_produit = models.CharField(max_length=128, blank=True)
    quantite_cde = models.IntegerField(default=0, blank=True)
    prix_vente = models.FloatField(default=0.0, blank=True)
    num_unique = models.IntegerField(default=0, blank=True)
    nom_client = models.CharField(max_length=128, blank=True)
    montant_total = models.FloatField(default=0, blank=True)

    def __str__(self):
        return f"client : {self.num_client} (produit : {self.produit})"


class BaseOF(models.Model):
    num_of = models.IntegerField(default=0, blank=True)
    num_produit = models.IntegerField(default=0, blank=True)
    num_lancement = models.CharField(max_length=15, blank=True)
    statut_of = models.CharField(max_length=5, blank=True)
    date_debut = models.DateField(blank=True)
    date_fin = models.DateField(blank=True)
    quantite = models.IntegerField(default=0, blank=True)
    id_cde = models.IntegerField(default=0, blank=True)
    nbre_operation = models.IntegerField(default=0, blank=True)
    qte_base = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.num_produit} ({self.quantite}) ({self.num_of}) ({self.id_cde})"


class BaseOperation(models.Model):
    num_of_operation = models.IntegerField(default=0, blank=True)
    num_phase_operation = models.CharField(max_length=5, blank=True)
    num_operation = models.IntegerField(default=0, blank=True)
    phase = models.CharField(max_length=10, blank=True)
    atelier = models.CharField(max_length=10, blank=True)
    machine = models.CharField(max_length=10, blank=True)
    description_operation = models.CharField(max_length=50, blank=True)
    temps_prepa = models.FloatField(default=0.0, blank=True)
    temps_prod = models.FloatField(default=0.0, blank=True)
    temps_total = models.FloatField(default=0.0, blank=True)
    date_fab = models.DateField(blank=True)
    solder = models.BooleanField()
    num_unique = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.num_of_operation} ({self.machine}) ({self.solder}) ({self.temps_total})"


class BaseNomenclature(models.Model):
    num_of_nomenclature = models.IntegerField(default=0, blank=True)
    num_phase_nomenclature = models.CharField(max_length=5, blank=True)
    num_produit = models.IntegerField(default=0, blank=True)
    quantite_besoin = models.FloatField(default=0.0, blank=True)
    besoin_solder = models.BooleanField()
    designation_produit = models.CharField(max_length=50, blank=True)
    date_conso = models.DateField(blank=True)
    num_unique_nomenclature = models.CharField(max_length=50, blank=True)
    produit_gp = models.BooleanField()

    def __str__(self):
        return f"{self.num_of_nomenclature} ({self.num_produit}) ({self.designation_produit})"


class StockGobal(models.Model):
    produit_global = models.IntegerField(default=0, blank=True)
    nom_produit_stock = models.CharField(max_length=128, blank=True)
    stock_global = models.FloatField(default=0.0, blank=True)
    stock_recalcule_global = models.FloatField(default=0.0, blank=True)

    def __str__(self):
        return f"{self.produit_global} ({self.stock_global})"


class CommandeFournisseur(models.Model):
    fournisseur = models.CharField(max_length=80, blank=True)
    num_commande = models.IntegerField(default=0, blank=True)
    num_produit_achat = models.IntegerField(default=0, blank=True)
    date_liv_accorde = models.DateField(blank=True)
    num_ligne = models.IntegerField(default=0, blank=True)
    quantite_commande = models.FloatField(default=0.0, blank=True)
    reception = models.BooleanField()
    reference_cde = models.CharField(max_length=125, blank=True)
