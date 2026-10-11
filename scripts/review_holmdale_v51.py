"""Use the established porch camera views for the mirrored window revision."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
f=ROOT/'scripts/review_holmdale_v50.py'
s=f.read_text().replace("dest=ROOT/'recon/v50'","dest=ROOT/'recon/v51'").replace("'pharmacie-holmdale-corner-porch-v50.blend'","'pharmacie-holmdale-mirrored-window-v51.blend'")
s=s.replace("archive=bpy.data.collections['ARCHIVE v50 | Straight-facing porch revision'];review.collection.children.link(archive)","archive=bpy.data.collections['ARCHIVE v51 | Smaller left porch window']")
s=s.replace("for stage in ('before','after'):","for stage in ('after',):")
ns={'__file__':str(f)};exec(compile(s,str(f),'exec'),ns);result=ns['result']
