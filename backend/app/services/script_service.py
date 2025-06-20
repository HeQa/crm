from app.database.models import Scripts, ScriptsText
from app.schemas import (ScriptsResponse, ScriptRequest, ScriptNodeRequest,
                        ScriptsTextResponse,
                         ScriptCreate, ScriptUpdate, ScriptDelete,
                         ScriptTextCreate, ScriptTextUpdate, ScriptTextDelete)
from typing import List


async def script_response(script: Scripts):
    return ScriptsResponse(
        id=script.id,
        name=script.name,
        description=script.description)


async def script_text_response(script_text: ScriptsText):
    return ScriptsTextResponse(
        id=script_text.id,
        script=script_text.script,
        parent=script_text.parent,
        head=script_text.head,
        text=script_text.text
        )


async def get_scripts_all() -> List[ScriptsResponse]:
    scripts = await Scripts.all()
    return [await script_response(script) for script in scripts]


async def get_scripts_node(script: ScriptRequest) -> ScriptNodeRequest:
    scripts_text = await ScriptsText.filter(script=script.id, parent=script.parent).all()
    script = await Scripts.get_or_none(id=script.id)
    return ScriptNodeRequest(script=script,
                             scripts_text=[await script_text_response(script_text) for script_text in scripts_text])

async def get_scripts_node_back(script: ScriptRequest) -> ScriptNodeRequest:
    up_parent = await ScriptsText.get_or_none(id=script.parent)
    scripts_text = await ScriptsText.filter(script=script.id, parent=up_parent.parent).all()
    script = await Scripts.get_or_none(id=script.id)
    return ScriptNodeRequest(script=script,
                             scripts_text=[await script_text_response(script_text) for script_text in scripts_text])

# -----------------------------------------------------------------

async def script_create(script: ScriptCreate):
    await Scripts.create(
                                    name=script.name,
                                    description=script.description,
                                )

    return await get_scripts_all()

async def script_update(script: ScriptUpdate):
    await Scripts.update_or_create(
                                    id=script.id,
                                    defaults={'name':script.name,
                                              'description': script.description}

                                )
    return await get_scripts_all()


async def script_delete(script: ScriptDelete):
    await Scripts.filter(id=script.id).delete()
    return await get_scripts_all()

# ----------------------------------------------------------------
async def script_text_create(script: ScriptTextCreate):
    new_script = await ScriptsText.create(
                            script_id=script.script_id,
                            parent=script.parent,
                            head=script.head,
                            text=script.text,
    )
    return await get_scripts_node(ScriptRequest(id=new_script.script, parent=script.parent))


async def script_text_update(script: ScriptTextUpdate):
    await ScriptsText.update_or_create(
        id=script.id,
        defaults={'head': script.head,
                  'text': script.text}

    )
    update_script = await ScriptsText.get_or_none(id=script.id)
    return await get_scripts_node(ScriptRequest(id=update_script.script, parent=update_script.parent))


async def script_text_delete(script: ScriptTextDelete):
    delete_script = await ScriptsText.get_or_none(id=script.id)
    await ScriptsText.filter(id=script.id).delete()
    return await get_scripts_node(ScriptRequest(id=delete_script.script, parent=delete_script.parent))

