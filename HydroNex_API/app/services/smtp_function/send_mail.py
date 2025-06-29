from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

from app.commons.instances.instances import logger

class EmailService:
    def __init__(self):
        # Charger les informations SMTP à partir de l'environnement
        self.smtp_server = os.getenv('smtp_server')
        self.smtp_port = int(os.getenv('smtp_port', 587))
        self.smtp_user = os.getenv('smtp_user')
        self.smtp_password = os.getenv('smtp_password')
        self.logo_path = os.path.join(os.path.dirname(__file__), '../../static/images/logo/logo.png')

    def get_icon_for_type(self, email_type):
        """Retourne l'icône SVG appropriée selon le type d'email"""
        icons = {
            'welcome': '''
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" fill="#0119F2" opacity="0.1"/>
                    <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="#0119F2"/>
                </svg>
            ''',
            'alert': '''
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" fill="#DC3545" opacity="0.1"/>
                    <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="#DC3545"/>
                    <circle cx="12" cy="12" r="3" fill="#DC3545"/>
                </svg>
            ''',
            'admin_welcome': '''
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" fill="#0119F2" opacity="0.1"/>
                    <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="#0119F2"/>
                    <circle cx="12" cy="12" r="3" fill="#0119F2"/>
                    <path d="M12 1V3M12 21V23M4.22 4.22L5.64 5.64M18.36 18.36L19.78 19.78M1 12H3M21 12H23" stroke="#0119F2" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
            ''',
            'default': '''
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" fill="#0119F2" opacity="0.1"/>
                    <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="#0119F2"/>
                </svg>
            '''
        }
        return icons.get(email_type, icons['default'])

    def create_email_template(self, message: str, email_type: str = 'default', title: str = None) -> str:
        """Crée un template d'email avec un design élégant et noble"""
        icon = self.get_icon_for_type(email_type)
        
        return f"""
            <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{title or 'HydroNex'}</title>
                    <style>
                        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
                        
                        * {{
                            margin: 0;
                            padding: 0;
                            box-sizing: border-box;
                        }}
                        
                        body {{
                            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                            background-color: #F8FAFC;
                            color: #1E293B;
                            line-height: 1.6;
                            padding: 0;
                            margin: 0;
                        }}
                        
                        .email-wrapper {{
                            background-color: #F8FAFC;
                            padding: 40px 20px;
                        }}
                        
                        .email-container {{
                            max-width: 600px;
                            margin: 0 auto;
                            background-color: #FFFFFF;
                            border-radius: 16px;
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            overflow: hidden;
                        }}
                        
                        .header {{
                            background: linear-gradient(135deg, #003366 0%, #0119F2 100%);
                            padding: 48px 40px 40px;
                            text-align: center;
                            position: relative;
                        }}
                        
                        .header::after {{
                            content: '';
                            position: absolute;
                            bottom: 0;
                            left: 0;
                            right: 0;
                            height: 4px;
                            background: linear-gradient(90deg, #0119F2 0%, #00D4FF 50%, #0119F2 100%);
                        }}
                        
                        .logo {{
                            margin-bottom: 24px;
                        }}
                        
                        .logo img {{
                            width: 180px;
                            height: auto;
                            filter: brightness(0) invert(1);
                        }}
                        
                        .brand-name {{
                            color: #FFFFFF;
                            font-size: 32px;
                            font-weight: 700;
                            letter-spacing: -0.025em;
                            margin-bottom: 8px;
                        }}
                        
                        .brand-tagline {{
                            color: rgba(255, 255, 255, 0.9);
                            font-size: 16px;
                            font-weight: 400;
                            line-height: 1.5;
                        }}
                        
                        .content {{
                            padding: 48px 40px;
                            background-color: #FFFFFF;
                        }}
                        
                        .icon-section {{
                            text-align: center;
                            margin-bottom: 32px;
                            padding: 24px;
                        }}
                        
                        .icon-section svg {{
                            filter: drop-shadow(0 2px 4px rgba(1, 25, 242, 0.1));
                        }}
                        
                        .message-content {{
                            color: #1E293B;
                            font-size: 16px;
                            line-height: 1.7;
                        }}
                        
                        .message-content h1, .message-content h2, .message-content h3 {{
                            color: #0119F2;
                            margin-bottom: 16px;
                            font-weight: 600;
                            letter-spacing: -0.025em;
                        }}
                        
                        .message-content h2 {{
                            font-size: 24px;
                        }}
                        
                        .message-content h3 {{
                            font-size: 20px;
                        }}
                        
                        .message-content p {{
                            margin-bottom: 16px;
                            color: #475569;
                        }}
                        
                        .message-content strong {{
                            color: #1E293B;
                            font-weight: 600;
                        }}
                        
                        .info-card {{
                            background: linear-gradient(135deg, #F8FAFF 0%, #F1F5FF 100%);
                            border: 1px solid #E2E8F0;
                            border-radius: 12px;
                            padding: 24px;
                            margin: 24px 0;
                        }}
                        
                        .info-card h3 {{
                            color: #0119F2;
                            margin-bottom: 16px;
                            font-size: 18px;
                            font-weight: 600;
                        }}
                        
                        .info-card p {{
                            color: #475569;
                            margin-bottom: 8px;
                        }}
                        
                        .info-card ul {{
                            list-style: none;
                            padding: 0;
                        }}
                        
                        .info-card li {{
                            color: #475569;
                            margin-bottom: 8px;
                            padding-left: 20px;
                            position: relative;
                        }}
                        
                        .info-card li::before {{
                            content: '•';
                            color: #0119F2;
                            font-weight: bold;
                            position: absolute;
                            left: 0;
                        }}
                        
                        .alert-card {{
                            background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
                            border: 1px solid #FECACA;
                            border-radius: 12px;
                            padding: 24px;
                            margin: 24px 0;
                        }}
                        
                        .alert-card h3 {{
                            color: #DC2626;
                            margin-bottom: 16px;
                        }}
                        
                        .alert-card p {{
                            color: #7F1D1D;
                        }}
                        
                        .divider {{
                            height: 1px;
                            background: linear-gradient(90deg, transparent 0%, #E2E8F0 50%, transparent 100%);
                            margin: 32px 0;
                        }}
                        
                        .footer {{
                            background-color: #F8FAFC;
                            padding: 32px 40px;
                            text-align: center;
                            border-top: 1px solid #E2E8F0;
                        }}
                        
                        .footer-text {{
                            color: #64748B;
                            font-size: 14px;
                            margin-bottom: 8px;
                        }}
                        
                        .footer-links {{
                            margin-top: 16px;
                        }}
                        
                        .footer-links a {{
                            color: #0119F2;
                            text-decoration: none;
                            font-weight: 500;
                            margin: 0 12px;
                            font-size: 14px;
                        }}
                        
                        .footer-links a:hover {{
                            text-decoration: underline;
                        }}
                        
                        .water-accent {{
                            position: absolute;
                            bottom: 0;
                            left: 0;
                            right: 0;
                            height: 3px;
                            background: linear-gradient(90deg, #0119F2 0%, #00D4FF 25%, #0119F2 50%, #00D4FF 75%, #0119F2 100%);
                            opacity: 0.8;
                        }}
                        
                        @media (max-width: 640px) {{
                            .email-wrapper {{
                                padding: 20px 10px;
                            }}
                            
                            .header, .content, .footer {{
                                padding: 32px 24px;
                            }}
                            
                            .brand-name {{
                                font-size: 28px;
                            }}
                            
                            .message-content {{
                                font-size: 15px;
                            }}
                            
                            .info-card, .alert-card {{
                                padding: 20px;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-wrapper">
                        <div class="email-container">
                            <div class="header">
                                <div class="logo">
                                    <img src="cid:logo" alt="HydroNex">
                                </div>
                                <p class="brand-tagline">Surveillance intelligente de la qualité de l'eau et de la salinité dans les zones côtières</p>
                                <div class="water-accent"></div>
                            </div>
                            
                            <div class="content">
                                <div class="icon-section">
                                    {icon}
                                </div>
                                
                                <div class="message-content">
                                    {message}
                                </div>
                            </div>
                            
                            <div class="footer">
                                <p class="footer-text">© 2024 HydroNex. Tous droits réservés.</p>
                                <p class="footer-text">Solution de surveillance de la qualité de l'eau et de la salinité dans les zones côtières</p>
                                <div class="footer-links">
                                    <a href="#">Support</a>
                                    <a href="#">Documentation</a>
                                    <a href="#">Contact</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
        """

    def send_email(self, to_email: str, subject: str, message: str, email_type: str = 'default') -> bool:
        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.smtp_user
            msg['To'] = to_email

            # Créer le template HTML avec le design amélioré
            html_content = self.create_email_template(message, email_type, subject)
            msg.attach(MIMEText(html_content, 'html'))

            # Ajouter le logo si disponible
            if os.path.exists(self.logo_path):
                with open(self.logo_path, 'rb') as img:
                    logo = MIMEImage(img.read())
                    logo.add_header('Content-ID', '<logo>')
                    msg.attach(logo)

            # Envoyer l'e-mail via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, to_email, msg.as_string())
            
            logger.info(f"E-mail de type '{email_type}' envoyé avec succès à {to_email}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'e-mail: {str(e)}")
            return False

    def send_welcome_email(self, to_email: str, nom: str) -> bool:
        """Envoie un email de bienvenue personnalisé"""
        message = f"""
            <h2>Bienvenue {nom} !</h2>
            <p>Nous sommes ravis de vous accueillir dans la communauté HydroNex.</p>
            
            <div class="info-card">
                <h3>Découvrez les fonctionnalités d'HydroNex</h3>
                <ul>
                    <li>Surveillance en temps réel de la qualité de l'eau</li>
                    <li>Alertes automatiques en cas de valeurs critiques</li>
                    <li>Historique détaillé des données environnementales</li>
                    <li>Recommandations personnalisées basées sur l'IA</li>
                </ul>
            </div>
            
            <p>Vous recevrez désormais nos dernières actualités, mises à jour et alertes importantes directement dans votre boîte mail.</p>
            
            <div class="divider"></div>
            
            <p>Si vous avez des questions, notre équipe est là pour vous accompagner.</p>
            
            <p>Cordialement,<br><strong>L'équipe HydroNex</strong></p>
        """
        return self.send_email(to_email, "Bienvenue à la newsletter HydroNex", message, 'welcome')

    def send_alert_email(self, to_email: str, alerte_data: dict) -> bool:
        """Envoie un email d'alerte avec les détails"""
        message = f"""
            <h2>Alerte - Valeurs critiques détectées</h2>
            
            <div class="alert-card">
                <h3>Détails de l'alerte</h3>
                <p><strong>Localisation :</strong> {alerte_data.get('localisation', 'N/A')}</p>
                <p><strong>Température :</strong> {alerte_data.get('temperature', 'N/A')}°C</p>
                <p><strong>Salinité :</strong> {alerte_data.get('salinity', 'N/A')}</p>
                <p><strong>pH :</strong> {alerte_data.get('ph', 'N/A')}</p>
                <p><strong>Turbidité :</strong> {alerte_data.get('turbidity', 'N/A')}</p>
            </div>
            
            <div class="info-card">
                <h3>Recommandation</h3>
                <p>{alerte_data.get('recommandation', 'Veuillez vérifier le dispositif et ajuster les paramètres si nécessaire.')}</p>
            </div>
            
            <p>Cette alerte a été générée automatiquement par le système HydroNex. Veuillez prendre les mesures appropriées.</p>
            
            <div class="divider"></div>
            
            <p>Cordialement,<br><strong>L'équipe HydroNex</strong></p>
        """
        return self.send_email(to_email, "Alerte - Valeurs critiques détectées", message, 'alert')

    def send_admin_welcome_email(self, to_email: str, password: str) -> bool:
        """Envoie un email de bienvenue pour les administrateurs"""
        message = f"""
            <h2>Bienvenue dans l'équipe HydroNex</h2>
            
            <p>Félicitations ! Vous avez été ajouté comme administrateur de la plateforme HydroNex.</p>
            
            <div class="info-card">
                <h3>Vos identifiants de connexion</h3>
                <p><strong>Email :</strong> {to_email}</p>
                <p><strong>Mot de passe temporaire :</strong> {password}</p>
            </div>
            
            <div class="alert-card">
                <h3>Important</h3>
                <p>Veuillez changer votre mot de passe après votre première connexion pour des raisons de sécurité.</p>
            </div>
            
            <div class="info-card">
                <h3>Fonctionnalités administrateur</h3>
                <ul>
                    <li>Gestion complète des dispositifs</li>
                    <li>Surveillance avancée des données</li>
                    <li>Gestion des alertes et notifications</li>
                    <li>Configuration du système</li>
                </ul>
            </div>
            
            <div class="divider"></div>
            
            <p>Si vous avez des questions ou besoin d'assistance, n'hésitez pas à contacter l'équipe technique.</p>
            
            <p>Cordialement,<br><strong>L'équipe HydroNex</strong></p>
        """
        return self.send_email(to_email, "Vos identifiants HydroNex", message, 'admin_welcome')

