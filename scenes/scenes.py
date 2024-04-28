from scenes.scene import SceneBase

SCENES: dict[str, SceneBase]= {
}

START_SCENE = "Title"

def get_start_scene():
    return SCENES[START_SCENE]

def set_start_scene(scene_name: str):
    global START_SCENE
    START_SCENE = scene_name

def set_scene(title: str, scene: SceneBase):
    SCENES[title] = scene

def get_scene(title: str):
    return SCENES[title]
