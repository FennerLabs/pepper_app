import io
import base64
from rdkit.Chem import Draw


def image_from_mol(mol):
    img = Draw.MolToImage(mol)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    img_bytes = bio.getvalue()
    base64_str = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:image/png;base64,{base64_str}"