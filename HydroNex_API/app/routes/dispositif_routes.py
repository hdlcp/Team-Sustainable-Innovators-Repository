from flask import Blueprint
from app.controllers.dispositif_controller import (
    create_dispositif,
    update_dispositif,
    get_dispositifs,
    get_dispositif,
    token_required
)

dispositif_bp = Blueprint('dispositif', __name__)

@dispositif_bp.route('/dispositifs', methods=['POST'])
@token_required
def create_dispositif_route():
    """
    Créer un nouveau dispositif
    ---
    tags:
      - Dispositifs
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nom
            - localisation
            - statut
          properties:
            nom:
              type: string
              description: Nom du dispositif
            localisation:
              type: string
              description: Localisation du dispositif
            statut:
              type: string
              enum: [actif, inactif]
              description: Statut du dispositif
    responses:
      201:
        description: Dispositif créé avec succès
      400:
        description: Données invalides ou nom/localisation déjà utilisé
      401:
        description: Non autorisé
      500:
        description: Erreur serveur
    """
    return create_dispositif()

@dispositif_bp.route('/dispositifs/<int:dispositif_id>', methods=['PUT'])
@token_required
def update_dispositif_route(dispositif_id):
    """
    Mettre à jour un dispositif
    ---
    tags:
      - Dispositifs
    security:
      - Bearer: []
    parameters:
      - in: path
        name: dispositif_id
        type: integer
        required: true
        description: ID du dispositif
      - in: body
        name: body
        schema:
          type: object
          properties:
            nom:
              type: string
              description: Nouveau nom du dispositif
            localisation:
              type: string
              description: Nouvelle localisation du dispositif
            statut:
              type: string
              enum: [actif, inactif]
              description: Nouveau statut du dispositif
    responses:
      200:
        description: Dispositif mis à jour avec succès
      400:
        description: Données invalides ou nom/localisation déjà utilisé
      401:
        description: Non autorisé
      404:
        description: Dispositif non trouvé
      500:
        description: Erreur serveur
    """
    return update_dispositif(dispositif_id)

@dispositif_bp.route('/dispositifs', methods=['GET'])
def get_dispositifs_route():
    """
    Obtenir la liste des dispositifs
    ---
    tags:
      - Dispositifs
    responses:
      200:
        description: Liste des dispositifs récupérée avec succès
      404:
        description: Aucun dispositif trouvé
      500:
        description: Erreur serveur
    """
    return get_dispositifs()

@dispositif_bp.route('/dispositifs/<int:dispositif_id>', methods=['GET'])
def get_dispositif_route(dispositif_id):
    """
    Obtenir les détails d'un dispositif
    ---
    tags:
      - Dispositifs
    parameters:
      - in: path
        name: dispositif_id
        type: integer
        required: true
        description: ID du dispositif
    responses:
      200:
        description: Détails du dispositif récupérés avec succès
      404:
        description: Dispositif non trouvé
      500:
        description: Erreur serveur
    """
    return get_dispositif(dispositif_id) 