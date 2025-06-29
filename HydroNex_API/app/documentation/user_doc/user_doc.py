update_user_doc = """
    Mise à jour des informations d'un utilisateur / Aussi utilisé pour éditer le profil d'un utilisateur.
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UpdateUser
          properties:
            email:
              type: string
              format: email
              description: Nouvelle adresse email de l'utilisateur
            first_name:
              type: string
              description: Nouveau prénom de l'utilisateur
            last_name:
              type: string
              description: Nouveau nom de famille de l'utilisateur
            sexe:
              type: string
              enum: [male, female]
              description: Sexe de l'utilisateur
            role:
              type: string
              enum: [student, professional, adult_learner, learners_motivated_by_challenge]
              description: Nouveau rôle attribué à l'utilisateur
            initial_level:
              type: string
              description: Nouveau niveau initial de l'utilisateur
            learning_objectives:
              type: array
              description: Nouveaux objectifs d'apprentissage de l'utilisateur
              items:
                type: string
                enum: [improve_speaking, improve_writing, professional_communication, academic_language, travel_communication]
    responses:
      200:
        description: Mise à jour effectuée avec succès
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: Identifiant unique de l'utilisateur
                first_name:
                  type: string
                  description: Prénom de l'utilisateur
                last_name:
                  type: string
                  description: Nom de famille de l'utilisateur
                email:
                  type: string
                  format: email
                  description: Adresse email de l'utilisateur
                role:
                  type: string
                  description: Rôle attribué à l'utilisateur
      400:
        description: Erreur de validation - Email indisponible ou mise à jour impossible
      500:
        description: Erreur serveur lors de la mise à jour du compte
"""


get_one_user_doc = """
    Retrieve the authenticated user's data.
    ---
    tags:
      - User
    responses:
      200:
        description: User data retrieved successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                email:
                  type: string
                  format: email
                name:
                  type: string
                # Add any other relevant fields here
            example:
              id: 1
              email: "johndoe@example.com"
              name: "John Doe"
      404:
        description: User not found.
      500:
        description: Error while retrieving user data.
    """


forgot_password_doc = """
    Demande de lien de réinitialisation de mot de passe.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              format: email
              description: Adresse email de l'utilisateur
    responses:
      200:
        description: Code de réinitialisation envoyé avec succès
      400:
        description: L'e-mail est requis ou utilisateur introuvable
      500:
        description: Erreur serveur
    """


change_password_doc = """
    Changement de mot de passe utilisateur.
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            old_password:
              type: string
              description: Ancien mot de passe
            new_password:
              type: string
              description: Nouveau mot de passe
    responses:
      200:
        description: Mot de passe mis à jour avec succès
      400:
        description: Ancien mot de passe incorrect ou données manquantes
      500:
        description: Erreur serveur
    """


reset_password_doc = """
    Réinitialisation du mot de passe avec un code.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            reset_code:
              type: string
              description: Code de réinitialisation envoyé par email
            new_password:
              type: string
              description: Nouveau mot de passe
    responses:
      200:
        description: Mot de passe mis à jour avec succès
      400:
        description: Code de réinitialisation invalide ou données manquantes
      500:
        description: Erreur serveur
    """


delete_my_account_doc = """
    Suppression du compte utilisateur.
    ---
    tags:
      - User
    responses:
      200:
        description: Compte utilisateur supprimé avec succès
      404:
        description: Utilisateur introuvable
      500:
        description: Erreur serveur
    """


verify_user_account_doc = """
    Vérification du compte utilisateur via un code envoyé par email.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              format: email
              description: Adresse email de l'utilisateur
            verification_code:
              type: string
              description: Code de vérification reçu par email
    responses:
      200:
        description: Compte vérifié avec succès
      400:
        description: Code de vérification incorrect ou données manquantes
      404:
        description: Utilisateur non trouvé
      500:
        description: Erreur serveur
    """


resent_verification_code_doc = """
    Renvoi du code de vérification utilisateur.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              format: email
              description: Adresse email de l'utilisateur
    responses:
      200:
        description: Nouveau code de vérification envoyé avec succès
      400:
        description: Email non fourni ou données manquantes
      404:
        description: Utilisateur non trouvé
      500:
        description: Erreur lors de l'envoi du code ou erreur serveur
    """


resent_user_verification_link_doc = """
    Renvoi du lien de vérification utilisateur.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              format: email
              description: Adresse email de l'utilisateur
    responses:
      200:
        description: Lien de vérification envoyé avec succès
      400:
        description: Email non fourni ou données manquantes
      404:
        description: Utilisateur non trouvé ou compte déjà vérifié
      500:
        description: Erreur serveur
    """


get_joined_competitions_by_participant_doc = """
    Récupère les compétitions auxquelles l'utilisateur connecté participe.
    ---
    tags:
      - User
    parameters:
      - name: page
        in: query
        required: false
        type: integer
        description: Numéro de page pour la pagination
        default: 1
      - name: per_page
        in: query
        required: false
        type: integer
        description: Nombre d'éléments par page pour la pagination
        default: 10
    responses:
      200:
        description: Compétitions récupérées avec succès.
      500:
        description: Erreur serveur lors de la récupération des compétitions
"""


get_organized_competitions_by_participant_doc = """
    Récupère les compétitions organisées par l'utilisateur connecté.
    ---
    tags:
      - User
    parameters:
      - name: page
        in: query
        required: false
        type: integer
        description: Numéro de page pour la pagination
        default: 1
      - name: per_page
        in: query
        required: false
        type: integer
        default: 10
        description: Nombre d'éléments par page pour la pagination
    responses:
      200:
        description: Compétitions récupérées avec succès.
      500:
        description: Erreur serveur lors de la récupération des compétitions
"""

get_joined_groups_by_participant_doc = """
    Récupère les groupes dont l'utilisateur connecté est membre.
    ---
    tags:
      - User
    parameters:
      - name: page
        in: query
        required: false
        type: integer
        description: Numéro de page pour la pagination
        default: 1
      - name: per_page
        in: query
        required: false
        type: integer
        description: Nombre d'éléments par page pour la pagination
        default: 10
    responses:
      200:
        description: Groupes récupérés avec succès.
      500:
        description: Erreur serveur lors de la récupération des groupes
"""

get_owned_groups_by_participant_doc = """
    Récupère les groupes créés par l'utilisateur connecté.
    ---
    tags:
      - User
    parameters:
      - name: page
        in: query
        required: false
        type: integer
        description: Numéro de page pour la pagination
        default: 1
      - name: per_page
        in: query
        required: false
        type: integer
        description: Nombre d'éléments par page pour la pagination
        default: 10
    responses:
      200:
        description: Groupes récupérés avec succès.
      500:
        description: Erreur serveur lors de la récupération des groupes
"""