#!/usr/bin/env python3
"""
validate_bundle.py — Validateur local de bundle Codabench
Créé par Claude. 
=========================================================
Reproduit fidèlement les contrôles effectués par Codabench lors de l'upload
d'un bundle.zip pour créer une compétition (couches 1 à 3 + règles métier
des sérialiseurs DRF), sans aucune dépendance Django.

Dépendances :
    pip install pyyaml python-dateutil

Usage :
    python validate_bundle.py mon_bundle.zip
    python validate_bundle.py mon_bundle.zip --verbose
    python validate_bundle.py mon_bundle.zip --version 2    # forcer la version
"""

import argparse
import datetime
import os
import sys
import tempfile
import uuid
import zipfile
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# ── Dépendances externes légères ─────────────────────────────────────────────
try:
    import yaml
except ImportError:
    sys.exit("PyYAML manquant : pip install pyyaml")

try:
    from dateutil import parser as dateutil_parser
except ImportError:
    sys.exit("python-dateutil manquant : pip install python-dateutil")

# ═══════════════════════════════════════════════════════════════════════════════
# Résultat de validation
# ═══════════════════════════════════════════════════════════════════════════════

COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def c(color: str, text: str) -> str:
    """Applique une couleur ANSI si le terminal le supporte."""
    if sys.stdout.isatty():
        return f"{COLORS[color]}{text}{COLORS['reset']}"
    return text


@dataclass
class ValidationResult:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def ok(self, msg: str):
        self.info.append(msg)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def print_summary(self, verbose: bool = False):
        print()
        if verbose or self.errors:
            for msg in self.errors:
                print(f"  {c('red', '✗')} {msg}")
        if verbose:
            for msg in self.warnings:
                print(f"  {c('yellow', '⚠')} {msg}")
            for msg in self.info:
                print(f"  {c('green', '✓')} {msg}")

        print()
        summary_errors   = f"{len(self.errors)} erreur(s)"
        summary_warnings = f"{len(self.warnings)} avertissement(s)"
        if self.is_valid:
            print(c("green", c("bold", f"Bundle valide — {summary_errors}, {summary_warnings}")))
        else:
            print(c("red", c("bold", f"Bundle invalide — {summary_errors}, {summary_warnings}")))
        print()


# ═══════════════════════════════════════════════════════════════════════════════
# Utilitaires
# ═══════════════════════════════════════════════════════════════════════════════

def get_datetime(field_val) -> Optional[datetime.datetime]:
    """Reproduit utils.get_datetime() de Codabench."""
    if not field_val:
        return None
    if isinstance(field_val, datetime.date) and not isinstance(field_val, datetime.datetime):
        field_val = datetime.datetime.combine(field_val, datetime.time())
    elif not isinstance(field_val, datetime.datetime):
        try:
            field_val = dateutil_parser.parse(str(field_val))
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Date invalide : {field_val!r} — {exc}") from exc
    # Ajoute un timezone si absent (utc+0 pour la comparaison locale)
    if field_val.tzinfo is None:
        field_val = field_val.replace(tzinfo=datetime.timezone.utc)
    return field_val


def looks_like_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
        return True
    except (ValueError, AttributeError):
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# COUCHE 1 — Intégrité ZIP + competition.yaml
# ═══════════════════════════════════════════════════════════════════════════════

def check_zip_and_yaml(
    bundle_path: str,
    temp_dir: str,
    result: ValidationResult,
) -> Optional[Dict[str, Any]]:
    """
    Extrait le ZIP et parse competition.yaml.
    Retourne le dict YAML ou None si une erreur bloquante est rencontrée.
    """
    # ── Intégrité ZIP ──────────────────────────────────────────────────────────
    try:
        with zipfile.ZipFile(bundle_path, "r") as zf:
            zf.extractall(temp_dir)
        result.ok("ZIP intact et extractible")
    except zipfile.BadZipFile:
        result.error("Fichier ZIP corrompu (BadZipFile)")
        return None
    except Exception as exc:
        result.error(f"Erreur lors de l'extraction du ZIP : {exc}")
        return None

    # ── Présence de competition.yaml ───────────────────────────────────────────
    yaml_path = os.path.join(temp_dir, "competition.yaml")
    if not os.path.exists(yaml_path):
        result.error(
            "competition.yaml introuvable à la racine du ZIP. "
            "Vérifiez que le fichier est bien à la racine (pas dans un sous-dossier)."
        )
        return None
    result.ok("competition.yaml présent à la racine")

    # ── Parsing YAML ──────────────────────────────────────────────────────────
    try:
        with open(yaml_path, encoding="utf-8") as f:
            competition_yaml = yaml.safe_load(f.read())
    except yaml.YAMLError as exc:
        result.error(f"Erreur de syntaxe YAML dans competition.yaml : {exc}")
        return None
    except Exception as exc:
        result.error(f"Impossible de lire competition.yaml : {exc}")
        return None

    if not isinstance(competition_yaml, dict):
        result.error("competition.yaml ne contient pas un dictionnaire YAML valide")
        return None

    result.ok("competition.yaml parsé avec succès")
    return competition_yaml


# ═══════════════════════════════════════════════════════════════════════════════
# COUCHE 2 — Sélection de version
# ═══════════════════════════════════════════════════════════════════════════════

def detect_version(competition_yaml: Dict, result: ValidationResult) -> Optional[str]:
    """Reproduit la sélection de V2Unpacker / V15Unpacker dans tasks.py."""
    version = str(competition_yaml.get("version", "1"))
    if version in ("1", "1.5"):
        result.ok(f"Version détectée : {version} (format legacy CodaLab)")
        return version
    elif version == "2":
        result.ok("Version détectée : 2 (format Codabench natif)")
        return version
    else:
        result.error(
            f"Version YAML '{version}' non supportée. "
            "Valeurs acceptées : '1', '1.5', '2'."
        )
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# COUCHE 3 — Validation sémantique V2 (V2Unpacker)
# ═══════════════════════════════════════════════════════════════════════════════

class V2Validator:
    """
    Reproduit V2Unpacker.unpack() + les règles métier des sérialiseurs DRF
    (CompetitionSerializer, LeaderboardSerializer, ColumnSerializer).
    Aucune DB n'est consultée : les références à des clés UUID existantes
    sont signalées comme avertissements, pas des erreurs bloquantes.
    """

    def __init__(self, yaml_data: Dict, temp_dir: str, result: ValidationResult, verbose: bool):
        self.yaml = yaml_data
        self.temp = temp_dir
        self.result = result
        self.verbose = verbose
        self.tasks: Dict[int, Any] = {}   # index → task dict ou clé uuid

    # ── Entry point ─────────────────────────────────────────────────────────

    def validate(self):
        self._check_title()
        self._check_image()
        self._check_terms()
        self._check_pages()
        self._check_tasks()
        self._check_solutions()
        self._check_phases()
        self._check_leaderboards()
        self._check_fact_sheet()
        self._check_auto_migrate_rules()

    # ── Titre ────────────────────────────────────────────────────────────────

    def _check_title(self):
        if not self.yaml.get("title"):
            self.result.warn("Champ 'title' absent ou vide")
        else:
            self.result.ok(f"Titre : {self.yaml['title']!r}")

    # ── Image ────────────────────────────────────────────────────────────────

    def _check_image(self):
        image_name = self.yaml.get("image")
        if not image_name:
            self.result.error("Champ 'image' manquant dans competition.yaml (_unpack_image)")
            return
        image_path = os.path.join(self.temp, image_name)
        if not os.path.exists(image_path):
            self.result.error(f"Image introuvable dans le ZIP : '{image_name}'")
        else:
            self.result.ok(f"Image trouvée : '{image_name}'")

    # ── Terms ────────────────────────────────────────────────────────────────

    def _check_terms(self):
        terms_path = self.yaml.get("terms")
        if not terms_path:
            self.result.error(
                "Champ 'terms' manquant dans competition.yaml. "
                "Un fichier de CGU est obligatoire (_unpack_terms)."
            )
            return
        full_path = os.path.join(self.temp, terms_path)
        if not os.path.exists(full_path):
            self.result.error(f"Fichier terms introuvable : '{terms_path}'")
        else:
            content = open(full_path, encoding="utf-8", errors="replace").read()
            if not content.strip():
                self.result.error(f"'{terms_path}' est vide, il doit contenir du contenu")
            else:
                self.result.ok(f"Terms OK : '{terms_path}'")

    # ── Pages ────────────────────────────────────────────────────────────────

    def _check_pages(self):
        pages = self.yaml.get("pages")
        if not pages:
            self.result.warn("Aucune page définie (champ 'pages' absent)")
            return
        for i, page in enumerate(pages):
            file_name = page.get("file")
            if not file_name:
                self.result.error(f"Page #{i} : champ 'file' manquant")
                continue
            full_path = os.path.join(self.temp, file_name)
            if not os.path.exists(full_path):
                self.result.error(f"Page '{file_name}' introuvable dans le ZIP")
            else:
                content = open(full_path, encoding="utf-8", errors="replace").read()
                if not content.strip():
                    self.result.error(f"Page '{file_name}' est vide")
                else:
                    self.result.ok(f"Page OK : '{file_name}'")

    # ── Tasks ────────────────────────────────────────────────────────────────

    def _check_tasks(self):
        tasks = self.yaml.get("tasks")
        if not tasks:
            self.result.error("Champ 'tasks' manquant ou vide (_unpack_tasks)")
            return

        seen_indexes: set = set()
        for task in tasks:
            # Index
            index = task.get("index")
            if index is None:
                name = task.get("name") or task.get("key") or "?"
                self.result.error(f"Tâche '{name}' sans 'index'")
                continue
            if index in seen_indexes:
                self.result.error(f"Index de tâche dupliqué : {index}")
                continue
            seen_indexes.add(index)

            # Référence UUID existante (ne peut être vérifiée sans BDD)
            if "key" in task:
                if looks_like_uuid(task["key"]):
                    self.result.warn(
                        f"Tâche #{index} référence une clé UUID existante ({task['key']!r}) "
                        "— non vérifiable sans BDD"
                    )
                    self.tasks[index] = task["key"]
                else:
                    self.result.error(f"Tâche #{index} : 'key' ne ressemble pas à un UUID : {task['key']!r}")
                continue

            # Vérification des fichiers référencés
            for file_type in ["ingestion_program", "input_data", "scoring_program", "reference_data"]:
                if file_type in task:
                    file_path = os.path.join(self.temp, task[file_type])
                    if not os.path.exists(file_path):
                        self.result.error(
                            f"Tâche #{index} '{task.get('name', '')}' : "
                            f"fichier '{task[file_type]}' introuvable ({file_type})"
                        )
                    else:
                        self.result.ok(f"Tâche #{index} — {file_type} : '{task[file_type]}' OK")
                elif file_type == "scoring_program":
                    self.result.error(
                        f"Tâche #{index} '{task.get('name', '')}' : "
                        "'scoring_program' obligatoire mais absent"
                    )
            self.tasks[index] = task

        if self.tasks:
            self.result.ok(f"{len(self.tasks)} tâche(s) définie(s) avec des index uniques")

    # ── Solutions ────────────────────────────────────────────────────────────

    def _check_solutions(self):
        solutions = self.yaml.get("solutions")
        if not solutions:
            return  # optionnel

        seen_indexes: set = set()
        for sol in solutions:
            index = sol.get("index")
            if index is None:
                self.result.error(
                    f"Solution '{sol.get('name') or sol.get('key') or '?'}' sans 'index'"
                )
                continue
            if index in seen_indexes:
                self.result.error(f"Index de solution dupliqué : {index}")
                continue
            seen_indexes.add(index)

            # Vérification des tâches référencées
            task_refs = sol.get("tasks")
            if task_refs is None:
                self.result.error(f"Solution #{index} : champ 'tasks' manquant")
            else:
                missing = [t for t in task_refs if t not in self.tasks]
                if missing:
                    self.result.error(
                        f"Solution #{index} : références à des index de tâches inexistants : {missing}"
                    )

            if "key" in sol:
                if not looks_like_uuid(sol["key"]):
                    self.result.error(f"Solution #{index} : 'key' n'est pas un UUID valide : {sol['key']!r}")
            else:
                path = sol.get("path")
                if not path:
                    self.result.error(f"Solution #{index} : champ 'path' manquant (et pas de 'key')")
                else:
                    full_path = os.path.join(self.temp, path)
                    if not os.path.exists(full_path):
                        self.result.error(f"Solution #{index} : fichier '{path}' introuvable")
                    else:
                        self.result.ok(f"Solution #{index} — path : '{path}' OK")

    # ── Phases ───────────────────────────────────────────────────────────────

    def _check_phases(self):
        phases_raw = self.yaml.get("phases")
        if not phases_raw:
            self.result.error("Aucune phase définie (clé 'phases' manquante)")
            return

        try:
            phases = sorted(phases_raw, key=lambda p: p.get("index", 0))
        except Exception:
            self.result.error("Impossible de trier les phases (vérifiez les champs 'index')")
            return

        parsed_phases = []
        for idx, ph in enumerate(phases):
            name = ph.get("name", f"phase #{idx}")

            # Tâches obligatoires
            if "tasks" not in ph:
                self.result.error(f"Phase '{name}' : champ 'tasks' manquant (obligatoire)")
            else:
                bad = [t for t in ph["tasks"] if t not in self.tasks]
                if bad:
                    self.result.error(
                        f"Phase '{name}' : références à des index de tâches inconnus : {bad}"
                    )

            # Dates
            start = end = None
            try:
                start = get_datetime(ph.get("start"))
                if start is None:
                    self.result.warn(f"Phase '{name}' : 'start' non défini")
            except ValueError as exc:
                self.result.error(f"Phase '{name}' : date 'start' invalide — {exc}")

            try:
                end = get_datetime(ph.get("end"))
            except ValueError as exc:
                self.result.error(f"Phase '{name}' : date 'end' invalide — {exc}")

            if start and end and end <= start:
                self.result.error(
                    f"Phase '{name}' : 'end' ({ph.get('end')}) doit être après 'start' ({ph.get('start')})"
                )

            # Fichiers optionnels (public_data, starting_kit)
            for field_name in ("public_data", "starting_kit"):
                if field_name in ph:
                    fp = os.path.join(self.temp, ph[field_name])
                    if not os.path.exists(fp):
                        self.result.error(f"Phase '{name}' : '{field_name}' — fichier '{ph[field_name]}' introuvable")
                    else:
                        self.result.ok(f"Phase '{name}' — {field_name} OK")

            parsed_phases.append({"index": idx, "name": name, "start": start, "end": end})

        self.result.ok(f"{len(parsed_phases)} phase(s) analysée(s)")

        # ── Validation de l'ordre (base_unpacker._validate_phase_ordering) ──
        for i in range(1, len(parsed_phases)):
            p1 = parsed_phases[i - 1]
            p2 = parsed_phases[i]
            p1_name = p1["name"]
            p2_name = p2["name"]

            if p1["start"] and p2["start"] and p1["end"] is None:
                self.result.error(
                    f"Phase '{p1_name}' doit avoir une date 'end' car une phase '{p2_name}' la suit"
                )
            elif p1["end"] and p2["start"]:
                if p2["start"] < p1["end"]:
                    self.result.error(
                        f"Les phases doivent être séquentielles : "
                        f"'{p2_name}' démarre avant la fin de '{p1_name}'"
                    )
                elif p1["end"] == p2["start"]:
                    self.result.error(
                        f"Conflit de dates : '{p2_name}' doit démarrer APRÈS "
                        f"la fin de '{p1_name}' (pas à la même heure)"
                    )

    # ── Leaderboards ─────────────────────────────────────────────────────────

    def _check_leaderboards(self):
        leaderboards = self.yaml.get("leaderboards")
        if not leaderboards:
            self.result.error("Champ 'leaderboards' manquant ou vide (_unpack_leaderboards)")
            return

        for li, ldb in enumerate(leaderboards):
            ldb_name = ldb.get("title") or ldb.get("key") or f"leaderboard #{li}"

            if not ldb.get("key"):
                self.result.error(f"Leaderboard '{ldb_name}' : champ 'key' manquant")
            if not ldb.get("title"):
                self.result.warn(f"Leaderboard '{ldb_name}' : champ 'title' manquant")

            columns = ldb.get("columns")
            if not columns:
                self.result.error(
                    f"Leaderboard '{ldb_name}' : au moins 1 colonne requise (LeaderboardSerializer)"
                )
                continue

            # Unicité des indexes et des clés (LeaderboardSerializer.validate_columns)
            col_indexes = [c.get("index") for c in columns]
            col_keys    = [c.get("key")   for c in columns]

            if len(set(col_indexes)) != len(col_indexes):
                self.result.error(f"Leaderboard '{ldb_name}' : indexes de colonnes dupliqués")
            else:
                self.result.ok(f"Leaderboard '{ldb_name}' : indexes de colonnes uniques")

            if len(set(col_keys)) != len(col_keys):
                self.result.error(f"Leaderboard '{ldb_name}' : clés de colonnes dupliquées")
            else:
                self.result.ok(f"Leaderboard '{ldb_name}' : clés de colonnes uniques")

            for col in columns:
                col_id = col.get("key") or col.get("title") or "?"
                computation   = col.get("computation")
                comp_indexes  = col.get("computation_indexes")

                # ColumnSerializer.validate
                if computation and not comp_indexes:
                    self.result.error(
                        f"Colonne '{col_id}' : 'computation' défini mais 'computation_indexes' absent"
                    )
                if comp_indexes and not computation:
                    self.result.error(
                        f"Colonne '{col_id}' : 'computation_indexes' défini mais 'computation' absent"
                    )
                if comp_indexes and str(col.get("index")) in str(comp_indexes).split(","):
                    self.result.error(
                        f"Colonne '{col_id}' : auto-référence interdite dans 'computation_indexes'"
                    )

                sorting = col.get("sorting")
                if sorting and sorting not in ("asc", "desc"):
                    self.result.error(
                        f"Colonne '{col_id}' : 'sorting' doit être 'asc' ou 'desc', reçu '{sorting}'"
                    )

    # ── Fact sheet ──────────────────────────────────────────────────────────

    def _check_fact_sheet(self):
        """Reproduit CompetitionSerializer.validate_fact_sheet."""
        fact_sheet = self.yaml.get("fact_sheet")
        if not fact_sheet:
            return  # optionnel

        if not isinstance(fact_sheet, dict):
            self.result.error("'fact_sheet' doit être un objet JSON/YAML valide")
            return

        expected_keys = {"key", "type", "title", "selection", "is_required", "is_on_leaderboard"}
        valid_types   = {"checkbox", "text", "select"}

        for fk, fv in fact_sheet.items():
            missing = expected_keys - set(fv.keys())
            if missing:
                self.result.error(f"fact_sheet '{fk}' : clés manquantes : {missing}")
            if fk != fv.get("key"):
                self.result.error(
                    f"fact_sheet : 'key' ({fv.get('key')!r}) ne correspond pas à la clé JSON ({fk!r})"
                )
            if fv.get("type") not in valid_types:
                self.result.error(
                    f"fact_sheet '{fk}' : type '{fv.get('type')}' invalide (attendus : {valid_types})"
                )

        self.result.ok("fact_sheet valide")

    # ── Règles CompetitionSerializer.validate_phases ─────────────────────────

    def _check_auto_migrate_rules(self):
        """Reproduit CompetitionSerializer.validate_phases."""
        phases = self.yaml.get("phases", [])
        if not phases:
            return  # déjà signalé dans _check_phases

        if len(phases) == 0:
            self.result.error("La compétition doit avoir au moins une phase")
            return

        first = min(phases, key=lambda p: p.get("index", 0))
        if first.get("auto_migrate_to_this_phase"):
            self.result.error(
                "La première phase ne peut pas avoir 'auto_migrate_to_this_phase: true'"
            )

        if len(phases) == 1 and phases[0].get("auto_migrate_to_this_phase"):
            self.result.error(
                "'auto_migrate_to_this_phase' ne peut pas être activé sur une compétition à une seule phase"
            )


# ═══════════════════════════════════════════════════════════════════════════════
# COUCHE 3 — Validation sémantique V1.5 (V15Unpacker)
# ═══════════════════════════════════════════════════════════════════════════════

class V15Validator:
    """
    Reproduit V15Unpacker.unpack() pour le format legacy CodaLab v1/1.5.
    """

    def __init__(self, yaml_data: Dict, temp_dir: str, result: ValidationResult, verbose: bool):
        self.yaml = yaml_data
        self.temp = temp_dir
        self.result = result
        self.verbose = verbose

    def validate(self):
        self._check_title()
        self._check_image()
        self._check_pages_and_terms()
        self._check_phases()
        self._check_leaderboard()

    def _check_title(self):
        if not self.yaml.get("title"):
            self.result.warn("Champ 'title' absent ou vide")
        else:
            self.result.ok(f"Titre : {self.yaml['title']!r}")

    def _check_image(self):
        image_name = self.yaml.get("image")
        if not image_name:
            self.result.error("Champ 'image' manquant (_unpack_image)")
            return
        image_path = os.path.join(self.temp, image_name)
        if not os.path.exists(image_path):
            self.result.error(f"Image introuvable : '{image_name}'")
        else:
            self.result.ok(f"Image trouvée : '{image_name}'")

    def _check_pages_and_terms(self):
        html = self.yaml.get("html")
        if not html:
            self.result.error("Champ 'html' manquant (_unpack_pages V1.5)")
            return

        if "terms" not in html:
            self.result.error(
                "Fichier 'terms' introuvable dans la section 'html' (obligatoire pour V1.5)"
            )

        for title, path in html.items():
            full_path = os.path.join(self.temp, path)
            if not os.path.exists(full_path):
                self.result.error(f"Fichier HTML '{path}' (page '{title}') introuvable")
            else:
                content = open(full_path, encoding="utf-8", errors="replace").read()
                if not content.strip():
                    self.result.warn(f"Fichier HTML '{path}' (page '{title}') est vide")
                else:
                    self.result.ok(f"Page '{title}' — '{path}' OK")

    def _check_phases(self):
        phases_raw = self.yaml.get("phases")
        if not phases_raw:
            self.result.error("Aucune phase trouvée (clé 'phases' manquante, V1.5)")
            return

        try:
            phases = sorted(phases_raw.values(), key=lambda p: p.get("phasenumber", 0))
        except (AttributeError, TypeError):
            self.result.error("'phases' doit être un dict (format V1.5)")
            return

        for ph in phases:
            label = ph.get("label", "?")

            for file_type in ["ingestion_program", "input_data", "scoring_program", "reference_data"]:
                if file_type in ph:
                    fp = os.path.join(self.temp, ph[file_type])
                    if not os.path.exists(fp):
                        self.result.error(
                            f"Phase '{label}' : '{file_type}' — fichier '{ph[file_type]}' introuvable"
                        )
                    else:
                        self.result.ok(f"Phase '{label}' — {file_type} OK")

            # Date de départ obligatoire
            if not ph.get("start_date"):
                self.result.error(f"Phase '{label}' : 'start_date' manquant")
            else:
                try:
                    get_datetime(ph["start_date"])
                    self.result.ok(f"Phase '{label}' — start_date OK")
                except ValueError as exc:
                    self.result.error(f"Phase '{label}' : 'start_date' invalide — {exc}")

        self.result.ok(f"{len(phases)} phase(s) V1.5 analysée(s)")

    def _check_leaderboard(self):
        ldb_root = self.yaml.get("leaderboard")
        if not ldb_root:
            self.result.error("Clé 'leaderboard' manquante (V1.5)")
            return

        if "leaderboards" not in ldb_root:
            self.result.error("Clé 'leaderboard.leaderboards' manquante (V1.5)")
        if "columns" not in ldb_root:
            self.result.error("Clé 'leaderboard.columns' manquante (V1.5)")
            return

        columns = ldb_root["columns"]
        for col_key, col_data in columns.items():
            if not col_data.get("leaderboard"):
                self.result.error(f"Colonne '{col_key}' : référence 'leaderboard' manquante")

        self.result.ok(f"Leaderboard V1.5 avec {len(columns)} colonne(s) analysé")


# ═══════════════════════════════════════════════════════════════════════════════
# Point d'entrée principal
# ═══════════════════════════════════════════════════════════════════════════════

def validate_bundle(bundle_path: str, verbose: bool = False, force_version: Optional[str] = None):
    result = ValidationResult()

    print(c("bold", f"\n  Validation de : {bundle_path}"))
    print("─" * 60)

    if not os.path.exists(bundle_path):
        result.error(f"Fichier introuvable : {bundle_path}")
        result.print_summary(verbose)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as temp_dir:

        # ── Couche 1 : ZIP + YAML ──────────────────────────────────────────
        print(c("blue", "[ Couche 1 ] Intégrité ZIP & competition.yaml"))
        competition_yaml = check_zip_and_yaml(bundle_path, temp_dir, result)
        if competition_yaml is None:
            result.print_summary(verbose)
            sys.exit(1)

        # ── Couche 2 : version ─────────────────────────────────────────────
        print(c("blue", "[ Couche 2 ] Détection de la version"))
        version = force_version or detect_version(competition_yaml, result)
        if version is None:
            result.print_summary(verbose)
            sys.exit(1)

        # ── Couche 3 : validation sémantique ──────────────────────────────
        print(c("blue", "[ Couche 3 ] Validation sémantique"))
        if version in ("1", "1.5"):
            validator = V15Validator(competition_yaml, temp_dir, result, verbose)
        else:
            validator = V2Validator(competition_yaml, temp_dir, result, verbose)
        validator.validate()

    result.print_summary(verbose)
    sys.exit(0 if result.is_valid else 1)


# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Validateur local de bundle.zip Codabench",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  python validate_bundle.py mon_bundle.zip
  python validate_bundle.py mon_bundle.zip --verbose
  python validate_bundle.py mon_bundle.zip --version 2

Codes de retour :
  0  → bundle valide
  1  → bundle invalide ou erreur
        """,
    )
    parser.add_argument("bundle", help="Chemin vers le fichier bundle.zip")
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Affiche tous les contrôles (y compris ceux qui passent)",
    )
    parser.add_argument(
        "--version",
        choices=["1", "1.5", "2"],
        default=None,
        help="Force la version du format (par défaut : auto-détection via competition.yaml)",
    )
    args = parser.parse_args()
    validate_bundle(args.bundle, verbose=args.verbose, force_version=args.version)


if __name__ == "__main__":
    main()