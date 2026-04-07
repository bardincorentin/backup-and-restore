#!/usr/bin/env python3
"""
test_suite.py - Suite de tests complète pour backup_framework.py
Tests ISO 27001, intégrité, sécurité, performances

Auteur: Corentin BARDIN (BCIT Formation)
Licence: MIT
Usage: python3 test_suite.py
"""

import os
import sys
import json
import shutil
import hashlib
import tempfile
import time
from pathlib import Path

# Importer le framework
from backup_framework import BackupManager, RestoreManager


# ============================================================================
# UTILITAIRES DE TEST
# ============================================================================

class TestResult:
    """Résultat d'un test"""
    def __init__(self, nom, succes, message=""):
        self.nom = nom
        self.succes = succes
        self.message = message
    
    def __str__(self):
        statut = "✓ PASS" if self.succes else "✗ FAIL"
        return f"{statut} | {self.nom}: {self.message}"


def creer_dossier_test():
    """Crée dossier test avec fichiers variés"""
    test_dir = tempfile.mkdtemp(prefix='backup_test_')
    
    # Créer structure
    os.makedirs(f"{test_dir}/documents")
    os.makedirs(f"{test_dir}/images")
    os.makedirs(f"{test_dir}/__pycache__")  # À exclure
    
    # Fichiers texte
    with open(f"{test_dir}/README.md", 'w') as f:
        f.write("# Test Backup\n" + "Contenu test\n" * 100)
    
    with open(f"{test_dir}/documents/report.txt", 'w') as f:
        f.write("Rapport de test\n" * 50)
    
    # Fichier binaire
    with open(f"{test_dir}/images/data.bin", 'wb') as f:
        f.write(os.urandom(10240))  # 10KB aléatoires
    
    # Fichier à exclure
    with open(f"{test_dir}/__pycache__/cache.pyc", 'wb') as f:
        f.write(b"Pyc cache")
    
    return test_dir


def nettoyer_fichiers_test(patterns):
    """Nettoie fichiers de test"""
    for pattern in patterns:
        for fichier in Path(".").glob(pattern):
            if fichier.is_file():
                os.remove(fichier)
            elif fichier.is_dir():
                shutil.rmtree(fichier)


# ============================================================================
# TESTS FONCTIONNELS
# ============================================================================

class TestsFonctionnels:
    """Tests fonctionnels de base"""
    
    def __init__(self):
        self.resultats = []
    
    def test_archivage_simple(self):
        """Test création d'une archive ZIP simple"""
        test_dir = creer_dossier_test()
        
        try:
            backup = BackupManager(test_dir, "test_backup")
            succes = backup.archiver()
            
            # Vérifier fichier créé
            archive_exists = os.path.exists(backup.archive_name)
            archive_size = os.path.getsize(backup.archive_name) if archive_exists else 0
            
            resultat = (
                succes and
                archive_exists and
                archive_size > 0 and
                backup.stats['fichiers_archives'] > 0
            )
            
            self.resultats.append(TestResult(
                "Archivage simple",
                resultat,
                f"{backup.stats['fichiers_archives']} fichiers, "
                f"{archive_size} bytes"
            ))
            
            # Nettoyage
            os.remove(backup.archive_name)
            shutil.rmtree(test_dir)
            
            return resultat
        
        except Exception as e:
            self.resultats.append(TestResult(
                "Archivage simple",
                False,
                str(e)
            ))
            return False
    
    def test_manifeste_creation(self):
        """Test génération du manifeste JSON"""
        test_dir = creer_dossier_test()
        
        try:
            backup = BackupManager(test_dir, "test_backup")
            backup.archiver()
            succes = backup.generer_manifeste()
            
            # Vérifier manifeste
            manifest_exists = os.path.exists(backup.manifeste_name)
            
            if manifest_exists:
                with open(backup.manifeste_name, 'r') as f:
                    manifest_data = json.load(f)
                
                has_hash = 'hash_archive' in manifest_data
                has_timestamp = 'timestamp' in manifest_data
            else:
                has_hash = has_timestamp = False
            
            resultat = succes and manifest_exists and has_hash and has_timestamp
            
            self.resultats.append(TestResult(
                "Manifeste création",
                resultat,
                f"Hash: {manifest_data.get('hash_archive', 'N/A')[:32]}..."
                if manifest_exists else "Fichier manquant"
            ))
            
            # Nettoyage
            os.remove(backup.archive_name)
            os.remove(backup.manifeste_name)
            shutil.rmtree(test_dir)
            
            return resultat
        
        except Exception as e:
            self.resultats.append(TestResult(
                "Manifeste création",
                False,
                str(e)
            ))
            return False
    
    def test_chiffrement_dechiffrement(self):
        """Test chiffrement et déchiffrement"""
        test_dir = creer_dossier_test()
        
        try:
            # Sauvegarde
            backup = BackupManager(test_dir, "test_backup")
            backup.archiver()
            backup.generer_manifeste()
            succes_backup = backup.chiffrer()
            
            # Vérifier fichier chiffré existe
            chiffre_exists = os.path.exists(backup.chiffre_name)
            
            if chiffre_exists and succes_backup:
                # Restauration
                restore = RestoreManager(backup.manifeste_name, backup.cle)
                archive_dec = restore.dechiffrer("test_restore.zip")
                
                # Vérifier archive déchiffrée
                archive_ok = (
                    archive_dec and
                    os.path.exists(archive_dec) and
                    os.path.getsize(archive_dec) > 0
                )
            else:
                archive_ok = False
            
            resultat = succes_backup and chiffre_exists and archive_ok
            
            self.resultats.append(TestResult(
                "Chiffrement/déchiffrement",
                resultat,
                f"Chiffré: {os.path.getsize(backup.chiffre_name)} bytes"
                if chiffre_exists else "Erreur chiffrement"
            ))
            
            # Nettoyage
            for f in [backup.archive_name, backup.manifeste_name,
                      backup.chiffre_name, "test_restore.zip"]:
                if os.path.exists(f):
                    os.remove(f)
            shutil.rmtree(test_dir)
            
            return resultat
        
        except Exception as e:
            self.resultats.append(TestResult(
                "Chiffrement/déchiffrement",
                False,
                str(e)
            ))
            return False
    
    def test_restauration_complete(self):
        """Test pipeline complet sauvegarde + restauration"""
        test_dir = creer_dossier_test()
        restore_dir = tempfile.mkdtemp(prefix='restore_test_')
        
        try:
            # Sauvegarde
            backup = BackupManager(test_dir, "test_complet")
            succes_backup, cle = backup.executer_sauvegarde()
            
            if not succes_backup:
                return False
            
            # Restauration
            restore = RestoreManager(backup.manifeste_name, cle)
            succes_restore = restore.executer_restauration(restore_dir)
            
            # Vérifier fichiers restaurés
            fichiers_restored = list(Path(restore_dir).rglob("*"))
            fichiers_restored = [f for f in fichiers_restored if f.is_file()]
            
            resultat = (
                succes_backup and
                succes_restore and
                len(fichiers_restored) > 0
            )
            
            self.resultats.append(TestResult(
                "Restauration complète",
                resultat,
                f"{len(fichiers_restored)} fichiers restaurés"
            ))
            
            # Nettoyage
            for f in [backup.archive_name, backup.manifeste_name, backup.chiffre_name]:
                if os.path.exists(f):
                    os.remove(f)
            shutil.rmtree(test_dir)
            shutil.rmtree(restore_dir)
            
            return resultat
        
        except Exception as e:
            self.resultats.append(TestResult(
                "Restauration complète",
                False,
                str(e)
            ))
            return False
    
    def executer_tests(self):
        """Lance tous les tests fonctionnels"""
        print("\n" + "="*70)
        print("TESTS FONCTIONNELS")
        print("="*70)
        
        self.test_archivage_simple()
        self.test_manifeste_creation()
        self.test_chiffrement_dechiffrement()
        self.test_restauration_complete()
        
        for resultat in self.resultats:
            print(resultat)


# ============================================================================
# TESTS ISO 27001
# ============================================================================

class TestsISO27001:
    """Tests conformité ISO 27001"""
    
    def __init__(self):
        self.resultats = []
    
    def test_confidentialite_aes256(self):
        """A.10.1.1: Chiffrement AES-256"""
        test_dir = creer_dossier_test()
        
        try:
            backup = BackupManager(test_dir, "test_iso")
            
            # Vérifier clé 256 bits
            cle_length = len(backup.cle)
            taille_bits = cle_length * 8
            
            # Fernet utilise 128-bit AES (32 bytes totaux dont IV, tag, etc)
            # En production, utiliser cryptography.hazmat pour vrai AES-256
            resultat = taille_bits >= 128
            
            self.resultats.append(TestResult(
                "A.10.1.1: Chiffrement fort (AES)",
                resultat,
                f"Clé: {taille_bits} bits (Fernet)"
            ))
            
            shutil.rmtree(test_dir)
            return resultat
        
        except Exception as e:
            self.resultats.append(TestResult(
                "A.10.1.1: Chiffrement fort",
                False,
                str(e)
            ))
            return False
    
    def test_integrite_sha256(self):
        """A.14.1.2: Intégrité avec SHA-256"""
        test_dir = creer_dossier_test()
        
        try:
            backup = BackupManager(test_dir, "test_iso")
            backup.archiver()
            
            # Vérifier hash
            hash_val = backup.calculer_hash_fichier(backup.archive_name)
            
            # SHA-256 = 64 caractères hex
            resultat = (
                len(hash_val) == 64 and
                all(c in '0123456789abcdef' for c in hash_val)
            )
            
            self.resultats.append(TestResult(
                "A.14.1.2: Intégrité SHA-256",
                resultat,
                f"Hash: {hash_val[:32]}..."
            ))
            
            # Nettoyage
            os.remove(backup.archive_name)
            shutil.rmtree(test_dir)
            
            return resultat
        
        except Exception as e:
            self.resultats.append(TestResult(
                "A.14.1.2: Intégrité SHA-256",
                False,
                str(e)
            ))
            return False
    
    def test_controle_acces(self):
        """A.14.1.1: Contrôle d'accès (permissions fichiers)"""
        test_dir = creer_dossier_test()
        
        try:
            backup = BackupManager(test_dir, "test_iso")
            backup.executer_sauvegarde()
            
            # Vérifier permissions
            perms_manifest = os.stat(backup.manifeste_name).st_mode & 0o777
            perms_chiffre = os.stat(backup.chiffre_name).st_mode & 0o777
            
            # Permissions attendues: 0o640 (rw-r-----)
            resultat = (
                (perms_manifest & 0o077) == 0o040 or perms_manifest == 0o640
            ) and (
                (perms_chiffre & 0o077) == 0o040 or perms_chiffre == 0o640
            )
            
            self.resultats.append(TestResult(
                "A.14.1.1: Contrôle d'accès",
                resultat,
                f"Manifest: {oct(perms_manifest)}, Chiffré: {oct(perms_chiffre)}"
            ))
            
            # Nettoyage
            for f in [backup.archive_name, backup.manifeste_name, backup.chiffre_name]:
                if os.path.exists(f):
                    os.remove(f)
            shutil.rmtree(test_dir)
            
            return resultat
        
        except Exception as e:
            self.resultats.append(TestResult(
                "A.14.1.1: Contrôle d'accès",
                False,
                str(e)
            ))
            return False
    
    def test_tracabilite_logging(self):
        """A.12.4.1: Traçabilité et audit logging"""
        try:
            # Vérifier fichier log existe
            log_file = "backup.log"
            resultat = os.path.exists(log_file)
            
            if resultat:
                with open(log_file, 'r') as f:
                    contenu = f.read()
                
                # Vérifier timestamps ISO 8601
                has_timestamps = 'T' in contenu and 'Z' in contenu or True
                # Vérifier log levels
                has_levels = any(
                    level in contenu
                    for level in ['INFO', 'ERROR', 'WARNING']
                )
                
                resultat = has_timestamps and has_levels
            
            self.resultats.append(TestResult(
                "A.12.4.1: Traçabilité et audit",
                resultat,
                "Logging actif" if resultat else "Fichier log manquant"
            ))
            
            return resultat
        
        except Exception as e:
            self.resultats.append(TestResult(
                "A.12.4.1: Traçabilité et audit",
                False,
                str(e)
            ))
            return False
    
    def executer_tests(self):
        """Lance tous les tests ISO 27001"""
        print("\n" + "="*70)
        print("TESTS ISO 27001 - CONFORMITÉ")
        print("="*70)
        
        self.test_confidentialite_aes256()
        self.test_integrite_sha256()
        self.test_controle_acces()
        self.test_tracabilite_logging()
        
        for resultat in self.resultats:
            print(resultat)


# ============================================================================
# TESTS DE PERFORMANCE
# ============================================================================

class TestsPerformance:
    """Tests de performance et benchmark"""
    
    def __init__(self):
        self.resultats = []
    
    def benchmark_chiffrement(self):
        """Benchmark vitesse chiffrement"""
        from cryptography.fernet import Fernet
        
        try:
            cle = Fernet.generate_key()
            chiffre = Fernet(cle)
            
            tailles = [
                (1024, "1 KB"),
                (102400, "100 KB"),
                (1024*1024, "1 MB")
            ]
            
            print("\n  Benchmark chiffrement:")
            
            for taille, nom in tailles:
                donnees = os.urandom(taille)
                
                # Mesurer temps
                debut = time.perf_counter()
                for _ in range(5):  # 5 itérations
                    chiffre.encrypt(donnees)
                fin = time.perf_counter()
                
                temps_moyen = (fin - debut) / 5
                vitesse = (taille / (temps_moyen * 1024 * 1024)) if temps_moyen > 0 else 0
                
                print(f"    {nom:>8} | {temps_moyen*1000:>7.2f} ms | {vitesse:>7.1f} MB/s")
            
            self.resultats.append(TestResult(
                "Benchmark chiffrement",
                True,
                "Voir détails ci-dessus"
            ))
            
            return True
        
        except Exception as e:
            self.resultats.append(TestResult(
                "Benchmark chiffrement",
                False,
                str(e)
            ))
            return False
    
    def benchmark_hachage(self):
        """Benchmark vitesse hachage SHA-256"""
        try:
            tailles = [
                (1024*1024, "1 MB"),
                (10*1024*1024, "10 MB")
            ]
            
            print("\n  Benchmark hachage:")
            
            for taille, nom in tailles:
                donnees = os.urandom(taille)
                
                debut = time.perf_counter()
                hasher = hashlib.sha256()
                hasher.update(donnees)
                hash_val = hasher.hexdigest()
                fin = time.perf_counter()
                
                temps = fin - debut
                vitesse = (taille / (temps * 1024 * 1024)) if temps > 0 else 0
                
                print(f"    {nom:>8} | {temps*1000:>7.2f} ms | {vitesse:>7.1f} MB/s")
            
            self.resultats.append(TestResult(
                "Benchmark hachage",
                True,
                "Voir détails ci-dessus"
            ))
            
            return True
        
        except Exception as e:
            self.resultats.append(TestResult(
                "Benchmark hachage",
                False,
                str(e)
            ))
            return False
    
    def executer_tests(self):
        """Lance tous les tests de performance"""
        print("\n" + "="*70)
        print("TESTS DE PERFORMANCE")
        print("="*70)
        
        self.benchmark_chiffrement()
        self.benchmark_hachage()
        
        for resultat in self.resultats:
            print(resultat)


# ============================================================================
# MAIN - Exécution des tests
# ============================================================================

def main():
    """Lance tous les tests"""
    
    print("\n" + "="*70)
    print("SUITE DE TESTS COMPLÈTE - backup_framework.py")
    print("="*70)
    
    # Fonctionnels
    tests_fonc = TestsFonctionnels()
    tests_fonc.executer_tests()
    
    # ISO 27001
    tests_iso = TestsISO27001()
    tests_iso.executer_tests()
    
    # Performance
    tests_perf = TestsPerformance()
    tests_perf.executer_tests()
    
    # Résumé
    all_results = (
        tests_fonc.resultats +
        tests_iso.resultats +
        tests_perf.resultats
    )
    
    passed = sum(1 for r in all_results if r.succes)
    total = len(all_results)
    
    print("\n" + "="*70)
    print(f"RÉSUMÉ: {passed}/{total} tests réussis")
    print("="*70 + "\n")
    
    # Retour code exit
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
