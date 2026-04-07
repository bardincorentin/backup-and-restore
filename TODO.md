# 🎯 TODO — Audit & Automatisation Complète

**Dernière mise à jour:** 2024-04-07
**Status global:** En cours
**Objectif:** CI/CD vert + sécurité + documentation

---

## 🔴 CRITIQUE — Blockers

### 1. GitHub Actions CI/CD
**Impact:** Impossible de merger PR sans tests automatisés
**Effort:** 4h
- [ ] Créer `.github/workflows/ci.yml` (test + lint + build)
- [ ] Créer `.github/workflows/release.yml` (semantic-release)
- [ ] Créer `.github/workflows/pr-check.yml` (title validation)
- [ ] Créer `.github/workflows/security.yml` (npm audit / pip audit)
- [ ] Tester workflows localement avec `act`
- [ ] Configurer branch protection sur GitHub (main + develop)

**Success criteria:** Tous les workflows green (✓ passing)

---

### 2. Fichiers de sécurité manquants
**Impact:** Secrets risque d'être commitées
**Effort:** 2h
- [ ] Ajouter `.gitignore` complet (Python + IDE)
  - `.env`, `*.pyc`, `__pycache__`, `.venv`, `backup*.zip*`, logs
- [ ] Créer `.env.example` (template variables)
- [ ] Créer `SECURITY.md` (divulgation responsable)
- [ ] Créer `dependabot.yml` (mises à jour automatiques)
- [ ] Scanner repo pour secrets commitées (git-secrets / TruffleHog)

**Success criteria:** Aucun secret trouvé, `.gitignore` blocking

---

### 3. Sauvegarde de test incomplète
**Impact:** Tests ne créent pas de données réalistes
**Effort:** 1h
- [ ] Ajouter dossier `test_data/` avec structure variée
  - Fichiers texte, binaires, dossiers vides
  - `.pyc` et dossiers à exclure (__pycache__)
- [ ] Documenter dans README (utilisation test_data)

**Success criteria:** test_suite.py passes avec vrais fichiers

---

## 🟠 IMPORTANT — Next Sprint

### 4. Documenter décisions techniques
**Impact:** Futurs contributeurs comprennent architecture
**Effort:** 2h
- [ ] Créer `DECISIONS.md` avec:
  - Pourquoi Fernet (AES-128 + HMAC) au lieu hazmat AES-256 brut
  - Pourquoi ZIP DEFLATE au lieu gzip
  - Pourquoi manifestejson au lieu de signature cryptographique
  - Choix d'exclusions par défaut

**Success criteria:** DECISIONS.md explique trade-offs

---

### 5. Améliorer couverture de tests
**Impact:** Confiance production
**Effort:** 3h
- [ ] Refactoriser test_suite.py en pytest
- [ ] Ajouter tests edge cases:
  - Corruption manifeste (hash faux)
  - Clé invalide (déchiffrement échoue)
  - Extraction avec permissions restrictives
  - Dossier destination existe (merge mode)
- [ ] Ajouter pytest fixtures pour dossiers test
- [ ] Rapport couverture (pytest-cov ≥95%)

**Success criteria:** pytest run successful, coverage ≥95%

---

### 6. Ajouter Dockerfile + setup.sh
**Impact:** Déploiement facile (non-Docker dépendances)
**Effort:** 2h
- [ ] Créer `setup.sh` (install + verify)
  - Check Python 3.9+
  - pip install cryptography
  - Permissions fichiers test
  - Lancer test_suite.py sanity check
- [ ] Créer `Dockerfile` (optionnel, multistage)
  - Build: Python 3.11-slim, cryptography
  - Runtime: Minimaliste
- [ ] Créer `.dockerignore`

**Success criteria:** ./setup.sh complète sans erreur

---

### 7. Changelog automatisé
**Impact:** Historique versions claire
**Effort:** 1h
- [ ] Créer `CHANGELOG.md` structuré
  - v1.0.0: Initial release (features + tests + docs)
  - Format: Added / Changed / Fixed / Security
- [ ] Configurer release.yml pour auto-update

**Success criteria:** CHANGELOG mise à jour, versioning visible

---

## 🟢 NICE-TO-HAVE — Roadmap Future

### 8. Backup incrémental
**Impact:** Économie stockage (diff only)
**Effort:** 6h
- [ ] Implémenter `BackupManager.incremental_backup()`
  - Comparer timestamps vs sauvegarde précédente
  - Archiver uniquement fichiers modifiés
  - Créer chaîne de dépendances (backup_1 → backup_2)
- [ ] Ajouter TP 2.2 (exercices code à trous)

**Success criteria:** Backup incrémental ≥50% compression

---

### 9. Rotation de clés automatique
**Impact:** Sécurité long-terme
**Effort:** 4h
- [ ] Implémenter `BackupManager.rotate_keys()`
  - Générer clé mensuelle (structure: cle_2024_01.enc)
  - Ré-chiffrer archives anciennes
  - Archiver clés (1 année conservation)
- [ ] Ajouter TP 2.1 (gestion clés)

**Success criteria:** Rotation sans perte données

---

### 10. Web UI (FastAPI)
**Impact:** Sauvegarder sans CLI
**Effort:** 8h
- [ ] Créer `app.py` (FastAPI)
  - POST /backup (source, nom)
  - POST /restore (manifeste, clé, dest)
  - GET /status (logs en temps réel)
- [ ] Frontend minimaliste (HTML/JS)
- [ ] Déployer sur vercel/Railway (optionnel)

**Success criteria:** UI fonctionnelle + accessible

---

### 11. Multi-cloud storage
**Impact:** Flexibility (S3, Azure, GCS)
**Effort:** 10h
- [ ] Implémenter `StorageBackend` (abstraction)
  - `S3Backend`, `AzureBlobBackend`, `LocalBackend`
- [ ] Ajouter `--storage s3` dans CLI
- [ ] Tests multi-cloud

**Success criteria:** Upload/Download S3 funcional

---

## 📊 Metriques

| Catégorie | Total | Complété | % |
|-----------|-------|----------|---|
| 🔴 Critique | 3 | 0 | 0% |
| 🟠 Important | 5 | 0 | 0% |
| 🟢 Nice-to-have | 5 | 0 | 0% |
| **TOTAL** | **13** | **0** | **0%** |

---

## 🚀 Priorité de déploiement

1. **Week 1** (15h): Critique + Important (1-7)
   - CI/CD verte, sécurité, tests améliorés
   - Target: v1.1.0 release

2. **Week 2-3** (12h): Nice-to-have (8-10)
   - Features avancées (incrémental, clés, UI)

3. **Week 4+** (optionnel): Multi-cloud (11)

---

## ✅ Checklists

### Avant première PR
- [ ] Tous les fichiers 🔴 Critique complétés
- [ ] CI/CD verte (tous workflows passing)
- [ ] Tests 12/12 réussis
- [ ] README + SECURITY.md + DECISIONS.md écrits
- [ ] `.gitignore` et `.env.example` en place
- [ ] Branch protection configurée

### Avant v1.0.0 Release
- [ ] CHANGELOG.md généré automatiquement
- [ ] Tags sémantique (v1.0.0) créé
- [ ] Release notes (GitHub Releases) publié
- [ ] Matériel pédagogique lié
- [ ] Portfolio GitHub présenté

---

## 📝 Notes

**Dépendances entre tasks:**
- 🔴 #1 (GitHub Actions) bloque tout
- 🔴 #2 (Sécurité) doit être fait avant push
- 🟠 #5 (Tests) beneficie de 🔴 #1

**Estimations:**
- 🔴 Critique: ~7h (semaine 1)
- 🟠 Important: ~8h (semaine 1-2)
- 🟢 Nice-to-have: ~28h (future sprints)

**Owner:** Corentin BARDIN (BCIT Formation)

---

Généré automatiquement lors audit 2024-04-07
