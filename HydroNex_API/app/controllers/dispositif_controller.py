from flask import request
from app.commons.response.custom_response import CustomResponse
from app.adaptater.dispositif.dispositif_adaptater import DispositifAdaptater
from app.commons.decorators.auth_decorator import token_required

@token_required
def create_dispositif():
    try:
        data = request.get_json()
        
        # Vérifier les champs requis
        required_fields = ['nom', 'localisation', 'statut']
        for field in required_fields:
            if field not in data:
                return CustomResponse.error(f"Le champ {field} est requis", 400)
        
        # Vérifier si le statut est valide
        if data['statut'] not in ['actif', 'inactif']:
            return CustomResponse.error("Le statut doit être 'actif' ou 'inactif'", 400)
        
        # Vérifier si le nom existe déjà
        if DispositifAdaptater.check_nom_exists(data.get('nom')):
            return CustomResponse.error("Un dispositif avec ce nom existe déjà", 400)
        
        # Vérifier si la localisation existe déjà
        if DispositifAdaptater.check_localisation_exists(data.get('localisation')):
            return CustomResponse.error("Un dispositif existe déjà à cette localisation", 400)
        
        # Créer le dispositif
        dispositif = DispositifAdaptater.create_dispositif(data)
        if not dispositif:
            return CustomResponse.error("Erreur lors de la création du dispositif", 500)
        
        return CustomResponse.success("Dispositif créé avec succès", dispositif.to_dict())
    except Exception as e:
        return CustomResponse.error(str(e), 500)

@token_required
def update_dispositif(dispositif_id):
    try:
        data = request.get_json()
        
        # Vérifier si le dispositif existe
        dispositif = DispositifAdaptater.get_dispositif_by_id(dispositif_id)
        if not dispositif:
            return CustomResponse.error("Dispositif non trouvé", 404)
        
        # Vérifier si le nouveau nom existe déjà (si modifié)
        if data.get('nom') and data['nom'] != dispositif.nom:
            if DispositifAdaptater.check_nom_exists(data['nom']):
                return CustomResponse.error("Un dispositif avec ce nom existe déjà", 400)
        
        # Vérifier si la nouvelle localisation existe déjà (si modifiée)
        if data.get('localisation') and data['localisation'] != dispositif.localisation:
            if DispositifAdaptater.check_localisation_exists(data['localisation']):
                return CustomResponse.error("Un dispositif existe déjà à cette localisation", 400)
        
        # Mettre à jour le dispositif
        updated_dispositif = DispositifAdaptater.update_dispositif(dispositif_id, data)
        if not updated_dispositif:
            return CustomResponse.error("Erreur lors de la mise à jour du dispositif", 500)
        
        return CustomResponse.success("Dispositif mis à jour avec succès", updated_dispositif.to_dict())
    except Exception as e:
        return CustomResponse.error(str(e), 500)

def get_dispositifs():
    try:
        dispositifs = DispositifAdaptater.get_all_dispositifs()
        if not dispositifs:
            return CustomResponse.error("Aucun dispositif trouvé", 404)
        
        return CustomResponse.success(
            "Dispositifs récupérés avec succès",
            [d.to_dict() for d in dispositifs]
        )
    except Exception as e:
        return CustomResponse.error(str(e), 500)

def get_dispositif(dispositif_id):
    try:
        dispositif = DispositifAdaptater.get_dispositif_by_id(dispositif_id)
        if not dispositif:
            return CustomResponse.error("Dispositif non trouvé", 404)
        
        return CustomResponse.success("Dispositif récupéré avec succès", dispositif.to_dict())
    except Exception as e:
        return CustomResponse.error(str(e), 500) 