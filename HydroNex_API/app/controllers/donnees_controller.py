from flask import request
from app.commons.response.custom_response import CustomResponse
from app.adaptater.donnees.donnees_adaptater import DonneesAdaptater
from app.adaptater.dispositif.dispositif_adaptater import DispositifAdaptater
from app.adaptater.newsletter.newsletter_adaptater import NewsletterAdaptater
from app.adaptater.alerte_recommandation.alerte_recommandation_adaptater import AlerteRecommandationAdaptater
from app.services.smtp_function.send_mail import EmailService
from app.commons.instances.instances import logger

def create_donnees():
    try:
        data = request.get_json()
        
        # Vérifier les champs requis
        dispositif_id = data.get('dispositif_id')
        if not dispositif_id:
            return CustomResponse.error("ID du dispositif requis", 400)

        # Récupérer les informations du dispositif
        dispositif = DispositifAdaptater.get_dispositif_by_id(dispositif_id)
        if not dispositif:
            return CustomResponse.error("Dispositif non trouvé", 404)
        
        # Créer les données
        donnees = DonneesAdaptater.create_donnees(data)
        if not donnees:
            return CustomResponse.error("Erreur lors de la création des données", 500)
        
        # Vérifier les seuils critiques et créer une alerte si nécessaire
        alerte = None
        if data.get('temperature', 0) > 30 or data.get('salinity', 0) > 40:
            # Créer l'alerte
            alerte_data = {
                'dispositif_id': dispositif_id,
                'alerte': f"Valeurs critiques détectées - Température: {data.get('temperature')}°C, Salinité: {data.get('salinity')}",
                'recommandation': "Veuillez vérifier le dispositif et ajuster les paramètres si nécessaire."
            }
            alerte = AlerteRecommandationAdaptater.create_alerte(alerte_data)
            
            # Préparer les données pour l'email d'alerte
            email_alerte_data = {
                'localisation': dispositif.localisation if hasattr(dispositif, 'localisation') else 'N/A',
                'temperature': data.get('temperature'),
                'salinity': data.get('salinity'),
                'ph': data.get('ph'),
                'turbidity': data.get('turbidity'),
                'recommandation': alerte_data['recommandation']
            }
            
            # Envoyer un email à tous les abonnés avec le nouveau design
            email_service = EmailService()
            emails = NewsletterAdaptater.get_all_emails()
            if emails:
                for email in emails:
                    if not email_service.send_alert_email(email, email_alerte_data):
                        logger.warning(f"Impossible d'envoyer l'email d'alerte à {email}")
            else:
                logger.warning("Aucun email trouvé dans la newsletter")
        
        response_data = donnees.to_dict()
        if alerte:
            response_data['alerte'] = alerte.to_dict()
        
        return CustomResponse.success("Données créées avec succès", response_data)
    except Exception as e:
        logger.error(f"Erreur lors de la création des données: {str(e)}")
        return CustomResponse.error(str(e), 500)

def get_temps_reel():
    try:
        dispositif_id = request.args.get('dispositif_id')
        if not dispositif_id:
            return CustomResponse.error("ID du dispositif requis", 400)
        
        donnees = DonneesAdaptater.get_donnees_by_dispositif(dispositif_id)
        if not donnees:
            return CustomResponse.error("Aucune donnée trouvée", 404)
        
        return CustomResponse.success("Données récupérées avec succès", donnees.to_dict())
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données en temps réel: {str(e)}")
        return CustomResponse.error(str(e), 500)

def get_historique():
    try:
        dispositif_id = request.args.get('dispositif_id')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        if not dispositif_id:
            return CustomResponse.error("ID du dispositif requis", 400)
        
        donnees = DonneesAdaptater.get_historique_donnees(
            page=page,
            per_page=per_page,
            dispositif_id=dispositif_id
        )
        if not donnees:
            return CustomResponse.error("Aucune donnée trouvée", 404)
        
        # Formater les résultats
        resultats = {
            'data': [d.to_dict() for d in donnees.items],
            'total': donnees.total,
            'page': page,
            'per_page': per_page
        }
        
        return CustomResponse.success("Historique récupéré avec succès", resultats)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'historique: {str(e)}")
        return CustomResponse.error(str(e), 500) 