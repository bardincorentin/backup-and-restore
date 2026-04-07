# 📚 Index Gamma - Tous les documents du cours

## Cours: Scripting de Sauvegarde et Restauration Chiffrée
**Durée:** 2 jours (14 heures)  
**Niveau:** BTS SIO/SISR 2ème année  
**Certification:** BCIT Formation Qualiopi

---

## 🎯 GUIDES PRINCIPAUX

### Guide Complet du Cours
**Document:** "De la théorie à la production : Construisez votre framework ISO 27001"
- **Lien Gamma:** https://gamma.app/generations/R2fSs4jpplngZi9Vfxens
- **Contenu:** Présentation cours + importance + livrables + cas d'usage + portfolio building + trajectoire carrière
- **Durée lecture:** 45-60 min
- **À lire:** AVANT de commencer les TP (orientation générale)

### Guide d'Orientation Professionnelle
**Document:** "De l'étudiant au Dev Sécurité : Votre feuille de route carrière"
- **Lien Gamma:** https://gamma.app/generations/EoiTH36sAxEPYKnr2Rhbk
- **Contenu:** Paysage professionnel + 5 profils carrière + stratégies recrutement + cas succès + salaires
- **Durée lecture:** 45-60 min
- **À lire:** APRÈS le cours (planification carrière)

---

## 📅 JOUR 1 - FONDATIONS (7 HEURES)

### Support de Cours - Fondations Python & Chiffrement
**Document:** Modules 1-6 avec illustrations (15 slides)
- **Lien Gamma:** https://gamma.app/generations/mMWrQFHb4y38gOJrTcdyE
- **Contenu:**
  - Module 1: Variables, types, fichiers Python
  - Module 2: Introduction AES-256 (concept clé, IV, mode CBC)
  - Module 3: Hachage SHA-256 (concept unidirectionnel)
  - Module 4: Archivage ZIP
  - Module 5: ISO 27001 (confidentialité, intégrité, traçabilité)
  - Module 6: Architecture pipeline complet
- **Durée:** 45 min de cours
- **Format:** Présentation visuelle avec exemples
- **Utilisation:** Affichage écran lors cours matin J1

---

### TP 1 - Fichiers Binaires et Chiffrement AES-256
**Document:** Exercices code à trous (3 parties A, B, C)
- **Lien Gamma:** https://gamma.app/generations/kjc9stNJkQ9wpML3crbpo
- **Contenu:**
  - Partie A: Lecture/écriture fichiers binaires (open, read, write)
  - Partie B: Chiffrement AES-256 avec Fernet (exercices B1-B2)
  - Partie C: Application fichier complet
- **Durée TP:** 90 minutes (45 min cours + 45 min travail)
- **Format:** Code à trous avec indices
- **Prérequis:** Avoir regardé Support Cours matin
- **Utilisation:** Ouvert pendant travail, complétez manquants

---

### Correction TP 1
**Document:** Solutions détaillées avec explications
- **Lien Gamma:** https://gamma.app/generations/Kx5hwjaRp2CuLbSCjPhun
- **Contenu:**
  - Solutions complètes (lire_fichier_binaire, obtenir_taille_fichier, chiffrer_message, dechiffrer_message, chiffrer_fichier)
  - Explications ligne par ligne
  - Erreurs courantes: "AttributeError", "TypeError", "InvalidToken"
  - Résultats attendus avec captures
  - Optimisations et bonnes pratiques
- **Durée:** 45 min explication live
- **Format:** Markdown avec code blocks
- **Utilisation:** Affichage écran lors correction TP1

---

### TP 2 - Hash SHA-256 et Intégrité
**Document:** Exercices code à trous (hash + manifeste)
- **Lien Gamma:** https://gamma.app/generations/VqUpaZuuqSFzoaFqMq9Fp
- **Contenu:**
  - Partie A: Concepts hash (MD5 vs SHA-1 vs SHA-256)
  - Partie B: Calcul SHA-256 par blocs (B1-B2: comparer fichiers)
  - Partie C: Manifeste JSON (C1: créer manifeste, C2: vérifier manifeste)
  - Partie D: Intégration avec TP 1 (workflow complet)
- **Durée TP:** 60 minutes
- **Format:** Code à trous progressif
- **Prérequis:** Maîtriser TP 1
- **Utilisation:** Après-midi J1

---

### Correction TP 2
**Document:** Solutions + exemples manifeste + cas test
- **Lien Gamma:** https://gamma.app/generations/tqDQTRrx623fVkZxeGuaU
- **Contenu:**
  - Solutions B1 (calculer_hash_fichier), B2 (fichiers_identiques)
  - Solutions C1 (creer_manifeste), C2 (verifier_manifeste)
  - Exemple manifeste JSON généré
  - Code avancé: rapport_verif_complet
  - Test d'intégrité: simuler corruption
  - Cas d'usage réel: vérifier après téléchargement
- **Durée:** 45 min explication
- **Format:** Markdown avec JSON exemples
- **Utilisation:** Affichage écran lors correction TP2

---

### Exercices Jour 1 + Corrections
**Document:** 5 exercices progressifs + solutions détaillées
- **Lien Gamma:** https://gamma.app/generations/bJiQUUMxBhV2LOtXN91kT
- **Contenu des exercices:**
  - **1.1 Gestion sécurisée de clés:** Sauvegarder avec permissions 0o600
  - **1.2 Chiffrer dossier complet:** Parcourir et chiffrer multiples fichiers
  - **1.3 Analyser fichier:** Retourner hash + taille + nombre lignes
  - **1.4 Identifier type fichier:** Magic bytes (ZIP, PDF, PNG, JPEG, texte)
  - **1.5 Benchmark chiffrement:** Mesurer vitesse vs taille fichier
- **Durée exercices:** 75 minutes (individuel)
- **Format:** Code à trous + solution côte à côte
- **Solutions:** Explications détaillées + résultats attendus
- **Utilisation:** Après-midi J1 (75 min de travail)

---

## 📅 JOUR 2 - INTÉGRATION & PRODUCTION (7 HEURES)

### Support de Cours - Archivage et ISO 27001
**Document:** Modules 4-6 avec diagrammes (15 slides)
- **Lien Gamma:** https://gamma.app/generations/kvaQAz2H0VeYLws28RBGh
- **Contenu:**
  - Module 4: Créer archives ZIP (simple, récursif, extraction)
  - Module 5: os.walk(), zipfile, exclusions fichiers
  - Module 6: Intégration pipeline complet (archiver → manifeste → chiffrer)
  - ISO 27001: A.10 (confidentialité), A.14 (intégrité), A.12 (traçabilité)
  - Workflow complet jour 2 avec exemples
- **Durée:** 45 min cours
- **Format:** Présentation visuelle + code examples
- **Utilisation:** Matin J2 affichage écran

---

### TP 3 - Archivage ZIP Récursif
**Document:** Code à trous archivage ZIP (3 parties)
- **Lien Gamma:** https://gamma.app/generations/kvaQAz2H0VeYLws28RBGh
- **Contenu:**
  - Partie A: Archive ZIP simple (ZipFile, write)
  - Partie B: Archive récursive (os.walk, arcname, exclusions)
  - Partie C: Extraction avec contrôle (testzip, extractall, validation)
- **Durée TP:** 90 minutes
- **Format:** Code à trous progressif
- **Prérequis:** TP 1 + TP 2 maîtrisés
- **Utilisation:** Matin J2

---

### TP 4 - Script Complet + Correction
**Document:** Classes BackupManager + RestoreManager (code à trous + solution)
- **Lien Gamma:** https://gamma.app/generations/Hid6MmEyzXBmPWvok0RdY
- **Contenu:**
  - **Exercice TP4-A:** Code à trous BackupManager
    - Méthode archiver()
    - Méthode generer_manifeste()
    - Méthode chiffrer()
    - Méthode verifier_integrite()
    - Méthode executer_sauvegarde()
  - **Exercice TP4-B:** Code à trous RestoreManager
    - Méthode verifier_manifeste()
    - Méthode dechiffrer()
    - Méthode extraire()
    - Méthode executer_restauration()
  - **Exercice TP4-C:** Utilisation complète + tests
  - **Correction complète:** Solutions côte à côte avec explications
  - **Logging ISO 27001:** Configuration audit trail
  - **Gestion erreurs:** Try/catch avec logging
- **Durée TP:** 120 minutes
- **Format:** Code à trous + solution complete
- **Résultat:** Script production-ready à ajouter portfolio GitHub
- **Utilisation:** Après-midi J2 (90 min travail)

---

### Exercices Jour 2 + Corrections + Tests ISO 27001
**Document:** 5 exercices avancés + corrections + test suite
- **Lien Gamma:** https://gamma.app/generations/BR8vJt8a1Ffzsi5m4D3Q5
- **Contenu des exercices:**
  - **2.1 Rotation mensuelle de clés:** Gérer clés par mois + archivage
  - **2.2 Backup incrémental:** Dépendances entre archives, chaîne restauration
  - **2.3 Quarantaine fichiers suspects:** Scanner + isoler (malware, taille, extension)
  - **2.4 Restauration parallèle:** Threading pour extraction rapide
  - **2.5 Audit trail complet:** Logging ISO 27001 immuable (append-only)
- **Durée exercices:** 75 minutes (individuel)
- **Format:** Code à trous + solutions complètes
- **Tests ISO 27001 inclus:**
  - A.10.1.1: Chiffrement fort (AES-256)
  - A.14.1.2: Intégrité (SHA-256)
  - A.14.1.1: Contrôle d'accès (permissions fichiers)
  - A.12.4.1: Traçabilité (logging)
  - Classe TestsISO27001 avec 6 tests
- **Utilisation:** Après-midi J2 (60 min exercices + 15 min tests)

---

## 🔗 RESSOURCES COMPLÉMENTAIRES

### Scripts Python (fichiers à télécharger)

#### backup_framework.py
- **Chemin:** /home/claude/backup_framework.py (ou lien GitHub après push)
- **Lignes:** 600+
- **Contenu:**
  - Classes BackupManager + RestoreManager complètes
  - Pipeline: Archiver → Manifeste → Chiffrer → Restaurer
  - Logging ISO 27001 A.12.4.1
  - CLI complète (--source, --backup, --restore, --destination, --key)
  - Commentaires détaillés + docstrings
  - Production-ready
- **Usage:** `python3 backup_framework.py --source /data --backup myapp_2024-01`
- **À ajouter:** Votre portfolio GitHub

#### test_suite.py
- **Chemin:** /home/claude/test_suite.py (ou GitHub)
- **Lignes:** 400+
- **Contenu:**
  - Tests fonctionnels (archivage, manifeste, chiffrement, restauration)
  - Tests ISO 27001 (A.10, A.14, A.12)
  - Benchmarks performance (chiffrement + hachage)
  - TestsFonctionnels, TestsISO27001, TestsPerformance classes
- **Usage:** `python3 test_suite.py`
- **Résultat:** 12/12 tests réussis = preuve conformité

#### README.md
- **Chemin:** /home/claude/README.md
- **Contenu:**
  - Organisation fichiers
  - Planning pédagogique détaillé (heure par heure)
  - Utilisation scripts (sauvegarde + restauration + tests)
  - Checklist avant/pendant/après cours
  - Objectifs pédagogiques J1 et J2

---

## 📊 CARTE MENTALE DOCUMENTS

```
COURS SAUVEGARDE CHIFFRÉE (14h)
│
├─ GUIDES ORIENTATION (130+ pages)
│  ├─ Guide Complet Cours
│  │  └─ https://gamma.app/generations/R2fSs4jpplngZi9Vfxens
│  └─ Guide Carrière Professionnelle
│     └─ https://gamma.app/generations/EoiTH36sAxEPYKnr2Rhbk
│
├─ JOUR 1 - FONDATIONS (7h)
│  ├─ Support Cours (Modules 1-6)
│  │  └─ https://gamma.app/generations/mMWrQFHb4y38gOJrTcdyE
│  ├─ TP 1 - AES-256 (code à trous)
│  │  └─ https://gamma.app/generations/kjc9stNJkQ9wpML3crbpo
│  ├─ Correction TP 1
│  │  └─ https://gamma.app/generations/Kx5hwjaRp2CuLbSCjPhun
│  ├─ TP 2 - SHA-256 + Manifeste (code à trous)
│  │  └─ https://gamma.app/generations/VqUpaZuuqSFzoaFqMq9Fp
│  ├─ Correction TP 2
│  │  └─ https://gamma.app/generations/tqDQTRrx623fVkZxeGuaU
│  └─ Exercices 1.1-1.5 + Corrections
│     └─ https://gamma.app/generations/bJiQUUMxBhV2LOtXN91kT
│
├─ JOUR 2 - INTÉGRATION (7h)
│  ├─ Support Cours (Archivage + ISO 27001)
│  │  └─ https://gamma.app/generations/kvaQAz2H0VeYLws28RBGh
│  ├─ TP 3 - ZIP Récursif (code à trous)
│  │  └─ https://gamma.app/generations/kvaQAz2H0VeYLws28RBGh
│  ├─ TP 4 - Script Complet + Correction
│  │  └─ https://gamma.app/generations/Hid6MmEyzXBmPWvok0RdY
│  └─ Exercices 2.1-2.5 + Tests ISO 27001
│     └─ https://gamma.app/generations/BR8vJt8a1Ffzsi5m4D3Q5
│
└─ RESSOURCES PYTHON
   ├─ backup_framework.py (600+ lignes, production-ready)
   ├─ test_suite.py (400+ lignes, tests complets)
   └─ README.md (organisation + usage)
```

---

## 🎯 WORKFLOW RECOMMANDÉ

### Avant le cours (J-2)
1. Lire: **Guide Complet du Cours** (orientation)
2. Préparer: Python 3.9+, VSCode, dossier test

### JOUR 1 Matin
1. Afficher: **Support Cours** (45 min)
2. Ouvrir: **TP 1** (code à trous)
3. Montrer: **Correction TP 1** (45 min)

### JOUR 1 Après-midi
1. Afficher: Support TP 2 intégré
2. Ouvrir: **TP 2** (code à trous)
3. Montrer: **Correction TP 2** (45 min)
4. Travail: **Exercices Jour 1** (75 min)
5. Débrief: Corrections + Q&A (30 min)

### JOUR 2 Matin
1. Afficher: **Support Cours** Jour 2 (45 min)
2. Ouvrir: **TP 3** (code à trous)
3. Correction live (45 min)

### JOUR 2 Après-midi
1. Ouvrir: **TP 4** (code à trous)
2. Montrer: **Correction TP 4** (90 min)
3. Travail: **Exercices Jour 2** (60 min)
4. Lancer: **test_suite.py** (15 min)
5. Débrief final + célébration ✓

### Après le cours
1. Lire: **Guide Carrière Professionnelle** (orientation emploi)
2. Pousser code GitHub
3. Publier post LinkedIn
4. Contacter recruteurs

---

## 📱 ACCÈS RAPIDE

| Document | Lien Gamma | Durée | Type |
|----------|-----------|-------|------|
| Guide Cours | https://gamma.app/generations/R2fSs4jpplngZi9Vfxens | 45-60 min | Document |
| Guide Carrière | https://gamma.app/generations/EoiTH36sAxEPYKnr2Rhbk | 45-60 min | Document |
| Support J1 | https://gamma.app/generations/mMWrQFHb4y38gOJrTcdyE | 45 min | Slides |
| TP 1 | https://gamma.app/generations/kjc9stNJkQ9wpML3crbpo | 90 min | Code |
| Correction 1 | https://gamma.app/generations/Kx5hwjaRp2CuLbSCjPhun | 45 min | Cours |
| TP 2 | https://gamma.app/generations/VqUpaZuuqSFzoaFqMq9Fp | 60 min | Code |
| Correction 2 | https://gamma.app/generations/tqDQTRrx623fVkZxeGuaU | 45 min | Cours |
| Exercices J1 | https://gamma.app/generations/bJiQUUMxBhV2LOtXN91kT | 75 min | Exercices |
| Support J2 | https://gamma.app/generations/kvaQAz2H0VeYLws28RBGh | 45 min | Slides |
| TP 3 | https://gamma.app/generations/kvaQAz2H0VeYLws28RBGh | 90 min | Code |
| TP 4 | https://gamma.app/generations/Hid6MmEyzXBmPWvok0RdY | 120 min | Code |
| Exercices J2 | https://gamma.app/generations/BR8vJt8a1Ffzsi5m4D3Q5 | 75 min | Exercices |

---

## ✅ CHECKLIST INSTRUCTEUR

- [ ] Télécharger tous les liens Gamma
- [ ] Préparer machine de démonstration
- [ ] Tester scripts Python (backup_framework.py + test_suite.py)
- [ ] Créer dossier test pour exemples
- [ ] Préparer salle/vidéoprojecteur
- [ ] Diffuser Guide Complet aux étudiants
- [ ] Préparer accès GitHub pour pousser code
- [ ] Configurer Slack/Discord pour support post-cours

---

**Dernière mise à jour:** Janvier 2024  
**Cours:** Scripting de Sauvegarde et Restauration Chiffrée  
**Formateur:** Corentin BARDIN (BCIT Formation Qualiopi)  
**Contact:** contact@bcit-formation.fr
