from . import client

from .cache import cache
from .helpers import normalize_model_parameter, timeit, get_extension


@cache
def all_output_types():
    """
    Returns:
        list: Output types listed in database.
    """
    return client.fetch_all("output-types")


@cache
def all_output_types_for_entity(entity):
    """
    Args:
        entity (str / dict): The entity dict or the entity ID.

    Returns:
        list: All output types linked to output files for given entity.
    """
    entity = normalize_model_parameter(entity)
    return client.fetch_all("entities/%s/output-types" % entity["id"])


@cache
def all_output_types_for_asset_instance(asset_instance, temporal_entity):
    """
    Returns:
        list: Output types for given asset instance and entity (shot or scene).
    """
    return client.fetch_all(
        "asset-instances/%s/entities/%s/output-types"
        % (asset_instance["id"], temporal_entity["id"])
    )


@cache
def get_output_type(output_type_id):
    """
    Args:
        output_type_id (str): ID of claimed output type.

    Returns:
        dict: Output type matching given ID.
    """
    return client.fetch_one("output-types", output_type_id)


@cache
def get_output_type_by_name(output_type_name):
    """
    Args:
        output_type_name (str): name of claimed output type.

    Returns:
        dict: Output type matching given name.
    """
    return client.fetch_first("output-types", {"name": output_type_name})


def new_output_type(name, short_name):
    """
    Create a new output type in database.

    Args:
        name (str): Name of created output type.
        short_name (str): Name shorten to represente the type in UIs.

    Returns:
        dict: Created output type.
    """
    data = {"name": name, "short_name": short_name}
    output_type = get_output_type_by_name(name)
    if output_type is None:
        return client.create("output-types", data)
    else:
        return output_type


@cache
def get_output_file(output_file_id):
    """
    Args:
        output_file_id (str): ID of claimed output file.

    Returns:
        dict: Output file matching given ID.
    """
    path = "data/output-files/%s" % (output_file_id)
    return client.get(path)


@cache
def get_output_file_by_path(path):
    """
    Args:
        output_file_id (str): Path of claimed output file.

    Returns:
        dict: Output file matching given path.
    """
    return client.fetch_first("output-files", {"path": path})


@cache
def get_all_working_files_for_entity(entity, task=None, name=None):
    """
    Retrieves all the working files of a given entity and specied parameters
    """
    entity = normalize_model_parameter(entity)
    task = normalize_model_parameter(task)
    path = "entities/{entity_id}/working-files?".format(entity_id=entity["id"])

    params = {}
    if task is not None:
        params["task_id"] = task["id"]
    if name is not None:
        params["name"] = name

    return client.fetch_all(path, params)


@cache
def get_all_preview_files_for_task(task):
    """
    Retrieves all the preview files for a given task.
    """
    task = normalize_model_parameter(task)
    return client.fetch_all("preview-files", {"task_id":task["id"]})


def all_output_files_for_entity(
    entity,
    output_type=None,
    task_type=None,
    name=None,
    representation=None,
    file_status=None,
    created_at_since=None,
    person=None,
):
    """
    Args:
        entity (str / dict): The entity dict or ID.
        output_type (str / dict): The output type dict or ID.
        task_type (str / dict): The task type dict or ID.
        name (str): The file name
        representation (str): The file representation
        file_status (str / dict): The file status

    Returns:
        list:
            Output files for a given entity (asset or shot), output type,
            task_type, name and representation
    """
    entity = normalize_model_parameter(entity)
    output_type = normalize_model_parameter(output_type)
    task_type = normalize_model_parameter(task_type)
    file_status = normalize_model_parameter(file_status)
    person = normalize_model_parameter(person)
    path = "entities/{entity_id}/output-files".format(entity_id=entity["id"])

    params = {}
    if output_type:
        params["output_type_id"] = output_type["id"]
    if task_type:
        params["task_type_id"] = task_type["id"]
    if representation:
        params["representation"] = representation
    if name:
        params["name"] = name
    if file_status:
        params["file_status_id"] = file_status["id"]
    if created_at_since:
        params["created_at_since"] = created_at_since
    if person:
        params["person_id"] = person["id"]

    return client.fetch_all(path, params)


@cache
def all_output_files_for_asset_instance(
    asset_instance,
    temporal_entity=None,
    task_type=None,
    output_type=None,
    name=None,
    representation=None,
    file_status=None,
    created_at_since=None,
    person=None,
):
    """
    Args:
        asset_instance (str / dict): The instance dict or ID.
        temporal_entity (str / dict): Shot dict or ID (or scene or sequence).
        task_type (str / dict): The task type dict or ID.
        output_type (str / dict): The output_type dict or ID.
        name (str): The file name
        representation (str): The file representation
        file_status (str / dict): The file status

    Returns:
        list: Output files for a given asset instance, temporal entity,
        output type, task_type, name and representation
    """
    asset_instance = normalize_model_parameter(asset_instance)
    temporal_entity = normalize_model_parameter(temporal_entity)
    task_type = normalize_model_parameter(task_type)
    output_type = normalize_model_parameter(output_type)
    file_status = normalize_model_parameter(file_status)
    person = normalize_model_parameter(person)
    path = "asset-instances/{asset_instance_id}/output-files".format(
        asset_instance_id=asset_instance["id"]
    )

    params = {}
    if temporal_entity:
        params["temporal_entity_id"] = temporal_entity["id"]
    if output_type:
        params["output_type_id"] = output_type["id"]
    if task_type:
        params["task_type_id"] = task_type["id"]
    if representation:
        params["representation"] = representation
    if name:
        params["name"] = name
    if file_status:
        params["file_status_id"] = file_status["id"]
    if created_at_since:
        params["created_at_since"] = created_at_since
    if person:
        params["person_id"] = person["id"]

    return client.fetch_all(path, params)


@cache
def all_softwares():
    """
    Returns:
        dict: Software versions listed in database.
    """
    return client.fetch_all("softwares")


@cache
def get_software(software_id):
    """
    Args:
        software_id (str): ID of claimed output type.

    Returns:
        dict: Software object corresponding to given ID.
    """
    return client.fetch_one("softwares", software_id)


@cache
def get_software_by_name(software_name):
    """
    Args:
        software_name (str): Name of claimed output type.

    Returns:
        dict: Software object corresponding to given name.
    """
    return client.fetch_first("softwares", {"name": software_name})


def new_software(name, short_name, file_extension):
    """
    Create a new software in datatabase.

    Args:
        name (str): Name of created software.
        short_name (str): Short representation of software name (for UIs).
        file_extension (str): Main file extension generated by given software.

    Returns:
        dict: Created software.
    """
    data = {
        "name": name,
        "short_name": short_name,
        "file_extension": file_extension,
    }
    software = get_software_by_name(name)
    if software is None:
        return client.create("softwares", data)
    else:
        return software


@cache
def build_working_file_path(
    task, name="main", mode="working", software=None, revision=1, sep="/"
):
    """
    From the file path template configured at the project level and arguments, it
    builds a file path location where to store related DCC file.

    Args:
        task (str / id): Task related to working file.
        name (str): Additional suffix for the working file name.
        mode (str): Allow to select a template inside the template.
        software (str / id): Software at the origin of the file.
        revision (int): File revision.
        sep (str): OS separator.

    Returns:
        Generated working file path for given task (without extension).
    """
    data = {"mode": mode, "name": name, "revision": revision}
    task = normalize_model_parameter(task)
    software = normalize_model_parameter(software)
    if software is not None:
        data["software_id"] = software["id"]
    result = client.post("data/tasks/%s/working-file-path" % task["id"], data)
    return "%s%s%s" % (
        result["path"].replace(" ", "_"),
        sep,
        result["name"].replace(" ", "_"),
    )


@cache
def build_entity_output_file_path(
    entity,
    output_type,
    task_type,
    name="main",
    mode="output",
    representation="",
    revision=0,
    nb_elements=1,
    sep="/",
):
    """
    From the file path template configured at the project level and arguments, it
    builds a file path location where to store related DCC output file.

    Args:
        entity (str / id): Entity for which an output file is needed.
        output_type (str / id): Output type of the generated file.
        task_type (str / id): Task type related to output file.
        name (str): Additional suffix for the working file name.
        mode (str): Allow to select a template inside the template.
        representation (str): Allow to select a template inside the template.
        revision (int): File revision.
        nb_elements (str): To represent an image sequence, the amount of file is
                           needed.
        sep (str): OS separator.

    Returns:
        Generated output file path for given entity, task type and output type
        (without extension).
    """
    entity = normalize_model_parameter(entity)
    output_type = normalize_model_parameter(output_type)
    task_type = normalize_model_parameter(task_type)

    data = {
        "task_type_id": task_type["id"],
        "output_type_id": output_type["id"],
        "mode": mode,
        "name": name,
        "representation": representation,
        "revision": revision,
        "nb_elements": nb_elements,
        "separator": sep,
    }
    path = "data/entities/%s/output-file-path" % entity["id"]
    result = client.post(path, data)
    return "%s%s%s" % (
        result["folder_path"].replace(" ", "_"),
        sep,
        result["file_name"].replace(" ", "_"),
    )


@cache
def build_asset_instance_output_file_path(
    asset_instance,
    temporal_entity,
    output_type,
    task_type,
    name="main",
    representation="",
    mode="output",
    revision=0,
    nb_elements=1,
    sep="/",
):
    """
    From the file path template configured at the project level and arguments, it
    builds a file path location where to store related DCC output file.

    Args:
        asset_instance_id entity (str / id): Asset instance for which a file
        is required.
        temporal entity (str / id): Temporal entity scene or shot in which
        the asset instance appeared.
        output_type (str / id): Output type of the generated file.
        task_type (str / id): Task type related to output file.
        name (str): Additional suffix for the working file name.
        mode (str): Allow to select a template inside the template.
        representation (str): Allow to select a template inside the template.
        revision (int): File revision.
        nb_elements (str): To represent an image sequence, the amount of file is
                           needed.
        sep (str): OS separator.

    Returns:
        Generated output file path for given asset instance, task type and
        output type (without extension).
    """
    asset_instance = normalize_model_parameter(asset_instance)
    temporal_entity = normalize_model_parameter(temporal_entity)
    output_type = normalize_model_parameter(output_type)
    task_type = normalize_model_parameter(task_type)
    data = {
        "task_type_id": task_type["id"],
        "output_type_id": output_type["id"],
        "mode": mode,
        "name": name,
        "representation": representation,
        "revision": revision,
        "nb_elements": nb_elements,
        "sep": sep,
    }
    path = "data/asset-instances/%s/entities/%s/output-file-path" % (
        asset_instance["id"],
        temporal_entity["id"],
    )
    result = client.post(path, data)
    return "%s%s%s" % (
        result["folder_path"].replace(" ", "_"),
        sep,
        result["file_name"].replace(" ", "_"),
    )


def new_working_file(
    task,
    name="main",
    mode="working",
    software=None,
    comment="",
    file_path="",
    person=None,
    revision=0,
    sep="/",
    size=None,
):
    """
    Create a new working_file for given task. It generates and store the
    expected path for given task and options. It sets a revision number
    (last revision + 1).

    Args:
        task (str / id): Task related to working file.
        name (str): Additional suffix for the working file name.
        mode (str): Allow to select a template inside the template.
        software (str / id): Software at the origin of the file.
        comment (str): Comment related to created revision.
        person (str / id): Author of the file.
        revision (int): File revision.
        sep (str): OS separator.

    Returns:
        Created working file.
    """
    task = normalize_model_parameter(task)
    software = normalize_model_parameter(software)
    person = normalize_model_parameter(person)
    data = {
        "name": name,
        "comment": comment,
        "task_id": task["id"],
        "revision": revision,
        "path": file_path,
        "mode": mode,
        "size": size,
    }
    if person is not None:
        data["person_id"] = person["id"]
    if software is not None:
        data["software_id"] = software["id"]

    return client.post("data/tasks/%s/working-files/new" % task["id"], data)


def new_entity_output_file(
    entity,
    output_type,
    task_type,
    comment=None,
    working_file=None,
    person=None,
    name="main",
    mode="output",
    render_info=None,
    file_path="",
    revision=0,
    nb_elements=1,
    representation="",
    sep="/",
    size=None,
    file_status_id=None,
):
    """
    Create a new output file for given entity, task type and output type.
    It generates and store the expected path and sets a revision number
    (last revision + 1).

    Args:
        entity (str / id): Entity for which an output file is needed.
        output_type (str / id): Output type of the generated file.
        task_type (str / id): Task type related to output file.
        comment (str): Comment related to created revision.
        working_file (str / id): Working file which is the source of the
        generated file.
        person (str / id): Author of the file.
        name (str): Additional suffix for the working file name.
        mode (str): Allow to select a template inside the template.
        revision (int): File revision.
        nb_elements (str): To represent an image sequence, the amount of file is
                           needed.
        representation (str): Differientate file extensions. It can be useful
        to build folders based on extensions like abc, jpg, etc.
        sep (str): OS separator.
        file_status_id (id): The id of the file status to set at creation

    Returns:
        Created output file.
    """
    entity = normalize_model_parameter(entity)
    output_type = normalize_model_parameter(output_type)
    task_type = normalize_model_parameter(task_type)
    working_file = normalize_model_parameter(working_file)
    person = normalize_model_parameter(person)
    path = "data/entities/%s/output-files/new" % entity["id"]
    data = {
        "output_type_id": output_type["id"],
        "task_type_id": task_type["id"],
        "comment": comment,
        "revision": revision,
        "representation": representation,
        "name": name,
        "path": file_path,
        "render_info": render_info,
        "nb_elements": nb_elements,
        "extension": get_extension(file_path),
        "sep": sep,
        "size": size,
    }

    if working_file is not None:
        data["working_file_id"] = working_file["id"]

    if person is not None:
        data["person_id"] = person["id"]

    if file_status_id is not None:
        data["file_status_id"] = file_status_id

    return client.post(path, data)


def new_asset_instance_output_file(
    asset_instance,
    temporal_entity,
    output_type,
    task_type,
    comment,
    name="master",
    mode="output",
    render_info=None,
    file_path="",
    working_file=None,
    person=None,
    revision=0,
    nb_elements=1,
    representation="",
    sep="/",
    size=None,
    file_status_id=None,
):
    """
    Create a new output file for given asset instance, temporal entity, task
    type and output type.  It generates and store the expected path and sets a
    revision number (last revision + 1).

    Args:
        entity (str / id): Entity for which an output file is needed.
        output_type (str / id): Output type of the generated file.
        task_type (str / id): Task type related to output file.
        comment (str): Comment related to created revision.
        working_file (str / id): Working file which is the source of the
    generated file.
        person (str / id): Author of the file.
        name (str): Additional suffix for the working file name.
        mode (str): Allow to select a template inside the template.
        revision (int): File revision.
        nb_elements (str): To represent an image sequence, the amount of file
    needed.
        representation (str): Differientate file extensions. It can be useful
    to build folders based on extensions like abc, jpg, cetc.
        sep (str): OS separator.
        file_status_id (id): The id of the file status to set at creation

    Returns:
        Created output file.
    """
    asset_instance = normalize_model_parameter(asset_instance)
    temporal_entity = normalize_model_parameter(temporal_entity)
    output_type = normalize_model_parameter(output_type)
    task_type = normalize_model_parameter(task_type)
    working_file = normalize_model_parameter(working_file)
    person = normalize_model_parameter(person)
    path = "data/asset-instances/%s/entities/%s/output-files/new" % (
        asset_instance["id"],
        temporal_entity["id"],
    )
    data = {
        "output_type_id": output_type["id"],
        "task_type_id": task_type["id"],
        "comment": comment,
        "name": name,
        "path": file_path,
        "render_info": render_info,
        "revision": revision,
        "representation": representation,
        "nb_elements": nb_elements,
        "extension": get_extension(file_path),
        "sep": sep,
        "size": size,
    }

    if working_file is not None:
        data["working_file_id"] = working_file["id"]

    if person is not None:
        data["person_id"] = person["id"]

    if file_status_id is not None:
        data["file_status_id"] = file_status_id

    return client.post(path, data)


def get_next_entity_output_revision(
    entity, output_type, task_type, name="main"
):
    """
    Args:
        entity (str / dict): The entity dict or ID.
        output_type (str / dict): The entity dict or ID.
        task_type (str / dict): The entity dict or ID.

    Returns:
        int: Next revision of ouput files available for given entity, output
        type and task type.
    """
    entity = normalize_model_parameter(entity)
    path = "data/entities/%s/output-files/next-revision" % entity["id"]
    data = {
        "name": name,
        "output_type_id": output_type["id"],
        "task_type_id": task_type["id"],
        "name": name,
    }
    return client.post(path, data)["next_revision"]


def get_next_asset_instance_output_revision(
    asset_instance, temporal_entity, output_type, task_type, name="master"
):
    """
    Args:
        asset_instance (str / dict): The asset instance dict or ID.
        temporal_entity (str / dict): The temporal entity dict or ID.
        output_type (str / dict): The entity dict or ID.
        task_type (str / dict): The entity dict or ID.

    Returns:
        int: Next revision of ouput files available for given asset insance
        temporal entity, output type and task type.
    """
    asset_instance = normalize_model_parameter(asset_instance)
    temporal_entity = normalize_model_parameter(temporal_entity)
    output_type = normalize_model_parameter(output_type)
    task_type = normalize_model_parameter(task_type)
    path = (
        "data/asset-instances/"
        + "%s/entities/%s/output-files/next-revision"
        % (asset_instance["id"], temporal_entity["id"])
    )
    data = {
        "name": name,
        "output_type_id": output_type["id"],
        "task_type_id": task_type["id"],
    }
    return client.post(path, data)["next_revision"]


def get_last_entity_output_revision(
    entity, output_type, task_type, name="master"
):
    """
    Args:
        entity (str / dict): The entity dict or ID.
        output_type (str / dict): The entity dict or ID.
        task_type (str / dict): The entity dict or ID.
        name (str): The output name

    Returns:
        int: Last revision of ouput files for given entity, output type and task
        type.
    """
    entity = normalize_model_parameter(entity)
    output_type = normalize_model_parameter(output_type)
    task_type = normalize_model_parameter(task_type)
    revision = get_next_entity_output_revision(
        entity, output_type, task_type, name
    )
    if revision != 1:
        revision -= 1
    return revision


def get_last_asset_instance_output_revision(
    asset_instance, temporal_entity, output_type, task_type, name="master"
):
    """
    Generate last output revision for given asset instance.
    """
    asset_instance = normalize_model_parameter(asset_instance)
    temporal_entity = normalize_model_parameter(temporal_entity)
    output_type = normalize_model_parameter(output_type)
    task_type = normalize_model_parameter(task_type)
    revision = get_next_asset_instance_output_revision(
        asset_instance, temporal_entity, output_type, task_type, name=name
    )
    if revision != 1:
        revision -= 1
    return revision


@cache
def get_last_output_files_for_entity(
    entity,
    output_type=None,
    task_type=None,
    name=None,
    representation=None,
    file_status=None,
    created_at_since=None,
    person=None,
):
    """
    Args:
        entity (str / dict): The entity dict or ID.
        output_type (str / dict): The output type dict or ID.
        task_type (str / dict): The task type dict or ID.
        name (str): The file name
        representation (str): The file representation
        file_status (str / dict): The file status

    Returns:
        list:
            Last output files for a given entity (asset or shot), output type,
            task_type, name and representation
    """
    entity = normalize_model_parameter(entity)
    output_type = normalize_model_parameter(output_type)
    task_type = normalize_model_parameter(task_type)
    file_status = normalize_model_parameter(file_status)
    person = normalize_model_parameter(person)
    path = "entities/{entity_id}/output-files/last-revisions".format(
        entity_id=entity["id"]
    )

    params = {}
    if output_type:
        params["output_type_id"] = output_type["id"]
    if task_type:
        params["task_type_id"] = task_type["id"]
    if representation:
        params["representation"] = representation
    if name:
        params["name"] = name
    if file_status:
        params["file_status_id"] = file_status["id"]
    if created_at_since:
        params["created_at_since"] = created_at_since
    if person:
        params["person_id"] = person["id"]

    return client.fetch_all(path, params)


@cache
def get_last_output_files_for_asset_instance(
    asset_instance,
    temporal_entity,
    task_type=None,
    output_type=None,
    name=None,
    representation=None,
    file_status=None,
    created_at_since=None,
    person=None,
):
    """
    Args:
        asset_instance (str / dict): The asset instance dict or ID.
        temporal_entity (str / dict): The temporal entity dict or ID.
        output_type (str / dict): The output type dict or ID.
        task_type (str / dict): The task type dict or ID.
        name (str): The file name
        representation (str): The file representation
        file_status (str / dict): The file status

    Returns:
        list: last output files for given asset instance and
        temporal entity where it appears.
    """
    asset_instance = normalize_model_parameter(asset_instance)
    temporal_entity = normalize_model_parameter(temporal_entity)
    output_type = normalize_model_parameter(output_type)
    task_type = normalize_model_parameter(task_type)
    file_status = normalize_model_parameter(file_status)
    person = normalize_model_parameter(person)
    path = (
        "asset-instances/{asset_instance_id}/entities/{temporal_entity_id}"
        "/output-files/last-revisions"
    ).format(
        asset_instance_id=asset_instance["id"],
        temporal_entity_id=temporal_entity["id"],
    )

    params = {}
    if output_type:
        params["output_type_id"] = output_type["id"]
    if task_type:
        params["task_type_id"] = task_type["id"]
    if representation:
        params["representation"] = representation
    if name:
        params["name"] = name
    if file_status:
        params["file_status_id"] = file_status["id"]
    if created_at_since:
        params["created_at_since"] = created_at_since
    if person:
        params["person_id"] = person["id"]

    return client.fetch_all(path, params)


@cache
def get_working_files_for_task(task):
    """
    Args:
        task (str / dict): The task dict or the task ID.

    Returns:
        list: Working files related to given task.
    """
    task = normalize_model_parameter(task)
    path = "data/tasks/%s/working-files" % task["id"]
    return client.get(path)


@cache
def get_last_working_files(task):
    """
    Args:
        task (str / dict): The task dict or the task ID.

    Returns:
        dict: Keys are working file names and values are last working file
        availbable for given name.
    """
    task = normalize_model_parameter(task)
    path = "data/tasks/%s/working-files/last-revisions" % task["id"]
    return client.get(path)


@cache
def get_last_working_file_revision(task, name="main"):
    """
    Args:
        task (str / dict): The task dict or the task ID.
        name (str): File name suffix (optional)

    Returns:
        dict: Last revisions stored in the API for given task and given file
        name suffx.
    """
    task = normalize_model_parameter(task)
    path = "data/tasks/%s/working-files/last-revisions" % task["id"]
    working_files_dict = client.get(path)
    return working_files_dict.get(name)


@cache
def get_working_file(working_file_id):
    """
    Args:
        working_file_id (str): ID of claimed working file.

    Returns:
        dict: Working file corresponding to given ID.
    """
    return client.fetch_one("working-files", working_file_id)


def update_comment(working_file, comment):
    """
    Update the file comment in database for given working file.

    Args:
        working_file (str / dict): The working file dict or ID.

    Returns:
        dict: Modified working file
    """
    working_file = normalize_model_parameter(working_file)
    return client.put(
        "/actions/working-files/%s/comment" % working_file["id"],
        {"comment": comment},
    )


def update_modification_date(working_file):
    """
    Update modification date of given working file with current time (now).

    Args:
        working_file (str / dict): The working file dict or ID.

    Returns:
        dict: Modified working file
    """
    return client.put(
        "/actions/working-files/%s/modified" % working_file["id"], {}
    )


def update_output_file(output_file, data):
    """
    Update the data of given output file.

    Args:
        output_file (str / dict): The output file dict or ID.

    Returns:
        dict: Modified output file
    """
    output_file = normalize_model_parameter(output_file)
    path = "/data/output-files/%s" % output_file["id"]
    return client.put(path, data)


def set_project_file_tree(project, file_tree_name):
    """
    (Deprecated) Set given file tree template on given project. This template
    will be used to generate file paths. The template is selected from sources.
    It is found by using given name.

    Args:
        project (str / dict): The project file dict or ID.

    Returns:
        dict: Modified project.

    """
    project = normalize_model_parameter(project)
    data = {"tree_name": file_tree_name}
    path = "actions/projects/%s/set-file-tree" % project["id"]
    return client.post(path, data)


def update_project_file_tree(project, file_tree):
    """
    Set given dict as file tree template on given project. This template
    will be used to generate file paths.

    Args:
        project (str / dict): The project dict or ID.
        file_tree (dict): The file tree template to set on project.

    Returns:
        dict: Modified project.
    """
    project = normalize_model_parameter(project)
    data = {"file_tree": file_tree}
    path = "data/projects/%s" % project["id"]
    return client.put(path, data)


def upload_working_file(working_file, file_path):
    """
    Save given file in working file storage.

    Args:
        working_file (str / dict): The working file dict or ID.
        file_path (str): Location on hard drive where to save the file.
    """
    working_file = normalize_model_parameter(working_file)
    url_path = "/data/working-files/%s/file" % working_file["id"]
    client.upload(url_path, file_path)
    return working_file


def download_working_file(working_file, file_path=None):
    """
    Download given working file and save it at given location.

    Args:
        working_file (str / dict): The working file dict or ID.
        file_path (str): Location on hard drive where to save the file.
    """
    working_file = normalize_model_parameter(working_file)
    if file_path is None:
        working_file = client.fetch_one("working-files", working_file["id"])
        file_path = working_file["path"]
    return client.download(
        "data/working-files/%s/file" % (working_file["id"]),
        file_path,
    )


def download_preview_file(preview_file, file_path):
    """
    Download given preview file and save it at given location.

    Args:
        preview_file (str / dict): The preview file dict or ID.
        file_path (str): Location on hard drive where to save the file.
    """
    preview_file = normalize_model_parameter(preview_file)
    preview_file = client.fetch_one("preview-files", preview_file["id"])
    file_type = 'movies' if preview_file['extension'] == 'mp4' else 'pictures'
    return client.download(
        "%s/originals/preview-files/%s.%s"
        % (file_type, preview_file["id"], preview_file["extension"]),
        file_path,
    )


def download_preview_file_thumbnail(preview_file, file_path):
    """
    Download given preview file thumbnail and save it at given location.

    Args:
        preview_file (str / dict): The preview file dict or ID.
        file_path (str): Location on hard drive where to save the file.

    """
    preview_file = normalize_model_parameter(preview_file)
    return client.download(
        "pictures/thumbnails/preview-files/%s.png" % (preview_file["id"]),
        file_path,
    )


def update_preview(preview_file, data):
    """
    Update the data of given preview file.

    Args:
        preview_file (str / dict): The preview file dict or ID.

    Returns:
        dict: Modified preview file
    """
    preview_file = normalize_model_parameter(preview_file)
    path = "/data/preview-files/%s" % preview_file["id"]
    return client.put(path, data)


# TODO: unittest
@cache
def all_file_status():
    """
    Returns:
        list: Output file-status listed in database.
    """
    return client.fetch_all("file-status")


def new_file_status(name, color):
    """
    Create a new file status if not existing yet.
    """
    data = {"name": name, "color": color}
    status = get_file_status_by_name(name)
    if status is None:
        return client.create("file-status", data)
    else:
        return status


@cache
def get_file_status(status_id):
    """
    Return file status object corresponding to given ID.
    """
    return client.fetch_one("file-status", status_id)


@cache
def get_file_status_by_name(name):
    """
    Return file status object corresponding to given name
    """
    return client.fetch_first("file-status?name=%s" % name)


# TODO: unittest
@cache
def get_children_file(children_file_id):
    """
    Args:
        children_file_id (str): ID of claimed children file.

    Returns:
        dict: Children file matching given ID.
    """
    path = "data/children-files/%s" % (children_file_id)
    return client.get(path)


# TODO: unittest
def new_children_file(
    output_file, output_type, path=None, size=None, file_status=None, render_info=None
):
    """
    Create a new children file of a output file

    Args:
        output_file (str / dict): The output file dict or ID.
        output_type (str / dict): The output type dict or ID.

    Returns:
        dict: Created children file.
    """
    output_file = normalize_model_parameter(output_file)
    output_type = normalize_model_parameter(output_type)

    data = {
        "output_type_id": output_type["id"],
        "path": path,
        "size": size,
        "render_info": render_info,
    }
    if file_status is not None:
        file_status = normalize_model_parameter(file_status)
        data["file_status_id"] = file_status["id"]

    return client.post("data/files/%s/children-files/new" % output_file["id"], data)


# TODO: unittest
def update_children_file(children_file, data):
    """
    Update the data of given children file.

    Args:
        children_file (str / dict): The children file dict or ID.

    Returns:
        dict: Modified children file
    """
    children_file = normalize_model_parameter(children_file)
    path = "data/children-files/%s" % children_file["id"]
    return client.put(path, data)


# TODO: unittest
def remove_children_file(children_file):
    """
    Remove children file from database.

    Args:
        task_status (str / dict): The task status dict or ID.
    """
    children_file = normalize_model_parameter(children_file)
    return client.delete(
        "data/children-files/%s" % children_file["id"], {"force": "true"}
    )


# TODO: unittest
@cache
def get_dependent_file(dependent_file_id):
    """
    Args:
        dependent_file_id (str): ID of claimed dependent file.

    Returns:
        dict: dependent file matching given ID.
    """
    path = "data/dependent-files/%s" % (dependent_file_id)
    return client.get(path)


# TODO: unittest
def new_dependent_file(output_file, path, checksum=None, size=None):
    """
    """
    output_file = normalize_model_parameter(output_file)
    data = {
        "path": path,
        "checksum": checksum,
        "size": size,
    }
    return client.post("data/files/%s/dependent-files/new" % output_file["id"], data)


# TODO: unittest
def update_dependent_file(dependent_file, data):
    """
    Update the data of given dependent file.

    Args:
        output_file (str / dict): The output file dict or ID.

    Returns:
        dict: Modified output file
    """
    dependent_file = normalize_model_parameter(dependent_file)
    path = "data/dependent-files/%s" % dependent_file["id"]
    return client.put(path, data)


# TODO: unittest
def remove_dependent_file(dependent_file):
    """
    Remove dependent file from database.

    Args:
        task_status (str / dict): The task status dict or ID.
    """
    dependent_file = normalize_model_parameter(dependent_file)
    return client.delete(
        "data/dependent-files/%s" % dependent_file["id"], {"force": "true"}
    )


def add_comment(output_file, task_status=None, comment="", person=None, attachments=[]):
    """
    Add comment to given output file. Each comment requires a file_status. Since the
    addition of comment triggers a task status change. Comment text can be
    empty.

    Args:
        task (str / dict): The task dict or the task ID.
        task_status (str / dict): The task status dict or ID. Currently NOT USED !
        comment (str): Comment text

    Returns:
        dict: Created comment.
    """
    output_file = normalize_model_parameter(output_file)
    task_status_id = None
    if task_status:
        task_status_id = normalize_model_parameter(task_status)["id"]

    data = {"task_status_id": task_status_id, "comment": comment}

    if person is not None:
        person = normalize_model_parameter(person)
        data["person_id"] = person["id"]

    if len(attachments) == 0:
        return client.post("actions/files/%s/comment" % output_file["id"], data)

    else:
        attachment = attachments.pop()
        return client.upload(
            "actions/files/%s/comment" % output_file["id"],
            attachment,
            data=data,
            extra_files=attachments,
        )


def remove_comment(comment):
    """
    Remove given comment and related (previews, news, notifications) from
    database.

    Args:
        comment (str / dict): The comment dict or the comment ID.
    """
    comment = normalize_model_parameter(comment)
    return client.delete("data/comments/%s" % comment["id"])


@cache
def all_comments_for_output_file(output_file):
    """
    Args:
        output_file (str / dict): The output_file dict or the output_file ID.

    Returns:
        Comments linked to the given output_file.
    """
    output_file = normalize_model_parameter(output_file)
    return client.fetch_all("files/%s/comments" % output_file["id"])


@cache
def get_last_comment_for_output_file(output_file):
    """
    Args:
        output_file (str / dict): The output_file dict or the output_file ID.

    Returns:
        Last comment posted for given output_file.
    """
    output_file = normalize_model_parameter(output_file)
    return client.fetch_first("files/%s/comments" % output_file["id"])


def get_output_file_by_shotgun_id(shotgun_id):
    path = "/data/files/shotgun/%s" % (shotgun_id)
    return client.get(path)


# -----------------------
# TODO: improve cache person/ entity
# TODO: move this to a better place
from .task import all_task_types
from .entity import get_entity
from .asset import get_asset
from .person import get_person
from .project import get_project
import clique


def get_attribute(func, id, retry=False):
    if not id:
        return None

    try:
        return next(el for el in func() if el["id"] == id)
    except:
        if retry:
            return None

        # try to clear cache and retry
        func.clear_cache()
        return get_attribute(func, id, retry=True)


def get_output_file_data(output_file):
    # shot
    if output_file.get("entity_id"):
        output_file["entity"] = get_entity(output_file["entity_id"])
        output_file["project"] = get_project(output_file["entity"]["project_id"])
        # sequence
        output_file["entity"]["parent"] = get_entity(output_file["entity"]["parent_id"])
    # asset
    elif output_file.get("asset_instance_id"):
        output_file["asset_instance"] = get_asset(output_file["asset_instance_id"])
        output_file["project"] = get_project(
            output_file["asset_instance"]["project_id"]
        )

    if output_file.get("path") and "%" in output_file["path"]:
        # TODO: catch potential error parse (single frame, etc)
        collection = clique.parse(output_file["path"])
        output_file["collection_path"] = output_file["path"]
        output_file["path"] = collection.format("{head}{padding}{tail}")
        frames = list(collection.indexes)
        output_file["frame_in"], output_file["frame_out"] = frames[0], frames[-1]

    output_file["person"] = get_person(output_file["person_id"])
    output_file["file_status"] = get_attribute(
        all_file_status, output_file["file_status_id"]
    )

    output_file["output_type"] = get_attribute(
        all_output_types, output_file["output_type_id"]
    )

    output_file["task_type"] = get_attribute(
        all_task_types, output_file["task_type_id"]
    )

    return output_file
