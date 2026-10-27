"""Refpot preview example, adapted from public guide revision 3294ce39f0e5630c660fad2e5a1e3977bf52a17f.

Copyright (c) 2026 Tugrul Guner. MIT; complete notice is in
skills/refpot-database/LICENSE. Requires the matching Refpot environment.
"""
from pathlib import Path
from tempfile import TemporaryDirectory

from refpot import Database, Row


with TemporaryDirectory(prefix="refpot-skill-") as directory:
    path = Path(directory) / "example.rp"
    with Database(path) as db:
        db.insert(1, 42, "answer")
        db.update(1, value=43)
        assert db.get(1) == Row(1, 43, "answer")
        with db.transaction():
            db.insert(2, 99, "é" * 15)
        try:
            with db.transaction():
                db.update(1, value=100)
                raise RuntimeError("roll back")
        except RuntimeError:
            pass
        assert db.get(1) == Row(1, 43, "answer")
        try:
            db.insert(3, 1, "é" * 16)
        except ValueError:
            pass
        else:
            raise AssertionError("oversized UTF-8 text was accepted")
        db.delete(2)
        db.checkpoint()
    with Database(path) as db:
        assert db.get(1) == Row(1, 43, "answer")
        assert len(db) == 1
        print(db.get(1))
