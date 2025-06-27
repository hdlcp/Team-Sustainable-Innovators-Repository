import { HelpCircle } from "lucide-react";

export default function Support() {
  return (
    <div className="p-8 bg-gray-50 min-h-screen text-gray-800">
      <h1 className="text-3xl font-bold mb-6 text-black">Support - À propos de HydroNex</h1>

      {/* Présentation de la plateforme */}
      <section className="mb-10">
        <h2 className="text-xl font-semibold mb-4 text-blue-600 flex items-center gap-2">
          <HelpCircle className="w-6 h-6" />
          Qu'est-ce que HydroNex ?
        </h2>
        <p className="text-gray-700 leading-relaxed text-sm">
          <strong>HydroNex</strong> est une solution IoT flottante innovante conçue pour la
          <strong> surveillance en temps réel de la qualité de l’eau et de la salinité côtière</strong>.
          Elle combine des dispositifs IoT autonomes, un tableau de bord interactif, un système d’alerte
          intelligent, une newsletter automatisée et un assistant virtuel baptisé <strong>HydroBot</strong>.
        </p>
      </section>

      {/* Fonctionnement */}
      <section className="mb-10">
        <h2 className="text-xl font-semibold mb-4 text-blue-600">
          Comment fonctionne HydroNex ?
        </h2>
        <ul className="list-disc pl-6 text-gray-700 space-y-3 text-sm">
          <li>
            🌊 <strong>Capteurs IoT flottants :</strong> installés sur l’eau, ces dispositifs mesurent
            en continu des paramètres clés tels que la température, la turbidité, le pH, l’oxygène
            dissous, et la salinité.
          </li>
          <li>
            ☁️ <strong>Transmission des données :</strong> les données sont transmises via réseau (Wi-Fi)
            vers la plateforme centrale.
          </li>
          <li>
            📊 <strong>Tableau de bord interactif :</strong> accessible depuis n’importe quel navigateur,
            il permet de visualiser les données en temps réel, analyser les tendances, et comparer
            différents sites.
          </li>
          <li>
            🚨 <strong>Système d’alerte intelligent :</strong> lorsqu’un seuil critique est dépassé (ex. salinité élevée),
            une alerte est générée avec une recommandation automatique.
          </li>
          <li>
            📨 <strong>Newsletter automatisée :</strong> un récapitulatif régulier est envoyé par email avec les
            dernières données, alertes et recommandations.
          </li>
          <li>
            🤖 <strong>HydroBot :</strong> un assistant virtuel intégré pour poser des questions, demander des conseils
            et obtenir rapidement des résumés des données.
          </li>
        </ul>
      </section>

      {/* Objectifs et avantages */}
      <section className="mb-10">
        <h2 className="text-xl font-semibold mb-4 text-blue-600">
          Pourquoi utiliser HydroNex ?
        </h2>
        <ul className="list-disc pl-6 text-gray-700 space-y-2 text-sm">
          <li>Améliorer la gestion durable des ressources en eau.</li>
          <li>Prendre des décisions rapides et basées sur des données fiables.</li>
          <li>Prévenir la pollution de l’eau et les risques environnementaux.</li>
          <li>Faciliter le suivi de plusieurs sites en simultané.</li>
          <li>Simplifier l’accès à l’information pour les acteurs locaux et les décideurs.</li>
        </ul>
      </section>

      {/* Contact support */}
      <section className="mb-10">
        <h2 className="text-xl font-semibold mb-4 text-blue-600">
          Besoin d’aide ?
        </h2>
        <p className="text-gray-700 text-sm leading-relaxed">
          Pour toute question technique ou demande d’assistance, veuillez nous contacter :
        </p>
        <ul className="mt-2 text-gray-700 text-sm">
          <li>📧 Email : <a href="shydronex@gmail.com" className="text-blue-600 underline">shydronex@gmail.com</a></li>
          <li>📞 Téléphone : +229 58 22 63 60</li>
        </ul>
      </section>

      <p className="text-xs text-gray-500 text-center">
        HydroNex © 2025 — Tous droits réservés
      </p>
    </div>
  );
}
