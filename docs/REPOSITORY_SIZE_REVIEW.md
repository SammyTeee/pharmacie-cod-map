# Repository size review — 7 November 2026

Read-only baseline before adding the handover files. Decimal MB/GB are used.
The working tree is not clean; existing character work must be preserved.

| Area | Measured size | Meaning |
| --- | ---: | --- |
| Tracked files | 4.292 GB / 2,935 files | Current index, measured from working files |
| Tracked Blender files | 3.023 GB / 72 files | Repeated full checkpoints; main checkout saving |
| Latest neutral v59 | 75.868 MB | Preserve unchanged; source of root handover copy |
| Separate skate v60 | 75.867 MB | Preserve unchanged; different variant |
| Other 70 tracked Blender files | 2.871 GB | Historical checkpoints in addition to v59/v60 |
| Other tracked content | 1.269 GB | Includes source assets, review media, notes and engine sources |
| Untracked, not ignored | 825.267 MB / 194 files | Mainly separate generated Dave/Rocky work; not yet committed |
| Ignored local files | 13.893 GB | Not included by an ordinary Git push |
| Physical `build/` tree | 12.441 GB | Local runtime/tool/build/backup data; not all disposable |
| Ignored files in `assets/blender` | 1.565 GB | Local backups/trials; preserve pending individual review |
| Local Git object files | 4.471 GB | Loose object storage, not the remote repository size |
| Local temporary Git object files | 961.012 MB / 30 files | Reported as garbage by `git count-objects`; not normal project files |

Local `master` and cached `origin/master` both pointed to `3d3a7bc` at audit
start; there were 29 commits on HEAD. This comparison used the local remote
tracking ref, not a fresh fetch. GitHub metadata separately confirmed repository
`SammyTeee/pharmacie-cod-map`, default branch `master`, with reported size
1,420,291 KB; that server metric is not a precise clone-transfer estimate.
No Git LFS rules were present in `.gitattributes`.

## Prepared handover

`Pharmacie-Syston.blend` is an identical copy of immutable v59: 75,868,496 bytes,
SHA-256 `c39f15e8b24e099f5b9753778597ef89bf9b76fa815324612af1fb5569f0a834`.
Blender 5.2.2 LTS opened it successfully; all 52 file-backed images are packed,
with no linked libraries or unpacked external paths. No source file was saved
or modified by this check. See [BROWNIE_HANDOVER.md](BROWNIE_HANDOVER.md).

The newer Blender modification dates belong to separate character files, not a
newer neutral street model. No Blender process was found during the initial
saved-file inspection. This does not audit operating-system temporary recovery
files or prove that an unsaved session never existed.

## Approved ordinary Git prune

Sam approved a smaller single-project checkout. Remove all 72 checkpoint paths
under `assets/blender/`, listed in
[handover/old-blender-checkpoints.txt](handover/old-blender-checkpoints.txt) from
the current Git index, using cached removal so every local file remains. The
directory's `.blend` files are now ignored to prevent accidental re-addition.
Keep the v59 original and v60 skate variant locally; the root handover file is
the single tracked Blender project. Keep all notes and other tracked assets.
The pre-removal local receipt records all 72 file sizes/modification times and
SHA-256 for v59, v60 and the handover copy:
[handover/local-checkpoint-receipt.json](handover/local-checkpoint-receipt.json).

After adding the 75.868 MB handover copy and removing 3.023 GB of checkpoint
paths, current tracked working files are expected to be approximately
**1.345 GB**, plus the small new notes: a **2.947 GB net reduction (69%)**. Git
stores identical content as the same blob, so the root copy reuses v59's content
object. No texture repacking or Blender resave was needed.

Existing history still retains the old checkpoints. Brownie should use a shallow
clone to avoid downloading that history. A normal full clone and GitHub's stored
history do not become small just because old paths disappear in a new commit.
No force push, history rewrite, local checkpoint deletion or blanket cache
deletion is part of this cleanup.

## Local disk cleanup is a separate decision

There is potential to reclaim space in old engine deployment backups, Blender
autosaves, reproducible captures and temporary Git objects. An ignored file is
not automatically disposable: `build/` also contains pinned tools, extracted
runtime inputs, accepted package outputs and recovery copies. Do not delete the
whole directory. Keep accepted core65/Dave66, separate Dave67, skate floor/audio
repairs, all character sources, original photos and the latest Blender projects.

The 30 `tmp_obj_*` files should be checked for active Git writers before any
maintenance. Garbage collection or manual deletion was not performed. Ordinary
Git object compression may improve local storage but is not the same as
removing history and has not been measured here.

## Status

The initial review prepared the handover without pruning. Sam then approved
untracking the checkpoints and pushing the single-project handover. The final
receipt is [handover/cleanup-result.json](handover/cleanup-result.json); it records
the staged size, single remaining tracked `.blend` and local preservation
verification. Existing unrelated uncommitted assets and edits remain local.
Git history is retained. No local checkpoint deletion or game work is involved.
