from scenes.scene import SceneBase
from scenes.title_scene import TitleScene

SCENES: dict[str, SceneBase]= {
    "Title": TitleScene(),
}

START_SCENE = "Title"

def get_start_scene():
    return SCENES[START_SCENE]

def set_scene(title: str, scene: SceneBase):
    SCENES[title] = scene

def get_scene(title: str):
    return SCENES[title]