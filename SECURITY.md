# 🔐 Security Policy

**Date:** Avril 2024
**Version:** 1.0
**Certification:** BCIT Formation | PECB Gold Trainer | ISO 27001 LA/LI

---

## 📋 Divulgation responsable

Si vous découvrez une vulnérabilité de sécurité:

### ⚠️ NE PAS
- ❌ Publier la vulnérabilité sur GitHub Issues (public)
- ❌ Tweeter ou discuter publiquement
- ❌ Vendre l'information
- ❌ Tester sans permission explicite

### ✅ FAIRE
1. **Email direct** → `security@bcit-formation.fr`
   - Objet: `[SECURITY] backup-and-restore vuln`
   - Incluez: Description + Reproduction + Impact
   - Signez avec GPG si possible

2. **Timeline:**
   - Day 1: Nous confirmons réception
   - Day 3: Évaluation sévérité
   - Day 7: Plan de correction communiqué
   - Day 30: Patch publié (à moins que complexe)
   - Day 60: CVE demandé si critique

3. **Confidentialité:**
   - Votre nom sera crédité en CHANGELOG.md
   - Vous pouvez rester anonyme (option)
   - Aucune donnée sensible n'est partagée publiquement

---

## 🛡️ Sécurité par conception

### Chiffrement (A.10.1.1 ISO 27001)

**Utilisation:** Fernet (AES-128 CBC + HMAC SHA-256)

```python
from cryptography.fernet import Fernet
cle = Fernet.generate_key()  # 256-bit key (32 bytes)
chiffre = Fernet(cle)
ciphertext = chiffre.encrypt(plaintext)
```

**Trade-off pédagogique:**
- ✅ Production-ready, OWASP-approved
- ✅ Authentification (HMAC) incluse
- ✅ Gestion IV automatique
- ⚠️ Pédagogique (non crypto brutale) — pour cours
- ❓ Production: Considérer `cryptography.hazmat` pour AES-256 brut

**Rotation de clés:**
```bash
# Recommandé: Renouveler clé tous les 90 jours
# Archiver clés anciennes 1 an minimum
# Template: cle_2024_01.enc (mois-année)
```

---

### Intégrité (A.14.1.2 ISO 27001)

**Hash SHA-256** sur tous les fichiers:
- Archive ZIP (avant chiffrement)
- Fichier chiffré (après chiffrement)
- Stocké dans manifeste JSON

```python
import hashlib
hasher = hashlib.sha256()
with open(archive, 'rb') as f:
    for chunk in iter(lambda: f.read(4096), b''):
        hasher.update(chunk)
hash_val = hasher.hexdigest()  # 64 caractères hex
```

**Vérification avant restauration:**
```
Fichier chiffré → Calcul hash → Comparer manifeste
Si mismatch → ABORT (corruption détectée)
```

---

### Contrôle d'accès (A.14.1.1 ISO 27001)

**Permissions fichiers:**
```bash
# Manifeste JSON
chmod 0o640 *.zip.manifest    # rw-r----- (propriétaire + groupe)

# Fichier chiffré
chmod 0o640 *.zip.enc         # rw-r----- (propriétaire + groupe)

# Fichier journal (audit trail)
chmod 0o640 backup.log        # rw-r----- (immuable)

# Clé (NEVER 0o644!)
chmod 0o600 cle_*.enc         # rw------- (propriétaire SEUL)
```

**Propriétaire:**
```python
os.chown(filename, uid=getuid(), gid=getgid())  # Si root
```

---

### Traçabilité (A.12.4.1 ISO 27001)

**Audit trail immuable (append-only):**

```
2024-04-07T14:30:22Z | INFO     | BackupManager initialisé: /var/www
2024-04-07T14:30:22Z | INFO     | Archivage de /var/www...
2024-04-07T14:30:25Z | INFO     | Archive créée: app_20240407_143025.zip (152 fichiers)
2024-04-07T14:30:25Z | INFO     | Génération du manifeste d'intégrité...
2024-04-07T14:30:26Z | INFO     | Manifeste créé: app_20240407_143025.zip.manifest
2024-04-07T14:30:26Z | INFO     | Chiffrement de l'archive avec AES-256...
2024-04-07T14:30:27Z | INFO     | Chiffrement réussi: app_20240407_143025.zip.enc
```

**Format ISO 8601:** `YYYY-MM-DDTHH:MM:SSZ`

**Durée de conservation:** 7 ans minimum (France - RGPD/légal)

**Immutabilité:**
```python
# Logs en mode append-only
logging.FileHandler(log_file, mode='a')  # 'a' = append
os.chmod(log_file, 0o640)               # Immuable
# Impossible de supprimer sans trace (système immutable)
```

---

## 🚨 Bonnes pratiques avant production

### Checklist Sécurité

- [ ] **Clés stockées EN DEHORS du repo**
  - ✅ Variables d'environnement
  - ✅ Vault (Hashicorp, AWS Secrets Manager)
  - ✅ .env (local ONLY, gitignore)
  - ❌ Hardcodées dans le code
  - ❌ Commentaires git

- [ ] **Logs sauvegardés sur stockage immuable**
  - ✅ Blockchain (WORM — Write Once Read Many)
  - ✅ Objet immutable cloud (AWS S3 Object Lock)
  - ✅ NAS/RAID avec snapshots
  - ✅ Syslog vers serveur centralisé
  - ❌ Filesystem local (risque accès root)

- [ ] **Restauration testée (fail-over)**
  - ✅ Tester restauration complète
  - ✅ Vérifier intégrité données
  - ✅ Timing acceptable pour RTO/RPO

- [ ] **Backups géo-redondants**
  - ✅ Multiple datacenters
  - ✅ Multi-cloud (S3 + Azure Blob)
  - ✅ Off-site (Veeam, CommVault)
  - ❌ Backup dans même bâtiment

- [ ] **Monitoring & Alerting**
  - ✅ Backup failed → Alert OPS
  - ✅ Restore test monthly
  - ✅ Integrity check en background
  - ✅ Dashboard Prometheus/Grafana

- [ ] **2FA pour restauration critique**
  - ✅ TOTP (Google Authenticator)
  - ✅ Approbation multi-admin
  - ✅ Audit de qui a restauré quoi

---

## 🔍 Scan de sécurité automatisé

### GitHub Actions - security.yml

Exécuté chaque semaine:

```yaml
name: Security Audit
on:
  schedule:
    - cron: '0 2 * * 0'  # Dimanche 2am UTC

jobs:
  bandit:  # Scan de code Python
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Bandit
        run: pip install bandit && bandit -r . -f json

  pip-audit:  # Dépendances
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Pip audit
        run: pip install pip-audit && pip-audit
```

**Résultat:** Email si vulnérabilités trouvées

---

## 📚 Références & Normes

### Normes appliquées

- **ISO/IEC 27001:2022** — Information security management
  - A.10.1.1: Encryption (AES-256)
  - A.14.1.1: Access control (permissions)
  - A.14.1.2: Data integrity (SHA-256 + manifeste)
  - A.12.4.1: Audit trail (logging)

- **OWASP Top 10**
  - ✅ A02: Cryptographic Failures → Fernet AES
  - ✅ A05: Access Control → chmod 0o640
  - ✅ A09: Logging & Monitoring → audit trail

- **NIST Cybersecurity Framework**
  - Protect (Encryption) → Detect (Hashing) → Respond (Logs)

### Ressources

- [cryptography.io - Fernet](https://cryptography.io/en/latest/fernet/)
- [OWASP Cheatsheet](https://cheatsheetseries.owasp.org/)
- [ISO 27001:2022](https://www.iso.org/standard/27001)

---

## 🐛 Signaler une vulnérabilité

### Procédure rapide

1. Email: `security@bcit-formation.fr`
2. Subject: `[SECURITY] Descriptif court`
3. Body:
   ```
   Vulnérabilité: [Titre]
   Sévérité: High / Medium / Low
   Reproduction: [Étapes]
   Proof-of-Concept: [Code ou screenshot]
   Impact: [Conséquences]
   Suggestion de fix: [Optionnel]
   ```
4. Attendez confirmation (24-48h)

---

## 📝 Versions & Historique

**v1.0** (2024-04-07)
- Initial security policy
- ISO 27001 A.10, A.12, A.14 compliance
- Fernet AES-128 + HMAC
- Audit trail immuable

---

**Dernière mise à jour:** Avril 2024
**Responsable:** Corentin BARDIN (BCIT Formation)
**Contact:** contact@bcit-formation.fr
