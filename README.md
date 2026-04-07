# 📚 Cours Scripting - Sauvegarde & Restauration Chiffrée

**Niveau:** BTS SIO/SISR 2ème année  
**Durée:** 2 jours (14h)  
**Objectif:** Coder un script de sauvegarde/restauration chiffré répondant aux besoins ISO 27001

---

## 📋 Organisation des livrables

### Structure proposée:

```
cours_backup/
├── JOUR_1/
│   ├── 01_Support_Cours_Fondations.pdf       (Gamma) → Théorie Python + chiffrement
│   ├── 02_TP1_Bases_Python_AES256.pdf        (Gamma) → Code à trous
│   ├── 03_Correction_TP1.pdf                 (Gamma)
│   ├── 04_TP2_Hash_et_Integrite.pdf          (Gamma)
│   ├── 05_Correction_TP2.pdf                 (Gamma)
│   ├── 06_Exercices_Jour1.pdf                (Gamma)
│   └── 07_Corrections_Exercices_J1.pdf       (Gamma)
│
├── JOUR_2/
│   ├── 08_Support_Cours_Archivage.pdf        (Gamma) → ZIP + intégration
│   ├── 09_TP3_Archivage_ZIP.pdf              (Gamma) → Code à trous
│   ├── 10_Correction_TP3.pdf                 (Gamma)
│   ├── 11_TP4_Script_Complet.pdf             (Gamma) → Code à trous + solution
│   ├── 12_Exercices_Jour2.pdf                (Gamma)
│   ├── 13_Tests_ISO27001.pdf                 (Gamma)
│   └── 14_Corrections_Exercices_J2.pdf       (Gamma)
│
├── SCRIPTS_PYTHON/
│   ├── backup_framework.py                   ← Script principal (production-ready)
│   └── test_suite.py                         ← Suite de tests complète
│
└── README.md                                  ← Ce fichier
```

---

## ⏰ Planning pédagogique (2 jours)

### JOUR 1 - Fondations Python & Chiffrement

#### Matin (09h00 - 12h30)

| Heure | Contenu | Format | Durée |
|-------|---------|--------|-------|
| 09h00 | Support Cours (Modules 1-2) | Gamma doc | 45 min |
| 09h45 | TP 1 - Fichiers & AES-256 (code à trous) | Python + Gamma | 60 min |
| 10h45 | Pause | - | 15 min |
| 11h00 | Correction TP 1 + questions | Gamma + live coding | 45 min |
| 11h45 | TP 2 - Hash SHA-256 (code à trous) | Python + Gamma | 45 min |

#### Après-midi (14h00 - 17h00)

| Heure | Contenu | Format | Durée |
|-------|---------|--------|-------|
| 14h00 | Correction TP 2 | Gamma + live coding | 45 min |
| 14h45 | Exercices Jour 1 (1.1 à 1.5) | Individuel | 75 min |
| 16h00 | Corrections + débrief | Gamma | 30 min |

**Résultat J1:** Maîtrise AES-256 + SHA-256 + hachage fichiers

---

### JOUR 2 - Intégration & Conformité ISO 27001

#### Matin (09h00 - 12h30)

| Heure | Contenu | Format | Durée |
|-------|---------|--------|-------|
| 09h00 | Support Cours (Modules 4-6) | Gamma doc | 45 min |
| 09h45 | TP 3 - Archivage ZIP récursif (code à trous) | Python + Gamma | 75 min |
| 11h00 | Pause | - | 15 min |
| 11h15 | Correction TP 3 | Gamma + live coding | 45 min |

#### Après-midi (14h00 - 17h00)

| Heure | Contenu | Format | Durée |
|-------|---------|--------|-------|
| 14h00 | TP 4 - Script complet (code à trous) | Python + Gamma | 90 min |
| 15h30 | Pause | - | 15 min |
| 15h45 | Exercices Jour 2 (2.1 à 2.5) | Individuel | 60 min |
| 16h45 | Tests ISO 27001 + débrief | test_suite.py | 15 min |

**Résultat J2:** Script production-ready + tests + conformité ISO 27001

---

## 🔑 Pédagogie - Fil conducteur

### Progression progressive

```
Jour 1:
1. Fichiers binaires (TP 1-A)
2. Chiffrement simple (TP 1-B)
3. Appliquer au fichier (TP 1-C)
4. Hash unique (TP 2-A)
5. Comparer fichiers (TP 2-B)
6. Manifeste d'intégrité (TP 2-C)

Jour 2:
7. Archive ZIP simple (TP 3-A)
8. Archive récursive (TP 3-B)
9. Extraction contrôlée (TP 3-C)
10. Pipeline complet (TP 4-A/B/C)
11. Restauration (RestoreManager)
12. Tests + ISO 27001
```

### Approche pédagogique

✓ **Code à trous dès le départ**
- Étudiants complètent les fonctions (apprentissage actif)
- Exemple complet fourni → puis à trous

✓ **Progression par étapes**
- Chaque TP ajoute 1 fonction au script
- À la fin J2: script complet fonctionnel

✓ **Tests intégrés**
- Chaque exercice inclut cas test
- Suite test_suite.py à la fin

✓ **ISO 27001 tout au long**
- Jour 1: confidentialité (chiffrement) + intégrité (hash)
- Jour 2: traçabilité (logging) + disponibilité (restauration)

---

## 💻 Utilisation des scripts Python

### 1. Installation dépendances

```bash
pip install cryptography
# Vérifier versions
python3 -c "import cryptography; print(cryptography.__version__)"
```

### 2. Lancer une sauvegarde

```bash
# Sauvegarde simple
python3 backup_framework.py --source /var/www/app --backup app_2024-01

# Résultat:
# app_2024-01_20240115_101530.zip         ← Archive
# app_2024-01_20240115_101530.zip.manifest ← Manifeste JSON
# app_2024-01_20240115_101530.zip.enc     ← Fichier chiffré

# Affiche aussi:
# ✓ Clé de restauration: gAEJdxyzABC... (à conserver!)
```

### 3. Restaurer depuis sauvegarde

```bash
# Utiliser clé affichée lors sauvegarde
python3 backup_framework.py \
  --restore app_2024-01_20240115_101530.zip.manifest \
  --destination /restore/app \
  --key "gAEJdxyzABC..."

# Résultat: fichiers restaurés dans /restore/app
```

### 4. Tests complets

```bash
python3 test_suite.py

# Résultat:
# ======================================================================
# TESTS FONCTIONNELS
# ======================================================================
# ✓ PASS | Archivage simple: 42 fichiers, 152300 bytes
# ✓ PASS | Manifeste création: Hash: a1b2c3d4e5...
# ✓ PASS | Chiffrement/déchiffrement: Chiffré: 152348 bytes
# ✓ PASS | Restauration complète: 42 fichiers restaurés
#
# ======================================================================
# TESTS ISO 27001 - CONFORMITÉ
# ======================================================================
# ✓ PASS | A.10.1.1: Chiffrement fort (AES): Clé: 128 bits (Fernet)
# ✓ PASS | A.14.1.2: Intégrité SHA-256: Hash: a1b2c3d4e5...
# ✓ PASS | A.14.1.1: Contrôle d'accès: Manifest: 0o640, Chiffré: 0o640
# ✓ PASS | A.12.4.1: Traçabilité et audit: Logging actif
#
# ======================================================================
# TESTS DE PERFORMANCE
# ======================================================================
#   Benchmark chiffrement:
#     1 KB |    0.08 ms |  11.6 MB/s
#   100 KB |    6.28 ms |  15.2 MB/s
#     1 MB |   65.13 ms |  14.8 MB/s
#
# ======================================================================
# RÉSUMÉ: 12/12 tests réussis
# ======================================================================
```

---

## 📊 Fichiers Gamma à créer

### Jour 1

1. **Support de cours** (15 slides)
   - Modules 1-2: Python fondamentaux + AES-256
   - Théorie + exemples complets
   - Images: architecture chiffrement

2. **TP 1** (document)
   - Exercices A1-C2 (code à trous)
   - Partie A: fichiers binaires
   - Partie B: chiffrement (Fernet)
   - Partie C: tests

3. **Correction TP 1** (document)
   - Solutions complètes
   - Explications détaillées
   - Résultats attendus

4. **TP 2** (document)
   - Exercices B1-C2 (code à trous)
   - Hash SHA-256
   - Manifeste JSON
   - Vérification intégrité

5. **Correction TP 2** (document)
   - Solutions + explications
   - Exemple manifeste JSON
   - Cas test corruption

6. **Exercices + Corrections Jour 1** (document combiné)
   - 5 exercices progressifs (1.1 à 1.5)
   - Thèmes: clés, hachage, types, benchmarks
   - Corrections détaillées

### Jour 2

7. **Support de cours** (15 slides)
   - Modules 4-6: ZIP + ISO 27001
   - Architecture pipeline complet
   - Diagrammes de workflow

8. **TP 3** (document)
   - Exercices A1-C1 (code à trous)
   - Archive ZIP simple puis récursive
   - Extraction avec validation

9. **Correction TP 3** (document)
   - Solutions + os.walk(), zipfile
   - Test archivage/extraction

10. **TP 4 + Correction** (document combiné)
    - Exercices TP4-A/B/C (code à trous)
    - Classes BackupManager + RestoreManager
    - Solution complète à côté

11. **Exercices + Corrections Jour 2** (document combiné)
    - 5 exercices avancés (2.1 à 2.5)
    - Thèmes: rotation clés, incrémental, quarantaine, threading, audit
    - Corrections détaillées
    - Tests ISO 27001 intégrés

---

## 🎯 Objectifs pédagogiques

### Jour 1
- ☑ Maîtriser fichiers binaires en Python
- ☑ Comprendre chiffrement symétrique (AES-256)
- ☑ Implémenter hachage SHA-256
- ☑ Générer manifeste d'intégrité

### Jour 2
- ☑ Créer archives ZIP récursives
- ☑ Intégrer chiffrement + archivage
- ☑ Restaurer avec vérification d'intégrité
- ☑ Respecter ISO 27001 (confidentialité, intégrité, traçabilité, disponibilité)

---

## ✅ Checklist d'utilisation

### Avant le cours
- [ ] Générer tous les documents Gamma (7 supports + corrections)
- [ ] Valider liens exemples
- [ ] Tester backup_framework.py sur sa machine
- [ ] Préparer dossier test (structure fichiers)

### Jour 1 (Matin)
- [ ] Support Cours 1-2 (vidéo partagée écran)
- [ ] TP 1: Étudiants ouvrent doc + Python
- [ ] Correction live: expliquer solutions

### Jour 1 (Après-midi)
- [ ] TP 2 → Correction
- [ ] Exercices individuels (1.1 à 1.5)
- [ ] Débrief: points clés AES-256 + SHA-256

### Jour 2 (Matin)
- [ ] Support Cours 4-6 (ZIP, ISO 27001)
- [ ] TP 3: Archivage récursif
- [ ] Correction TP 3

### Jour 2 (Après-midi)
- [ ] TP 4: Script complet (BackupManager + RestoreManager)
- [ ] Exercices 2.1 à 2.5
- [ ] Lancer test_suite.py
- [ ] Débrief: conformité ISO 27001

---

## 📚 Ressources pédagogiques

### Documentation officielle
- [Python docs - hashlib](https://docs.python.org/3/library/hashlib.html)
- [Cryptography.io - Fernet](https://cryptography.io/en/latest/fernet/)
- [Python docs - zipfile](https://docs.python.org/3/library/zipfile.html)

### Normes
- ISO/IEC 27001:2022 - Information security management
- ISO/IEC 27002:2022 - Information security controls

### Bonnes pratiques
- Never hardcode credentials (utiliser variables d'environnement)
- Always verify integrity before decrypt
- Keep keys separate from data
- Audit trail = legal proof

---

## 🚀 Évolutions futures

- [ ] Ajouter sauvegarde incrémentale (TP 2.2)
- [ ] Intégrer rotation de clés automatique (TP 2.1)
- [ ] Paralléliser extraction (threading - TP 2.4)
- [ ] Cloud storage (S3, Azure, etc.)
- [ ] Déduplication de blocs
- [ ] Authentification 2FA pour restauration

---

## 📞 Contact & Support

**Auteur:** Corentin BARDIN (BCIT Formation)  
**Email:** contact@bcit-formation.fr  
**Certification:** Qualiopi | PECB Gold Trainer | ISO 27001 LA/LI  
**Mise à jour:** Janvier 2024

---

## 📝 Notes de version

### v1.0 (2024-01-15)
- ✓ Support complet 2 jours
- ✓ 14 documents Gamma
- ✓ 2 scripts Python production-ready
- ✓ Tests ISO 27001 inclus
- ✓ 12 exercices progressifs + corrections

---

**Licence:** MIT - Libre d'usage pédagogique  
**Pré-requis:** Python 3.9+, pip install cryptography

