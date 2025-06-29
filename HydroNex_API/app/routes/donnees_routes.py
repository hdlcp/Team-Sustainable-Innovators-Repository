from flask import Blueprint
from app.controllers.donnees_controller import create_donnees, get_temps_reel, get_historique

donnees_bp = Blueprint('donnees', __name__)

@donnees_bp.route('/donnees', methods=['POST'])
def create_donnees_route():
    """
    Créer une nouvelle entrée de données
    ---
    tags:
      - Données
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - dispositif_id
            - temperature
            - salinity
            - ph
            - turbidity
            - battery_level
          properties:
            dispositif_id:
              type: integer
              description: ID du dispositif
            temperature:
              type: number
              description: Température de l'eau en °C
            salinity:
              type: number
              description: Salinité de l'eau en ppt
            ph:
              type: number
              description: pH de l'eau
            turbidity:
              type: number
              description: Turbidité de l'eau en NTU
            battery_level:
              type: number
              description: Niveau de batterie en pourcentage
    responses:
      201:
        description: Données créées avec succès
      400:
        description: Données invalides
      404:
        description: Dispositif non trouvé
      500:
        description: Erreur serveur
    """
    return create_donnees()

@donnees_bp.route('/donnees/temps-reel', methods=['GET'])
def get_temps_reel_route():
    """
    Obtenir les données en temps réel
    ---
    tags:
      - Données
    parameters:
      - in: query
        name: dispositif_id
        type: integer
        required: true
        description: ID du dispositif
    responses:
      200:
        description: Données récupérées avec succès
      400:
        description: ID du dispositif requis
      404:
        description: Aucune donnée trouvée
      500:
        description: Erreur serveur
    """
    return get_temps_reel()

@donnees_bp.route('/donnees/historique', methods=['GET'])
def get_historique_route():
    """
    Obtenir l'historique des données
    ---
    tags:
      - Données
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
        description: Numéro de la page
      - in: query
        name: per_page
        type: integer
        default: 10
        description: Nombre d'éléments par page
      - in: query
        name: dispositif_id
        type: integer
        description: ID du dispositif (optionnel)
      - in: query
        name: date_debut
        type: string
        format: date-time
        description: Date de début (optionnel)
      - in: query
        name: date_fin
        type: string
        format: date-time
        description: Date de fin (optionnel)
    responses:
      200:
        description: Données historiques récupérées avec succès
      404:
        description: Aucune donnée trouvée
      500:
        description: Erreur serveur
    """
    return get_historique() 