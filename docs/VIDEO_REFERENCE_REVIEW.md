# Video reference review — 2026-10-02

Source: [Beer Pharmacie Cask & Tap House In Syston Leicestershire](https://www.youtube.com/watch?v=q0zBpicUXjg), Blue Van Man, uploaded 16 May 2019, duration 19:00. Upload date is metadata, not a verified filming date. Compare historical interior evidence with newer photographs, supplied plan and Sam's corrections.

Downloaded available 1280×720 video to ignored `build/video-reference/q0zBpicUXjg.mp4`. Extracted 114 full-resolution JPEG samples every ten seconds, plus additional selected timestamps. Selected 20 tour frames. No source photo edits, cropping or repainting. Separate contact sheets resize previews only. Source metadata, SHA256 and extraction recipe: `assets/video-references/q0zBpicUXjg/manifest.json`; selected timestamps: `selected-manifest.json`. Reference use only; distribution rights are not established.

Open `assets/video-references/q0zBpicUXjg/selected-tour.jpg`. All five overview sheets and the selected sheet were visually reviewed. Sampling can miss brief shots.

| Section | Observed evidence | Blender use |
| --- | --- | --- |
| 06:10–07:40 | Medicine cases, instruments, advert wall, sofas, entrance framing, skeleton display | Refine display positions, shelf heights and entrance details |
| 08:10–08:40 | Bar drawers, pumps, lights and passage beside bar | Compare current counter and passage from multiple angles |
| 10:20 | Rear corridor, cream door frames, notices, wood floor | Dress passage using user-confirmed door layout |
| 10:32–10:40 | Timber treads, metal nosings, dark stair wall, handrail and window by turn | Add stair finishes; exact orientation/dimensions remain unverified |
| 10:52–13:30 | Upstairs banquettes, tables, stools/chairs, muted carpet, recessed lights, poster walls, mirror, TV, dartboard, bookcase, upright piano and vintage radios | Furnish upstairs with separate editable objects |
| 14:10–14:40 | Corridor notices and downstairs reverse view | Check passage decor and bar/room relationship |

Suggested next pass: stair finishes/window detail, upstairs carpet/banquettes/tables, then TV/darts/bookcase/piano and wall decoration. Check large prop placement against the latest plan before changing partitions. This is reference footage, not a measured survey. No useful exterior street views were identified in the ten-second samples; surrounding buildings need another source.

Successful commands: yt-dlp metadata extraction and download with best video <=1080 plus audio, MP4 merge using C:/ffmpeg; `python scripts/review_reference_video.py`; `python scripts/select_reference_video.py`. Blender remains v08. No Radiant/game rebuild or push.
