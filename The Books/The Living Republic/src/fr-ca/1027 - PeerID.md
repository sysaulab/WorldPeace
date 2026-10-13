### PeerID

**Identité sociale-biométrique sans racine, hors ligne d'abord, pour la Gouvernance Vivante.**

#### Noyau

- **Pas de racine, pas d'émetteur central, pas d'ID global.** Le graphe est le registre. L'autorité est délimitée : les infirmières accréditent les infirmières, les universités accréditent les diplômés, les quartiers accréditent les résidents.
- **Amorçage avec deux personnes.** Échangez les clés via QR/NFC/Bluetooth. Signez une attestation mutuelle. C'est une cellule pair. Le graphe croît par poignée de main.
- **Biométrie = étiquette/présence, jamais secret.** Phrase de passe = secret. Appareil = coffre-fort. Une empreinte volée seule ne peut pas déverrouiller ; une phrase de passe seule sans appareil ne peut pas déverrouiller.
- **L'identité est mortelle.** Perte = mort ou renaissance sociale via des attestations de continuité de personnes qui vous connaissaient. Pas de récupération centrale. Si personne ne se porte garant, recommencez à zéro.
- **Révocation = mise à jour signée du graphe.** Un justificatif meurt lorsque le soutien seuil chute. Pas une trahison ; de l'honnêteté.

#### Portefeuille
Contient : clé racine de l'appareil, modèle biométrique local, graine chiffrée par phrase de passe, clés par paires par contexte, justificatifs signés, cache du graphe de confiance, moteur de politiques.

**Champs d'attestation :** sujet, contexte, poids, horodatage, expiration, conditions de révocation, signature.

**Justificatifs :** auto-déclarations, attestations de pairs, justificatifs à seuil (ex. 5 sur 7 infirmières), institutionnels, tuteur.

#### Graphe

- **Global par connexion, pas par racine.** Les nœuds communs relient les grappes ; l'internet achemine les requêtes.
- **Vérification :** le vérificateur demande « qui connaît Alice ? » Les chemins se propagent. Le vérificateur évalue localement : chemins indépendants, nœuds de confiance, fraîcheur, révocations, correspondance de contexte.
- **Pas de dépendance aux ponts.** La redondance augmente à mesure que le graphe croît. Les ponts capturés sont contournés.

#### Résistance aux attaques Sybil

- **Coût social, pas prévention cryptographique.** Une nouvelle identité exige que N personnes réelles attestent d'une rencontre physique et du contrôle des clés. Le maintien exige une confiance continue.
- **La biométrie confirme la présence locale.** Pas de base de données biométrique globale. L'unicité globale n'est pas un objectif ; la responsabilité locale l'est.
- **La renaissance exige de gagner une nouvelle confiance.** C'est une réforme sociale, pas un enfermement.

#### Hors ligne / En ligne

- **Hors ligne :** présenter des justificatifs, signer des défis, vérifier des signatures, authentifier des pairs via QR/NFC/Bluetooth/Wi-Fi local.
- **En ligne :** interroger les pairs faisant autorité, récupérer les révocations, synchroniser le graphe, voter.
- **Stockage distribué :** fragments chiffrés de justificatifs publics. Inutiles sans le secret de l'appareil. Pas de récupération magique.

#### Récupération comme Renaissance
Pas de récupération de clé. Nouvelle clé + attestations de continuité de personnes qui vous connaissaient. Assez de signatures → justificatifs réémis. Sinon, recommencez à zéro. Rend la coercition plus difficile ; identité liée à des relations vivantes.

#### Intégration à la Gouvernance Vivante

- **Couche d'identité pour le Registre de Consentement Continu.** Les justificatifs d'adhésion définissent l'éligibilité. Les nullifieurs empêchent le double vote par juridiction.
- **Le vote exige l'internet ; le portefeuille fonctionne hors ligne.** Lois sur registre distribué, pas de contrôle central.
- **Cordon Andon :** les justificatifs de tuteur autorisent la pause. **Non-délégation :** chaque soutien est une signature discrète. **Sentience :** les humains et les IA sentientes détiennent des PeerID ; les non-sentientes ont des tuteurs.
- **Les lois globales** exigent des chaînes de confiance intercommunautaires, pas une unicité globale. Seuil plus élevé pour une unicité stricte ; ou sanctions automatiques pré-engagées.

#### Vie privée et surveillance

- **Technique :** clés par paires, ZKP, divulgation sélective, biométrie locale, P2P chiffré, clés rotatives, pas de graphe global.
- **Gouvernance :** la surveillance viole l'Axiome du Respect. Le pouvoir est transparent ; les individus sont privés. Le Cordon Andon peut suspendre les lois de surveillance.
- **Limites :** l'observation physique, les métadonnées, l'inférence, la coercition subsistent. Objectif : rendre la surveillance de masse coûteuse, fragmentée, contestable.

#### Gouvernance du protocole
Pas de propriétaire. Spécifications ouvertes, implémentations multiples. Cadres de confiance locaux. Litiges locaux, escalade via le graphe, Cordon Andon. Forkable. Fluide.

#### Contexte
Post-catastrophe après abus d'une autorité centralisée. L'ID centralisé discrédité. Discipline élevée ; principes de santé systémique universels. Les attaques Sybil perçues comme des attaques contre les communs. Norme de Gouvernance Vivante. Confiance gagnée en personne.

#### Essence
PeerID est un maillage sans racine de relations vivantes, de biométrie locale et de justificatifs délimités. S'amorce avec deux personnes. Croît par la confiance. Meurt avec la personne. René par la communauté. Couche d'identité pour le consentement continu, des institutions transparentes, des individus privés.