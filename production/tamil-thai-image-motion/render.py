"""Render Tamil Thai Vazhthu with 21 distinct image-derived shots."""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ENGINE = ROOT / "production/thiruppavai1-image-motion/render.py"
spec = importlib.util.spec_from_file_location("gkd_image_film", ENGINE)
film = importlib.util.module_from_spec(spec)
spec.loader.exec_module(film)

film.HERE = HERE
film.STILLS = ROOT / "production/approved/tamil-thai-vazhthu"
film.AUDIO = next((ROOT / "source/youtube").glob("ETELjf0OTi4*.m4a"))
film.OUTPUT = HERE / "TAMIL-THAI-VAZHTHU-CINEMATIC-v1.mp4"
film.SOURCE_VIDEO_ID = "ETELjf0OTi4"
film.ALLOW_REPEAT = False
film.SHOTS = [
    ("S01",.50,.51,1.04,"southern night over sea"),
    ("S02",.50,.52,1.06,"three seas at sunrise"),
    ("S03",.50,.50,1.06,"Western Ghats waterfall"),
    ("S04",.50,.53,1.05,"fertile Cauvery fields"),
    ("S06",.50,.52,1.08,"ancient river anicut"),
    ("S05",.50,.50,1.05,"Chola temple civilization"),
    ("S09",.50,.52,1.07,"Sangam port and trade"),
    ("S07",.50,.53,1.08,"poetry gathering place"),
    ("TT18",.50,.50,1.05,"poet and listeners"),
    ("S08",.50,.51,1.10,"palm-leaf learning"),
    ("S13",.50,.51,1.04,"learning beneath banyan"),
    ("S16",.50,.52,1.11,"stone inscription craft"),
    ("S17",.50,.51,1.09,"bronze-casting craft"),
    ("S12",.50,.52,1.07,"handloom craft"),
    ("TT21",.50,.50,1.05,"Tamil women at the loom"),
    ("S10",.50,.51,1.08,"traditional instruments"),
    ("TT19",.50,.49,1.05,"Tamil music ensemble"),
    ("S11",.50,.52,1.08,"dance heritage"),
    ("TT20",.50,.49,1.05,"Bharatanatyam performance"),
    ("S14",.50,.50,1.04,"Tamil Thai at sunrise"),
    ("S15",.50,.50,1.04,"lamp and kolam closing"),
]

if __name__ == "__main__":
    film.main()
