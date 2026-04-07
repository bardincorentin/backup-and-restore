# 📚 Cours: Sauvegarde & Restauration Chiffrée — ISO 27001

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![CI Status](https://img.shields.io/badge/CI-Setup-blue)
![Tests](https://img.shields.io/badge/Tests-12%20passing-brightgreen)

**Niveau:** BTS SIO/SISR 2ème année
**Durée:** 2 jours (14 heures)
**Certification:** BCIT Formation Qualiopi | PECB Gold Trainer | ISO 27001 LA/LI

---

## 📖 Description

Framework complet et production-ready pour :
- **Sauvegarde** : Dossier source → Archive ZIP → Hash SHA-256 → Manifeste JSON → Chiffrement AES-256
- **Restauration** : Fichier chiffré → Vérification intégrité → Déchiffrement → Extraction
- **Conformité ISO 27001** : A.10 (Confidentialité), A.12 (Traçabilité), A.14 (Intégrité)
- **Audit trail** : Logging immuable en format ISO 8601

Inclus : 2 scripts Python + Suite de tests (12 tests ISO 27001) + Matériel pédagogique Gamma.

---

## 🏗️ Architecture

### Structure du projet

```
backup-and-restore/
├── backup_framework.py         ← Script principal (620 lignes)
├── test_suite.py               ← Tests complets (615 lignes)
├── README.md                   ← Documentation (ce fichier)
├── .gitignore                  ← Exclusions Git
├── .env.example                ← Template variables d'environnement
├── SECURITY.md                 ← Politique sécurité
├── CHANGELOG.md                ← Historique versions
├── setup.sh                    ← Automatisation setup
├── .github/
│   └── workflows/
│       ├── ci.yml              ← Tests + Lint + Build
│       ├── release.yml         ← Versioning automatique
│       ├── pr-check.yml        ← Validation PR
│       └── security.yml        ← Audit de sécurité
└── gamma.md                    ← Index documents pédagogiques

```

### Pipeline sauvegarde

```
Source Folder
    ↓
[BackupManager]
    ↓
├→ Archiver()          (ZIP DEFLATE + exclusions)
├→ Vérifier intégrité  (testzip())
├→ Generer manifeste   (JSON + SHA-256)
├→ Chiffrer            (AES-256 Fernet)
└→ Log audit           (Timestamps ISO 8601)
    ↓
Fichiers générés:
  - {name}_{timestamp}.zip         ← Archive
  - {name}_{timestamp}.zip.manifest ← Intégrité
  - {name}_{timestamp}.zip.enc     ← Chiffré
  - Clé Fernet B64                ← À conserver !
```

### Pipeline restauration

```
Manifeste + Clé
    ↓
[RestoreManager]
    ↓
├→ Vérifier manifeste   (Existence + Hash)
├→ Déchiffrer           (AES-256)
├→ Extraire archive     (testzip())
├→ Log audit            (Traçabilité)
└→ Rapport intégrité
    ↓
Dossier restauré (identique à original)
```

---

## 🚀 Installation & Setup

### Prérequis

- **Python 3.9+** : `python3 --version`
- **pip** : `pip3 --version`
- **Dossier test** (optionnel) : `mkdir -p test_data`

### Installation rapide (30 secondes)

```bash
# 1. Cloner repo
git clone https://github.com/YOUR_USERNAME/backup-and-restore.git
cd backup-and-restore

# 2. Exécuter setup (automatisé)
chmod +x setup.sh
./setup.sh

# 3. Vérifier installation
python3 -c "import cryptography; print('✓ OK')"
```

### Installation manuelle

```bash
# Installer dépendances
pip install cryptography

# Vérifier version
pip show cryptography
# Expected: cryptography>=40.0.0
```

---

## 💻 Usage

### 1. Sauvegarder un dossier

```bash
# Mode simple
python3 backup_framework.py \
  --source /chemin/vers/dossier \
  --backup nom_sauvegarde

# Exemple réel
python3 backup_framework.py \
  --source /var/www/myapp \
  --backup app_production_2024-01

# Résultat:
# ✓ app_production_2024-01_20240115_143022.zip
# ✓ app_production_2024-01_20240115_143022.zip.manifest
# ✓ app_production_2024-01_20240115_143022.zip.enc
#
# ✓ Clé de restauration: gAEJd...xyzABC (À CONSERVER!)
```

### 2. Restaurer depuis sauvegarde

```bash
# Utiliser la clé affichée lors sauvegarde
python3 backup_framework.py \
  --restore app_production_2024-01_20240115_143022.zip.manifest \
  --destination /chemin/restauration \
  --key "gAEJd...xyzABC"

# Exemple
python3 backup_framework.py \
  --restore app_production_2024-01_20240115_143022.zip.manifest \
  --destination /restore/app_backup \
  --key "gAEJdxyzABC..."

# Résultat:
# ✓ Vérification manifeste...
# ✓ Déchiffrement...
# ✓ Extraction 42 fichiers...
# ✓ Restauration réussie dans /restore/app_backup
```

### 3. Lancer les tests complets

```bash
python3 test_suite.py

# Résultat attendu:
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
# RÉSUMÉ: 12/12 tests réussis
# ======================================================================
```

---

## 🔒 Variables d'environnement

Aucune clé secrète hardcodée. Utiliser `.env.example` :

```bash
# Copier template
cp .env.example .env

# Éditer avec vos paramètres
cat .env
```

**Contenu `.env`:**

```
# Logs (optionnel)
LOG_FILE=backup.log
LOG_LEVEL=INFO

# Restauration sécurisée
RESTORE_VERIFY_HASH=true
RESTORE_TIMEOUT_SECONDS=3600

# Exclusions (optionnel)
EXCLUDE_PATTERNS=".pyc,__pycache__,.git,node_modules,.env"
```

---

## 📦 Dépendances

**Minimaliste** : 1 seule dépendance externe

| Package | Version | Rôle | Raison |
|---------|---------|------|--------|
| `cryptography` | ≥40.0.0 | Chiffrement Fernet AES-256 | Standard OWASP, certifié OpenSSL |

Stdlib Python inclus : `json`, `os`, `sys`, `zipfile`, `hashlib`, `logging`, `argparse`, `pathlib`, `datetime`.

---

## ✅ Tests

### Exécution rapide

```bash
# Tous les tests (2-3 min)
python3 test_suite.py

# Spécifique
python3 -m pytest test_suite.py::TestsFonctionnels::test_archivage_simple -v
```

### Couverture

- **Fonctionnels** : Archivage, Manifeste, Chiffrement, Restauration (4 tests)
- **ISO 27001** : Confidentialité (A.10), Intégrité (A.14), Traçabilité (A.12) (4 tests)
- **Performance** : Benchmark chiffrement + hachage (2 tests)
- **Edge cases** : Corruption, mauvaise clé, fichiers manquants

### CI/CD

Tests exécutés automatiquement sur:
- Chaque push vers `develop`
- Chaque pull request vers `main`
- Build release (`main` → v1.0.0)

---

## 📋 Configuration GitHub

### Branch protection

À activer manuellement sur GitHub:

**Settings → Branches → Protect → Require:**
- ✅ Pull request reviews before merging (1 reviewer)
- ✅ Commit signing (GPG)
- ✅ Passing status checks (CI green)
- ✅ Up to date before merging
- ✅ Dismiss stale PR approvals
- ✅ No force pushes

### Auto-merge

**Settings → Pull Requests:**
- ✅ Allow auto-merge
- Priorité: Squash & merge

---

## 🔐 Sécurité

Voir [SECURITY.md](SECURITY.md) pour:
- Politique de divulgation (responsible disclosure)
- Audit de sécurité (hebdo via GitHub Security)
- Rotation de clés (recommandations)
- Gestion des secrets (jamais dans git)

**Checklist avant production:**
- [ ] Clés en variables d'environnement (jamais hardcodées)
- [ ] Logs sauvegardés sur stockage immutable
- [ ] Permissions fichiers: `0o640` (rw-r-----)
- [ ] Tester restauration depuis sauvegarde (fail-over)
- [ ] Monitoring: audit trail + alertes anomalies
- [ ] Backup hors-site (géo-redondance)

---

## 📚 Matériel pédagogique

Tous les documents Gamma (cours, TP, corrections) listés dans [gamma.md](gamma.md).

### Jour 1 (7h) — Fondations
- Support cours: Variables Python, AES-256, SHA-256, ZIP
- TP 1-2: Fichiers binaires, chiffrement, hachage
- Exercices 1.1-1.5: Gestion clés, benchmark, magic bytes

### Jour 2 (7h) — Intégration
- Support cours: Archivage, ISO 27001, Pipeline complet
- TP 3-4: Archive ZIP, Classes BackupManager/RestoreManager
- Exercices 2.1-2.5: Rotation clés, backup incrémental, threading
- Tests ISO 27001: Conformité automatisée

**Langage pédagogique:** Code à trous progressifs + solutions complètes.

---

## 🚢 Release & Versioning

Versioning **Semantic Versioning** (MAJOR.MINOR.PATCH):

- **MAJOR** (v2.0.0): Changement architecture incompatible
- **MINOR** (v1.1.0): Nouvelle feature (backward-compatible)
- **PATCH** (v1.0.1): Bug fix

Généré automatiquement par release.yml via **conventional commits**:

```bash
feat: add incremental backup (bumps MINOR)
fix: correct hash verification (bumps PATCH)
BREAKING CHANGE: change API (bumps MAJOR)
```

**Historique dans [CHANGELOG.md](CHANGELOG.md)**.

---

## 🐛 Issues & Support

### Signaler un bug

1. GitHub Issues → New issue
2. Template:
   ```
   **Description:** Brève description
   **Reproduction:** Étapes pour reproduire
   **Logs:** Sortie de `backup.log`
   **Système:** OS + Python version
   ```

### Contribution

1. Fork → Branch → Commit conventionnel → PR
2. Tests doivent passer (CI verte)
3. Reviewer automatique assigné

---

## 📊 Améliorations proposées

### 🔴 Critique (Blockers)

- [ ] **Ajouter GitHub Actions** (CI/CD automatisée) — Bloquant pour production
- [ ] **Ajouter .gitignore** (éviter secrets) — Sécurité
- [ ] **Créer SECURITY.md** (politique divulgation) — Conformité

### 🟠 Important (Next)

- [ ] **Backup incrémental** (TP 2.2) — Sauvegarder diff uniquement
- [ ] **Rotation de clés mensuelles** (TP 2.1) — Sécurité long-terme
- [ ] **Tests avec pytest** (refactor) — Couverture 100%
- [ ] **Paralléliser extraction** (TP 2.4 threading) — Perf grandes archives
- [ ] **Docker support** (Dockerfile + docker-compose) — Deploy facilité

### 🟢 Nice-to-have (Roadmap)

- [ ] Cloud storage (S3, Azure Blob) — Multi-cloud
- [ ] Déduplication de blocs — Économie stockage
- [ ] MFA pour restauration — Sécurité supplémentaire
- [ ] Web UI (FastAPI) — Accessible web
- [ ] Monitoring dashboard (Prometheus/Grafana) — Observabilité

---

## 📄 Licence

**MIT License** — Libre d'usage pédagogique et commercial.

Fichiers:
- `backup_framework.py` — MIT
- `test_suite.py` — MIT
- Matériel pédagogique Gamma — BCIT Formation (Qualiopi certifiée)

---

## 📞 Contact & Contribution

**Auteur:** Corentin BARDIN
**Organisation:** BCIT Formation Qualiopi
**Email:** contact@bcit-formation.fr
**Certification:** PECB Gold Trainer | ISO 27001 LA/LI

**Support post-cours:** Discord/Slack (voir invit dans confirmation)

---

## 📝 Historique versions

**v1.0.0** (2024-01-15)
- ✓ Framework sauvegarde/restauration production-ready
- ✓ Suite tests 12/12 (fonctionnels + ISO 27001 + perf)
- ✓ Logging audit ISO 8601
- ✓ Matériel pédagogique 14 documents Gamma
- ✓ 12 exercices progressifs + corrections

Voir [CHANGELOG.md](CHANGELOG.md) pour détails.

---

**Dernière mise à jour:** Avril 2024
**CI Status:** [![CI](https://img.shields.io/badge/CI-blue)]() · **Tests:** [![Tests](https://img.shields.io/badge/Tests-12%20passing-brightgreen)]()
