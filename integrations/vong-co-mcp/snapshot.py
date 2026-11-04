"""Bounded offline snapshots of explicitly approved V1/V2 Markdown sources.

Hashes detect accidental modification; they are not signatures or licensing grants.
No network requests or fallback are performed by LocalSource or the exporter.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from catalog import BRANCHES, MAX_BYTES, REPO, WORKS, SourceAccessError, SourceNotFound

SCHEMA = 1
MANIFEST_LIMIT = 100_000


def approved_sources():
    pairs = {(branch, f'{w.folder}/README.md')
             for branch in BRANCHES.values() for w in WORKS}
    pairs.update((BRANCHES['v2'], f'{w.folder}/v2-bien-ban-nghiem-thu.md') for w in WORKS)
    pairs.add((BRANCHES['v2'], 'docs/ke-hoach-v2.md'))
    return pairs


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate manifest key')
        result[key] = value
    return result


def _bounded_read(root, relative, limit):
    target = root / relative
    # Reject symlinks at every level, including links that point inside the root.
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise SourceAccessError('Snapshot symlinks are not supported')
    if not target.resolve().is_relative_to(root):
        raise SourceAccessError('Snapshot path escaped its root')
    try:
        with target.open('rb') as stream:
            content = stream.read(limit + 1)
    except OSError as exc:
        raise SourceAccessError('Cannot read the local snapshot') from exc
    if len(content) > limit:
        raise SourceAccessError('Snapshot file exceeds size limit')
    return content


class LocalSource:
    def __init__(self, directory):
        directory = Path(directory)
        if directory.is_symlink():
            raise SourceAccessError('Snapshot root must not be a symlink')
        self.root = directory.resolve()
        try:
            manifest = json.loads(_bounded_read(self.root, 'manifest.json', MANIFEST_LIMIT),
                                  object_pairs_hook=_unique)
            if (not isinstance(manifest, dict) or
                set(manifest) != {'schema_version', 'repository', 'commits', 'files'} or
                type(manifest['schema_version']) is not int or manifest['schema_version'] != SCHEMA or
                manifest['repository'] != REPO):
                raise ValueError('Invalid snapshot schema')
            commits = manifest['commits']
            if (not isinstance(commits, dict) or set(commits) != set(BRANCHES.values()) or
                any(not isinstance(v, str) or not re.fullmatch(r'[0-9a-f]{40}', v)
                    for v in commits.values())):
                raise ValueError('Invalid source commits')
            records = manifest['files']
            if not isinstance(records, list) or len(records) != len(approved_sources()):
                raise ValueError('Incomplete source inventory')
            self.records = {}
            for record in records:
                if not isinstance(record, dict) or set(record) != {'branch', 'path', 'sha256'}:
                    raise ValueError('Invalid file record')
                key = (record['branch'], record['path'])
                if key not in approved_sources() or key in self.records:
                    raise ValueError('Unapproved or duplicate source')
                digest = record['sha256']
                if digest is not None and (not isinstance(digest, str) or
                                           not re.fullmatch(r'[0-9a-f]{64}', digest)):
                    raise ValueError('Invalid digest')
                self.records[key] = digest
            self.commits = dict(commits)
        except (ValueError, TypeError, KeyError, UnicodeError) as exc:
            raise SourceAccessError('Invalid snapshot manifest') from exc

    def __call__(self, branch, path):
        key = (branch, path)
        if key not in self.records:
            raise ValueError('Source is outside the approved snapshot inventory')
        expected = self.records[key]
        if expected is None:
            raise SourceNotFound(path)
        raw = _bounded_read(self.root, f'{branch}/{path}', MAX_BYTES)
        if hashlib.sha256(raw).hexdigest() != expected:
            raise SourceAccessError('Snapshot checksum mismatch; export a fresh snapshot')
        try:
            return raw.decode('utf-8')
        except UnicodeError as exc:
            raise SourceAccessError('Snapshot document is not valid UTF-8') from exc

    def status(self):
        return {'mode': 'offline_snapshot', 'network_fallback': False,
                'commits': dict(self.commits), 'inventory_files': len(self.records),
                'available_files': sum(v is not None for v in self.records.values()),
                'integrity': 'SHA-256 checked on every read; not a digital signature'}


def _git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def export_snapshot(repo, output):
    """Export committed sources, never working-tree edits, to a new directory."""
    repo, output = Path(repo).resolve(), Path(output)
    if output.is_symlink() or output.exists():
        raise ValueError('Snapshot destination must not exist')
    output = output.absolute()
    commits = {}
    for branch in BRANCHES.values():
        for ref in (f'refs/remotes/origin/{branch}', f'refs/heads/{branch}'):
            try:
                commits[branch] = _git(repo, 'rev-parse', '--verify', ref + '^{commit}').decode().strip()
                break
            except subprocess.CalledProcessError:
                continue
        else:
            raise ValueError(f'Missing local Git ref: {branch}; fetch sources first')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.vong-co-snapshot-', dir=output.parent) as tmp:
        staged = Path(tmp) / 'snapshot'
        staged.mkdir()
        records = []
        for branch, path in sorted(approved_sources()):
            spec = commits[branch] + ':' + path
            # A missing approved document is recorded explicitly, not silently ignored.
            exists = _git(repo, 'ls-tree', commits[branch], '--', path).decode().strip()
            digest = None
            if exists:
                if not exists.startswith('100644 blob ') and not exists.startswith('100755 blob '):
                    raise ValueError('Only regular Markdown files can be exported')
                size = int(_git(repo, 'cat-file', '-s', spec))
                if size > MAX_BYTES:
                    raise ValueError('Source document exceeds snapshot limit')
                raw = _git(repo, 'show', spec)
                raw.decode('utf-8')
                digest = hashlib.sha256(raw).hexdigest()
                dest = staged / branch / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(raw)
            records.append({'branch': branch, 'path': path, 'sha256': digest})
        manifest = {'schema_version': SCHEMA, 'repository': REPO,
                    'commits': commits, 'files': records}
        (staged / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        source = LocalSource(staged)
        for key, digest in source.records.items():
            if digest is not None:
                source(*key)
        if output.exists() or output.is_symlink():
            raise ValueError('Snapshot destination appeared during export')
        staged.rename(output)
    return LocalSource(output).status()


def main():
    parser = argparse.ArgumentParser(description='Export Vong-co V1/V2 for offline MCP use')
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = export_snapshot(args.repo, args.out)
    except (ValueError, OSError, subprocess.SubprocessError, SourceAccessError) as exc:
        parser.exit(1, f'Cannot export snapshot: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
