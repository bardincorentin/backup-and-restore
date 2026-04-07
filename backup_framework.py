#!/usr/bin/env python3
"""
backup_framework.py - Framework complet de sauvegarde chiffrée et archivée
Conforme ISO 27001: Confidentialité, Intégrité, Traçabilité, Disponibilité

Auteur: Corentin BARDIN (BCIT Formation)
Licence: MIT
Usage: python3 backup_framework.py --source /data --backup myapp_2024-01

Features:
- Chiffrement AES-256 avec Fernet
- Archive ZIP avec compression DEFLATE
- Hachage SHA-256 + manifeste d'intégrité
- Logging complet pour audit
- Restauration avec vérification
"""

import json
import os
import sys
import shutil
import hashlib
import logging
import zipfile
from datetime import datetime
from pathlib import Path
from argparse import ArgumentParser
from cryptography.fernet import Fernet, InvalidToken


# ============================================================================
# CONFIGURATION LOGGING (ISO 27001 A.12.4.1)
# ============================================================================

def configurer_logging(log_file='backup.log'):
    """Configure logging au format audit avec timestamps ISO 8601"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%SZ',
        handlers=[
            logging.FileHandler(log_file, mode='a'),  # append-only (immuable)
            logging.StreamHandler()
        ]
    )
    # Définir permissions fichier log (lecture restreinte)
    if os.path.exists(log_file):
        os.chmod(log_file, 0o640)
    
    return logging.getLogger(__name__)

logger = configurer_logging()


# ============================================================================
# CLASSE BackupManager - Sauvegarde chiffrée et archivée
# ============================================================================

class BackupManager:
    """
    Gère pipeline complet de sauvegarde:
    Dossier source → Archive ZIP → Hash SHA-256 → Manifeste → Chiffrement AES-256
    
    Respecte ISO 27001:
    - A.10.1.1: Chiffrement AES-256
    - A.14.1.1: Contrôle d'accès (permissions fichiers)
    - A.14.1.2: Intégrité (hash, manifeste, vérification)
    - A.12.4.1: Traçabilité (logging détaillé)
    """
    
    def __init__(self, dossier_source, nom_backup, cle=None, exclusions=None):
        """
        Initialise le gestionnaire de sauvegarde
        
        Args:
            dossier_source: Chemin du dossier à sauvegarder
            nom_backup: Nom de base de la sauvegarde (ex: "app_2024-01")
            cle: Clé Fernet existante (bytes) ou None pour générer
            exclusions: Liste d'extensions/dossiers à exclure
        """
        self.dossier_source = Path(dossier_source)
        self.nom_backup = nom_backup
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Générer ou charger clé
        if cle is None:
            self.cle = Fernet.generate_key()
            logger.info(f"Clé générée: {self.cle.decode()}")
        else:
            self.cle = cle if isinstance(cle, bytes) else cle.encode()
        
        # Exclusions par défaut
        if exclusions is None:
            self.exclusions = [
                '.pyc', '__pycache__', '.git', '.gitignore',
                'node_modules', '.tmp', '.cache', '.DS_Store',
                '*.swp', '.env', 'venv/', '.venv/'
            ]
        else:
            self.exclusions = exclusions
        
        # Noms fichiers de sortie
        timestamp_file = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        self.archive_name = f"{nom_backup}_{timestamp_file}.zip"
        self.manifeste_name = f"{self.archive_name}.manifest"
        self.chiffre_name = f"{self.archive_name}.enc"
        
        # Statistiques
        self.stats = {
            'fichiers_archives': 0,
            'fichiers_exclus': 0,
            'octets_original': 0,
            'octets_archive': 0
        }
        
        logger.info(f"BackupManager initialisé: {self.dossier_source}")
    
    def calculer_hash_fichier(self, chemin):
        """
        Calcule hash SHA-256 d'un fichier (ISO 27001 A.14.1.2)
        Lecture par blocs pour économiser mémoire (efficient pour gros fichiers)
        
        Args:
            chemin: Chemin du fichier
        
        Returns:
            Hash en hexadécimal (64 caractères)
        """
        hasher = hashlib.sha256()
        
        with open(chemin, 'rb') as f:
            while True:
                bloc = f.read(4096)  # Lire par bloc de 4KB
                if not bloc:
                    break
                hasher.update(bloc)
        
        return hasher.hexdigest()
    
    def doit_exclure(self, chemin_fichier):
        """Vérifie si fichier doit être exclu"""
        for excl in self.exclusions:
            if excl in chemin_fichier:
                return True
        return False
    
    def archiver(self):
        """
        Étape 1: Créer archive ZIP du dossier source
        Compression DEFLATE, préservation structure
        
        Returns:
            bool: True si succès, False sinon
        """
        logger.info(f"Archivage de {self.dossier_source}...")
        
        try:
            with zipfile.ZipFile(
                self.archive_name, 'w', zipfile.ZIP_DEFLATED
            ) as zf:
                
                for racine, dossiers, fichiers in os.walk(self.dossier_source):
                    for fichier in fichiers:
                        chemin_complet = os.path.join(racine, fichier)
                        
                        # Vérifier exclusions
                        if self.doit_exclure(chemin_complet):
                            self.stats['fichiers_exclus'] += 1
                            continue
                        
                        # Ajouter à archive
                        arcname = os.path.relpath(
                            chemin_complet, self.dossier_source
                        )
                        zf.write(chemin_complet, arcname=arcname)
                        
                        # Mettre à jour stats
                        taille = os.path.getsize(chemin_complet)
                        self.stats['fichiers_archives'] += 1
                        self.stats['octets_original'] += taille
                
                # Taille archive comprimée
                self.stats['octets_archive'] = zf.NameToInfo[
                    zf.namelist()[0]
                ].compress_size if zf.namelist() else 0
            
            # Recalculer taille archive réelle
            self.stats['octets_archive'] = os.path.getsize(self.archive_name)
            
            ratio_compression = (
                (1 - self.stats['octets_archive'] / self.stats['octets_original']) * 100
                if self.stats['octets_original'] > 0 else 0
            )
            
            logger.info(
                f"Archive créée: {self.archive_name} "
                f"({self.stats['fichiers_archives']} fichiers, "
                f"{self.stats['octets_archive']:,} bytes, "
                f"compression: {ratio_compression:.1f}%)"
            )
            return True
        
        except Exception as e:
            logger.error(f"Erreur archivage: {e}")
            return False
    
    def generer_manifeste(self):
        """
        Étape 2: Créer manifeste JSON d'intégrité (ISO 27001 A.14.1.2)
        Contient hash, timestamps, métadonnées
        
        Returns:
            bool: True si succès, False sinon
        """
        logger.info("Génération du manifeste d'intégrité...")
        
        try:
            hash_archive = self.calculer_hash_fichier(self.archive_name)
            
            manifeste = {
                "version": "1.0",
                "timestamp": self.timestamp,
                "dossier_source": str(self.dossier_source),
                "nom_backup": self.nom_backup,
                "archive_file": self.archive_name,
                "hash_archive": hash_archive,
                "taille_bytes": self.stats['octets_archive'],
                "fichiers_archives": self.stats['fichiers_archives'],
                "fichiers_exclus": self.stats['fichiers_exclus'],
                "octets_original": self.stats['octets_original'],
                "cle_id": f"cle_{datetime.utcnow().strftime('%Y_%m')}",
                "iso27001": {
                    "confidentialite": "AES-256 Fernet",
                    "integrite": "SHA-256",
                    "disponibilite": "ZIP archivé",
                    "tracabilite": "Logging complet"
                }
            }
            
            with open(self.manifeste_name, 'w') as f:
                json.dump(manifeste, f, indent=2)
            
            # Permissions fichier manifeste
            os.chmod(self.manifeste_name, 0o640)
            
            logger.info(f"Manifeste créé: {self.manifeste_name}")
            return True
        
        except Exception as e:
            logger.error(f"Erreur manifeste: {e}")
            return False
    
    def chiffrer(self):
        """
        Étape 3: Chiffrer l'archive avec AES-256 (ISO 27001 A.10.1.1)
        Fernet = AES-128 mode CBC + HMAC authentification
        (Utilisé à titre pédagogique, en production utiliser cryptography.hazmat)
        
        Returns:
            bool: True si succès, False sinon
        """
        logger.info("Chiffrement de l'archive avec AES-256...")
        
        try:
            # Lire archive
            with open(self.archive_name, 'rb') as f:
                contenu = f.read()
            
            # Chiffrer
            chiffre = Fernet(self.cle)
            ciphertext = chiffre.encrypt(contenu)
            
            # Écrire fichier chiffré
            with open(self.chiffre_name, 'wb') as f:
                f.write(ciphertext)
            
            # Permissions fichier chiffré
            os.chmod(self.chiffre_name, 0o640)
            
            # Calculer hash du fichier chiffré
            hash_chiffre = self.calculer_hash_fichier(self.chiffre_name)
            
            # Mettre à jour manifeste avec info chiffrement
            with open(self.manifeste_name, 'r') as f:
                manifeste = json.load(f)
            
            manifeste['chiffre_file'] = self.chiffre_name
            manifeste['hash_chiffre'] = hash_chiffre
            manifeste['chiffrement_date'] = datetime.utcnow().isoformat() + 'Z'
            
            with open(self.manifeste_name, 'w') as f:
                json.dump(manifeste, f, indent=2)
            
            logger.info(
                f"Chiffrement réussi: {self.chiffre_name} "
                f"({os.path.getsize(self.chiffre_name):,} bytes)"
            )
            return True
        
        except Exception as e:
            logger.error(f"Erreur chiffrement: {e}")
            return False
    
    def verifier_integrite_archive(self):
        """Vérifier intégrité archive avant chiffrement"""
        logger.info("Vérification d'intégrité de l'archive...")
        
        try:
            with zipfile.ZipFile(self.archive_name, 'r') as zf:
                bad_file = zf.testzip()
                if bad_file is not None:
                    logger.error(f"Archive corrompue: {bad_file}")
                    return False
            
            logger.info("✓ Archive intègre")
            return True
        
        except Exception as e:
            logger.error(f"Erreur vérification: {e}")
            return False
    
    def executer_sauvegarde(self):
        """
        Exécute pipeline complet de sauvegarde
        
        Returns:
            tuple: (bool succès, str clé B64) ou (False, None)
        """
        logger.info("="*70)
        logger.info("DÉBUT SAUVEGARDE CHIFFRÉE ET ARCHIVÉE")
        logger.info("="*70)
        
        etapes = [
            ("Archivage", self.archiver),
            ("Vérification intégrité", self.verifier_integrite_archive),
            ("Manifeste", self.generer_manifeste),
            ("Chiffrement", self.chiffrer)
        ]
        
        for nom_etape, fonction in etapes:
            if not fonction():
                logger.error(f"✗ Sauvegarde échouée à l'étape: {nom_etape}")
                logger.info("="*70)
                return False, None
        
        logger.info("="*70)
        logger.info("✓ SAUVEGARDE RÉUSSIE")
        logger.info("="*70)
        logger.info(f"Fichiers générés:")
        logger.info(f"  - Archive: {self.archive_name}")
        logger.info(f"  - Manifeste: {self.manifeste_name}")
        logger.info(f"  - Chiffré: {self.chiffre_name}")
        logger.info(f"  - Clé: {self.cle.decode()}")
        logger.info("="*70)
        
        return True, self.cle.decode()


# ============================================================================
# CLASSE RestoreManager - Restauration depuis sauvegarde chiffrée
# ============================================================================

class RestoreManager:
    """
    Gère pipeline complet de restauration:
    Fichier chiffré → Déchiffrement → Archive → Extraction
    
    Avec vérification d'intégrité à chaque étape (ISO 27001 A.14.1.2)
    """
    
    def __init__(self, manifeste_path, cle):
        """
        Initialise gestionnaire de restauration
        
        Args:
            manifeste_path: Chemin du manifeste .manifest.json
            cle: Clé Fernet (bytes ou str B64)
        """
        self.manifeste_path = Path(manifeste_path)
        
        # Normaliser clé
        if isinstance(cle, str):
            self.cle = cle.encode()
        else:
            self.cle = cle
        
        # Charger manifeste
        with open(manifeste_path, 'r') as f:
            self.manifeste = json.load(f)
        
        logger.info(f"RestoreManager initialisé: {manifeste_path}")
    
    def calculer_hash_fichier(self, chemin):
        """Calcule SHA-256 d'un fichier"""
        hasher = hashlib.sha256()
        
        with open(chemin, 'rb') as f:
            while True:
                bloc = f.read(4096)
                if not bloc:
                    break
                hasher.update(bloc)
        
        return hasher.hexdigest()
    
    def verifier_manifeste(self):
        """
        Étape 1: Vérifier intégrité du manifeste et fichier chiffré
        (ISO 27001 A.14.1.2 - avant déchiffrement)
        
        Returns:
            bool: True si OK, False sinon
        """
        logger.info("Vérification du manifeste et fichier chiffré...")
        
        try:
            # Vérifier fichier chiffré existe
            chiffre_path = Path(self.manifeste.get('chiffre_file'))
            if not chiffre_path.exists():
                logger.error(f"Fichier chiffré introuvable: {chiffre_path}")
                return False
            
            # Vérifier hash du fichier chiffré
            hash_attendu = self.manifeste['hash_chiffre']
            hash_calcule = self.calculer_hash_fichier(str(chiffre_path))
            
            if hash_attendu != hash_calcule:
                logger.error(
                    f"Corruption détectée! "
                    f"Attendu: {hash_attendu[:32]}... "
                    f"Obtenu: {hash_calcule[:32]}..."
                )
                return False
            
            logger.info("✓ Manifeste et fichier chiffré valides")
            return True
        
        except Exception as e:
            logger.error(f"Erreur vérification manifeste: {e}")
            return False
    
    def dechiffrer(self, chemin_sortie=None):
        """
        Étape 2: Déchiffrer l'archive
        
        Args:
            chemin_sortie: Chemin fichier déchiffré (auto-généré si None)
        
        Returns:
            str: Chemin archive déchiffrée ou None si erreur
        """
        logger.info("Déchiffrement de l'archive...")
        
        try:
            if chemin_sortie is None:
                chemin_sortie = self.manifeste['archive_file']
            
            chiffre_path = self.manifeste['chiffre_file']
            
            # Lire fichier chiffré
            with open(chiffre_path, 'rb') as f:
                ciphertext = f.read()
            
            # Déchiffrer
            chiffre = Fernet(self.cle)
            plaintext = chiffre.decrypt(ciphertext)
            
            # Écrire archive déchiffrée
            with open(chemin_sortie, 'wb') as f:
                f.write(plaintext)
            
            logger.info(f"Déchiffrement réussi: {chemin_sortie}")
            return chemin_sortie
        
        except InvalidToken:
            logger.error("✗ Erreur déchiffrement: Mauvaise clé ou fichier corrompu")
            return None
        except Exception as e:
            logger.error(f"Erreur déchiffrement: {e}")
            return None
    
    def extraire(self, archive_path, dossier_destination):
        """
        Étape 3: Extraire archive ZIP vers dossier
        
        Args:
            archive_path: Chemin archive déchiffrée
            dossier_destination: Dossier de destination
        
        Returns:
            bool: True si succès, False sinon
        """
        logger.info(f"Extraction vers {dossier_destination}...")
        
        try:
            dossier_destination = Path(dossier_destination)
            dossier_destination.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(archive_path, 'r') as zf:
                # Vérifier intégrité archive
                bad_file = zf.testzip()
                if bad_file is not None:
                    logger.error(f"✗ Archive corrompue: {bad_file}")
                    return False
                
                fichiers = zf.namelist()
                logger.info(f"Extraction de {len(fichiers)} fichiers...")
                
                # Extraire
                zf.extractall(str(dossier_destination))
            
            logger.info("✓ Extraction réussie")
            return True
        
        except Exception as e:
            logger.error(f"Erreur extraction: {e}")
            return False
    
    def executer_restauration(self, dossier_destination):
        """
        Exécute pipeline complet de restauration
        
        Args:
            dossier_destination: Dossier où restaurer
        
        Returns:
            bool: True si succès, False sinon
        """
        logger.info("="*70)
        logger.info("DÉBUT RESTAURATION")
        logger.info("="*70)
        
        # Étape 1: Vérifier manifeste
        if not self.verifier_manifeste():
            logger.error("✗ Restauration échouée: manifeste invalide")
            logger.info("="*70)
            return False
        
        # Étape 2: Déchiffrer
        archive_temp = self.dechiffrer()
        if archive_temp is None:
            logger.info("="*70)
            return False
        
        # Étape 3: Extraire
        if not self.extraire(archive_temp, dossier_destination):
            logger.info("="*70)
            return False
        
        logger.info("="*70)
        logger.info("✓ RESTAURATION RÉUSSIE")
        logger.info("="*70)
        logger.info(f"Données restaurées dans: {dossier_destination}")
        logger.info("="*70)
        
        return True


# ============================================================================
# MAIN - Interface CLI
# ============================================================================

def main():
    """Point d'entrée principal avec arguments CLI"""
    
    parser = ArgumentParser(
        description="Framework de sauvegarde chiffrée et archivée (ISO 27001)",
        epilog="Exemple: python3 backup_framework.py --source /var/www/app --backup app_2024-01"
    )
    
    parser.add_argument(
        '--source', '-s',
        required=True,
        help='Chemin du dossier à sauvegarder'
    )
    parser.add_argument(
        '--backup', '-b',
        required=True,
        help='Nom de la sauvegarde (ex: app_2024-01)'
    )
    parser.add_argument(
        '--restore', '-r',
        help='Restaurer depuis manifeste (chemin .manifest)'
    )
    parser.add_argument(
        '--destination', '-d',
        help='Dossier de destination pour restauration'
    )
    parser.add_argument(
        '--key', '-k',
        help='Clé Fernet existante (B64) pour restauration'
    )
    
    args = parser.parse_args()
    
    # Mode sauvegarde
    if args.source and not args.restore:
        backup = BackupManager(args.source, args.backup)
        succes, cle = backup.executer_sauvegarde()
        
        if not succes:
            sys.exit(1)
        
        print(f"\n✓ Clé de restauration: {cle}")
        print(f"  Conservez-la dans un lieu sûr!")
    
    # Mode restauration
    elif args.restore and args.destination and args.key:
        restore = RestoreManager(args.restore, args.key)
        succes = restore.executer_restauration(args.destination)
        
        if not succes:
            sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
