from services.smtp_function.send_mail import EmailService
from adaptater.user.user_adaptater import UserAdaptater
from adaptater.group.group_adaptater import GroupAdaptater
from adaptater.assessment.assessment_adaptater import AssessmentAdaptater
from adaptater.competition.competition_adaptater import CompetitionAdaptater
from adaptater.competition_participant.competition_participant_adaptater import CompetitionParticipantAdaptater
from data.entities.user.user import User
from data.entities.competition.competition.competition import Competition
from commons.enums.competition_status.status import CompetitionStatus
from commons.utils.utils import to_utc_human_readable
from commons.const.string.app_string import AppString
from jinja2 import Template
from adaptater.progression.progression_adaptater import ProgressionAdaptater
from adaptater.module_formation.module_formation_adaptater import ModuleFormationAdaptater

email_service = EmailService()

class SendMail:
    @staticmethod
    def send_one_mail(app, email, subject, mail_message):
        with app.app_context():
            email_service.send_email(email, subject, message=mail_message)


    @staticmethod
    def send_group_message_emails(app, group_id: int, user_id: int):
        with app.app_context():
            user = UserAdaptater.get_user_by_id(user_id)
            group = GroupAdaptater.get_group_by_id(group_id)

            subject = f"Nouveau message dans le groupe {group.name}"
            message = f"Bonjour,<br/><br/>{user.first_name} {user.last_name} vient d'envoyer un message dans le groupe \"<b>{group.name}</b>\".<br/><br/>Merci de vérifier votre messagerie."
            # getting participants from group
            participants = group.participants + [group.owner]
            for participant in participants:
                if participant != user:
                    # send message to each participant
                    email_service.send_email(participant.email, subject, message)


    @staticmethod
    def send_group_delete_emails(app, group_id: int, user_id: int):
        with app.app_context():
            group = GroupAdaptater.get_deleted_group_by_id(group_id)
    
            subject = f"Groupe {group.name}"
            message = f"Bonjour,<br/><br/>Ce groupe a été supprimé."
            # getting participants from group
            participants = group.participants + [group.owner]
            for participant in participants:
                if participant.id != user_id:
                    # send message to each participant
                    email_service.send_email(participant.email, subject, message)


    @staticmethod
    def send_competition_invitation_email(app, competition: Competition, invitee: User):
        with app.app_context():
            organizer = UserAdaptater.get_user_by_id(competition.organizer_id)
            assessment = AssessmentAdaptater.get_assessment_by_id(competition.assessment_id)

            subject = f"Competition \"{competition.name}\" | Invitation"
            message = f"Bonjour,<br/><br/>{organizer.first_name} {organizer.last_name} vous invite à rejoindre la compétition \"<b>{competition.name}</b>\", de type {assessment.type.replace("_", " ").upper()} et qui s'étend du {to_utc_human_readable(competition.start_date_time)} au {to_utc_human_readable(competition.end_date_time)}.<br/><br/>Merci de bien vouloir la joindre en cliquant ce <a href='{AppString.front_join_competition_url}{competition.id}'>lien</a> afin de vous challenger et de rivaliser avec d'autres utilisateurs de la plateforme."
            # send invitation to user
            email_service.send_email(invitee.email, subject, message)


    @staticmethod
    def subscribe_and_send_competition_entrance_emails(app, competition: Competition, organizer_group_id: int):
        with app.app_context():
            organizer = UserAdaptater.get_user_by_id(competition.organizer_id)
            assessment = AssessmentAdaptater.get_assessment_by_id(competition.assessment_id)
            group_participants = GroupAdaptater.get_participants_by_group_id(organizer_group_id)

            subject = f"Competition {competition.name}"
            message = f"Bonjour,<br/><br/>Vous avez été ajouté(e) à la compétition de groupe \"<b>{competition.name}</b>\", de type {assessment.type.replace("_", " ").upper()}, organisée par {organizer.first_name} {organizer.last_name}, et qui s'étend du {to_utc_human_readable(competition.start_date_time)} au {to_utc_human_readable(competition.end_date_time)}.<br/><br/>Merci de bien vouloir vous préparer afin d'affronter les défis qui vous seront présenter."
            # getting participants from organizer's group
            for participant in group_participants:
                # subscribe each participant to the competition
                if CompetitionParticipantAdaptater.add_participant_to_competition(
                    data = {"competition_id": competition.id, "user_id": participant.id}
                ):
                    # send message to each participant
                    email_service.send_email(participant.email, subject, message)


    @staticmethod
    def send_competition_status_update_emails(app, competition_id: int):
        with app.app_context():
            competition = CompetitionAdaptater.get_competition_by_id(competition_id)

            subject = f"Competition {competition.name}"
            message = f"Bonjour,<br/><br/>La compétition \"<b>{competition.name}</b>\" a été {'annulée' if competition.status == CompetitionStatus.CANCELLED.value else 'reportée au '+to_utc_human_readable(competition.start_date_time)+' et prendra fin le '+to_utc_human_readable(competition.end_date_time)}."
            # getting participants from organizer's group
            for participant in competition.friendly_participants:
                # send message to each participant
                email_service.send_email(participant.email, subject, message)


    @staticmethod
    def send_competition_assessment_email(app, competition_name, competition_id, user_id, submitted_answers, assessment_result, submitted_date_time):
        with app.app_context():
            user = UserAdaptater.get_user_by_id(user_id)
            _, competition_participant = CompetitionParticipantAdaptater.check_user_already_joined_competition(user_id=user_id, competition_id=competition_id)
           
            # save those metrics into database
            data = {"score": assessment_result["score"].split("%")[0], "submitted_answers": submitted_answers, "appreciation": assessment_result["appreciation"], "areas_of_improvement": assessment_result["axes_d_amelioration"], "submitted_at": submitted_date_time}
            updated_competition_participant = CompetitionParticipantAdaptater.save_evaluation_response(competition_participant, data)

            if updated_competition_participant:
                subject = f"Competition {competition_name} | Résultats"
                
                html_template = """
                <h1>Résultats du Challenge</h1>

                <div class="section">
                    <h2>Score : {{ score }}</h2>
                    <p><strong>Appréciation :</strong> {{ appreciation }}</p>
                    <p><strong>Axes d'amélioration :</strong> {{ areas_of_improvement }}</p>
                </div>

                <div class="section">
                    <h2>Défi proposé</h2>
                    {% for question in questionnaire %}
                        <div class="question">
                            <p><strong>Question {{ question.number }}:</strong> {{ question.statement }}</p>
                            {% if question.type == "qcm" %}
                                <div class="choices">
                                    <strong>Choix possibles :</strong>
                                    <ul>
                                        {% for choice in question.choices %}
                                            <li>{{ choice }}</li>
                                        {% endfor %}
                                    </ul>
                                </div>
                            {% elif question.type == "association" %}
                                <div class="choices">
                                    <strong>Associez les éléments :</strong>
                                    <table>
                                        <tr>
                                            <th>Gauche</th>
                                            <th>Droite</th>
                                        </tr>
                                        {% for choice in question.choices %}
                                            <tr>
                                                <td>{{ choice.left }}</td>
                                                <td>
                                                    <ul>
                                                        {% for right_option in choice.right_options %}
                                                            <li>{{ right_option }}</li>
                                                        {% endfor %}
                                                    </ul>
                                                </td>
                                            </tr>
                                        {% endfor %}
                                    </table>
                                </div>
                            {% endif %}
                        </div>
                    {% endfor %}
                </div>

                <div class="section">
                    <h2>Réponses soumises par l'utilisateur</h2>
                    <table class="answers-table">
                        <thead>
                            <tr>
                                <th>Question</th>
                                <th>Réponse soumise</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for useract in submitted_answers %}
                                <tr>
                                    <td>{{ useract.number }}</td>
                                    <td>{{ useract.user_answer }}</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <div class="section">
                    <h2>Essai de correction</h2>
                    <table class="answers-table">
                        <thead>
                            <tr>
                                <th>Question</th>
                                <th>Réponse proposée</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for question in questionnaire %}
                                <tr>
                                    <td>{{ question.statement }}</td>
                                    <td>
                                        {% if question.type == "qcm" %}
                                            {% if question.answer is iterable and question.answer is not string %}
                                                <ul>
                                                    {% for item in question.answer %}
                                                        <li>{{ item }}</li>
                                                    {% endfor %}
                                                </ul>
                                            {% else %}
                                                {{ question.answer }}
                                            {% endif %}
                                        {% elif question.type == "association" %}
                                            <table style="border: 1px solid #ccc; border-collapse: collapse;">
                                                <tr>
                                                    <th style="border: 1px solid #ccc; padding: 5px;">Élément gauche</th>
                                                    <th style="border: 1px solid #ccc; padding: 5px;">Élément associé</th>
                                                </tr>
                                                {% for pair in question.answer %}
                                                    <tr>
                                                        <td style="border: 1px solid #ccc; padding: 5px;">{{ pair.left }}</td>
                                                        <td style="border: 1px solid #ccc; padding: 5px;">{{ pair.right }}</td>
                                                    </tr>
                                                {% endfor %}
                                            </table>
                                        {% else %}
                                            {{ question.answer }}
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                """

                # Créer un objet Template Jinja2 et le remplir avec les données
                template = Template(html_template)
                mail_message = template.render(
                    questionnaire=AssessmentAdaptater.get_assessment_by_competition_id(competition_id).questionary,
                    **data
                )

                email_service.send_email(user.email, subject, message=mail_message)
                
                
    @staticmethod
    def send_module_formation_email(app, module_name, module_id, user_id, time_spent, new_status, submitted_answers, assessment_result, submitted_date_time):
        with app.app_context():
            user = UserAdaptater.get_user_by_id(user_id)
            progression = ProgressionAdaptater.get_existing_progression(module_id, user_id)
           
            # save those metrics into database
            progression_data = {"final_score": assessment_result["score"].split("%")[0],"time_spent": time_spent,"status": new_status, "submitted_answers": submitted_answers, "appreciation": assessment_result["appreciation"], "areas_of_improvement": assessment_result["axes_d_amelioration"], "submitted_at": submitted_date_time}
            print(progression_data)            
            updated_progression_module_participant = ProgressionAdaptater.update_progression(progression, progression_data)

            if updated_progression_module_participant :
                subject = f"Module {module_name} | Résultats"
                
                html_template = """
                <h1>Résultats du Challenge</h1>

                <div class="section">
                    <h2>Score : {{final_score}}</h2>
                    <p><strong>Appréciation :</strong> {{ appreciation }}</p>
                    <p><strong>Axes d'amélioration :</strong> {{ areas_of_improvement }}</p>
                </div>

                <div class="section">
                    <h2>Défi proposé</h2>
                    {% for question in questionnaire %}
                        <div class="question">
                            <p><strong>Question {{ question.number }}:</strong> {{ question.statement }}</p>
                            {% if question.type == "qcm" %}
                                <div class="choices">
                                    <strong>Choix possibles :</strong>
                                    <ul>
                                        {% for choice in question.choices %}
                                            <li>{{ choice }}</li>
                                        {% endfor %}
                                    </ul>
                                </div>
                            {% elif question.type == "association" %}
                                <div class="choices">
                                    <strong>Associez les éléments :</strong>
                                    <table>
                                        <tr>
                                            <th>Gauche</th>
                                            <th>Droite</th>
                                        </tr>
                                        {% for choice in question.choices %}
                                            <tr>
                                                <td>{{ choice.left }}</td>
                                                <td>
                                                    <ul>
                                                        {% for right_option in choice.right_options %}
                                                            <li>{{ right_option }}</li>
                                                        {% endfor %}
                                                    </ul>
                                                </td>
                                            </tr>
                                        {% endfor %}
                                    </table>
                                </div>
                            {% endif %}
                        </div>
                    {% endfor %}
                </div>

                <div class="section">
                    <h2>Réponses soumises par l'utilisateur</h2>
                    <table class="answers-table">
                        <thead>
                            <tr>
                                <th>Question</th>
                                <th>Réponse soumise</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for useract in submitted_answers %}
                                <tr>
                                    <td>{{ useract.number }}</td>
                                    <td>{{ useract.user_answer }}</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <div class="section">
                    <h2>Essai de correction</h2>
                    <table class="answers-table">
                        <thead>
                            <tr>
                                <th>Question</th>
                                <th>Réponse proposée</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for question in questionnaire %}
                                <tr>
                                    <td>{{ question.statement }}</td>
                                    <td>
                                        {% if question.type == "qcm" %}
                                            {% if question.answer is iterable and question.answer is not string %}
                                                <ul>
                                                    {% for item in question.answer %}
                                                        <li>{{ item }}</li>
                                                    {% endfor %}
                                                </ul>
                                            {% else %}
                                                {{ question.answer }}
                                            {% endif %}
                                        {% elif question.type == "association" %}
                                            <table style="border: 1px solid #ccc; border-collapse: collapse;">
                                                <tr>
                                                    <th style="border: 1px solid #ccc; padding: 5px;">Élément gauche</th>
                                                    <th style="border: 1px solid #ccc; padding: 5px;">Élément associé</th>
                                                </tr>
                                                {% for pair in question.answer %}
                                                    <tr>
                                                        <td style="border: 1px solid #ccc; padding: 5px;">{{ pair.left }}</td>
                                                        <td style="border: 1px solid #ccc; padding: 5px;">{{ pair.right }}</td>
                                                    </tr>
                                                {% endfor %}
                                            </table>
                                        {% else %}
                                            {{ question.answer }}
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                """

                # Créer un objet Template Jinja2 et le remplir avec les données
                template = Template(html_template)
                mail_message = template.render(
                    questionnaire=ModuleFormationAdaptater.get_module_by_id(module_id).questionnaire,
                    **progression_data
                )

                email_service.send_email(user.email, subject, message=mail_message)
