"""Render Namo Narayanam / Dashavatara from the original channel song."""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ENGINE = ROOT / "production/thiruppavai1-image-motion/render.py"
spec = importlib.util.spec_from_file_location("gkd_image_film", ENGINE)
film = importlib.util.module_from_spec(spec)
spec.loader.exec_module(film)

film.HERE = HERE
film.STILLS = ROOT / "production/approved/namo-narayanam"
film.AUDIO = next((ROOT / "source/youtube").glob("4vZEVROZIx8*.m4a"))
film.OUTPUT = HERE / "NAMO-NARAYANAM-CINEMATIC-v1.mp4"
film.SOURCE_VIDEO_ID = "4vZEVROZIx8"
film.ALLOW_REPEAT = True
film.SHOTS = [
    ("N01",.50,.50,1.04,"Vishnu emblems"),
    ("NN18",.50,.49,1.05,"devotees approach Vishnu temple"),
    ("N14",.50,.50,1.08,"Garuda banner"),
    ("N16",.50,.51,1.08,"tulsi and conch offering"),
    ("NN21",.50,.49,1.04,"devotees at temple tank"),
    ("N17",.50,.50,1.07,"cosmic ocean transition"),
    ("N02",.50,.50,1.05,"Matsya"),
    ("N04",.50,.50,1.05,"Kurma"),
    ("NN22",.50,.51,1.05,"Varaha boar"),
    ("N06",.50,.49,1.06,"Narasimha"),
    ("N03",.50,.50,1.06,"Vamana"),
    ("N11",.50,.51,1.07,"Parashurama"),
    ("N07",.50,.50,1.07,"Rama"),
    ("N12",.50,.51,1.07,"Balarama"),
    ("N08",.50,.50,1.08,"Krishna"),
    ("N09",.50,.50,1.06,"Kalki"),
    ("NN19",.50,.50,1.04,"devotees study Dashavatara relief"),
    ("N15",.50,.49,1.04,"ten-avatar relief"),
    ("N10",.50,.50,1.05,"Ananta Shayanam"),
    ("N13",.50,.49,1.04,"Vishnu and Lakshmi"),
    ("NN20",.50,.49,1.04,"priest offers tulsi"),
    ("N02",.49,.52,1.32,"Matsya ocean closer"),
    ("N04",.55,.49,1.31,"Kurma mountain closer"),
    ("NN22",.51,.49,1.31,"Varaha boar closer"),
    ("N06",.50,.48,1.31,"Narasimha closer"),
    ("N03",.55,.49,1.31,"Vamana steps closer"),
    ("N11",.53,.48,1.33,"Parashurama axe closer"),
    ("N07",.55,.49,1.31,"Rama bow closer"),
    ("N12",.52,.52,1.31,"Balarama plough closer"),
    ("N08",.52,.51,1.32,"Krishna flute closer"),
    ("N09",.53,.51,1.31,"Kalki horse closer"),
    ("N15",.50,.50,1.30,"Dashavatara medallions closer"),
    ("NN21",.59,.49,1.28,"devotees return to tank"),
    ("N14",.48,.50,1.31,"Garuda banner closer"),
    ("N10",.50,.49,1.30,"Ananta Shayanam closer"),
    ("NN20",.57,.49,1.28,"tulsi reaches sanctum"),
    ("N13",.50,.49,1.04,"Vishnu and Lakshmi final"),
]

if __name__ == "__main__":
    film.main()
