#!/bin/bash
##############################################################################
# setup.sh — Automatisation du setup du projet
#
# Usage: chmod +x setup.sh && ./setup.sh
#
# Actions:
#   1. Vérifier Python 3.9+
#   2. Créer venv (optionnel)
#   3. Installer cryptography
#   4. Copier .env.example → .env
#   5. Tester import cryptography
#   6. Lancer test_suite.py (sanity check)
##############################################################################

set -e  # Exit on error

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

# Helpers
log_info() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

##############################################################################
# 1. Vérifier Python 3.9+
##############################################################################
echo ""
echo "==================================================================="
echo "Backup & Restore Framework - Setup"
echo "==================================================================="
echo ""

log_info "Checking Python version..."

python_version=$(python3 --version 2>&1 | awk '{print $2}')
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [[ $python_major -lt 3 ]] || [[ $python_major -eq 3 && $python_minor -lt 9 ]]; then
    log_error "Python 3.9+ required, found $python_version"
    exit 1
fi

log_info "Python $python_version installed ✓"

##############################################################################
# 2. Créer venv (optionnel)
##############################################################################
if [[ ! -d "venv" ]]; then
    log_warn "Virtual environment not found"
    read -p "Create venv? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Creating venv..."
        python3 -m venv venv
        log_info "Venv created ✓"
        log_info "Activate with: source venv/bin/activate"
    fi
fi

##############################################################################
# 3. Installer cryptography
##############################################################################
log_info "Installing dependencies..."

if pip3 list | grep -q cryptography; then
    crypto_version=$(pip show cryptography 2>/dev/null | grep Version | awk '{print $2}')
    log_info "cryptography $crypto_version already installed"
else
    log_warn "Installing cryptography..."
    pip install --upgrade pip > /dev/null 2>&1
    pip install cryptography >= 40.0.0
    log_info "cryptography installed ✓"
fi

##############################################################################
# 4. Copier .env.example → .env
##############################################################################
if [[ ! -f ".env" ]]; then
    if [[ -f ".env.example" ]]; then
        log_info "Copying .env.example → .env"
        cp .env.example .env
        log_warn "Edit .env with your configuration"
    fi
fi

##############################################################################
# 5. Tester import cryptography
##############################################################################
log_info "Testing cryptography import..."

if python3 -c "import cryptography; print(f'cryptography {cryptography.__version__}')" 2>/dev/null; then
    log_info "Cryptography import successful ✓"
else
    log_error "Failed to import cryptography"
    exit 1
fi

##############################################################################
# 6. Créer dossier test_data/
##############################################################################
if [[ ! -d "test_data" ]]; then
    log_info "Creating test_data directory..."
    mkdir -p test_data/documents
    mkdir -p test_data/images

    # Créer fichiers test
    echo "# Test Backup Structure" > test_data/README.md
    echo "Test document" > test_data/documents/report.txt
    dd if=/dev/urandom of=test_data/images/data.bin bs=1024 count=10 2>/dev/null

    log_info "test_data created ✓"
fi

##############################################################################
# 7. Lancer test_suite.py (sanity check)
##############################################################################
echo ""
log_info "Running sanity check tests..."
echo ""

if [[ -f "test_suite.py" ]]; then
    if python3 test_suite.py 2>&1 | tail -20; then
        echo ""
        log_info "All tests passed ✓"
    else
        log_warn "Some tests failed (see output above)"
        exit 1
    fi
else
    log_error "test_suite.py not found"
    exit 1
fi

##############################################################################
# 8. Summary
##############################################################################
echo ""
echo "==================================================================="
echo "Setup Complete ✓"
echo "==================================================================="
echo ""

cat << EOF
🎉 Environment ready!

Next steps:
  1. Review configuration:
     cat .env

  2. Create your first backup:
     python3 backup_framework.py \\
       --source /path/to/backup \\
       --backup my_backup_2024-01

  3. View logs:
     tail -f backup.log

  4. Read documentation:
     cat README.md

  5. Commit & push:
     git add .
     git commit -m "chore: initial setup"
     git push origin

For help: python3 backup_framework.py --help
EOF

echo ""
