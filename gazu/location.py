import os
import sys
import logging
import platform
import lucidity

from .templates import dd_paris_v2
from future.utils import iteritems

logger = logging.getLogger("location")


def lucidity_resolver(templates):
    resolver = {}
    for template in templates:
        resolver[template.name] = template
    for template in templates:
        template.template_resolver = resolver
    return resolver


def system_format(string):
    if platform.system() == "Windows":
        return string.replace("/", "\\")
    else:
        return string.replace("\\", "/")


class DefaultStructure:
    def __init__(self, location_name, template_file):
        self.location_name = location_name
        self.mount_point = self.get_disk(location_name)
        self.templates = template_file.register()
        self.templates.reverse()
        lucidity_resolver(self.templates)

    def get_disk(self, location_name):
        data = {
            "pub": {"windows": "O:/", "linux": "/space/commercials/"},
            "long": {"windows": "Q:/", "linux": "/space/features/"},
        }
        return data.get(location_name).get(
            platform.system() == "Windows" and "windows" or "linux"
        )

    def get_root_folders(self):
        return {}

    def get_shot_folders(self):
        return {}

    def format_version(self, version):
        return "v%s" % str(version).zfill(3)

    def get_task_type(self, task_type):
        rules = {
            "2D": ["Rotoscoping", "Compositing",],
            "3D": ["Modeling", "Shading", "Animation", "FX", "Lighting",],
        }

        task_category = None
        shot_task = None

        for category in rules:
            if task_type in rules[category]:
                task_category = category
                break

        if task_category == "2D":
            if task_type == "Compositing":
                shot_task = "COMPS"
            else:
                shot_task = "ELEMENTS/{}".format(task_type.upper())

        return task_category, shot_task

    def get_asset_category(self, asset_type):
        if asset_type in ["plate", "edit"]:
            return asset_type.upper()
        return None

    def get_file_name_map(self):
        templates = [
            lucidity.Template(
                "asset_build",
                "{asset_build}_{asset}_{component_name}_{asset_version}{seq}{ext}",
            ),
            lucidity.Template(
                "asset_only", "{asset}_{component_name}_{asset_version}{seq}{ext}"
            ),
            lucidity.Template(
                "shot", "{shot}_{asset}_{component_name}_{asset_version}{seq}{ext}"
            ),
            lucidity.Template(
                "sequence",
                "{sequence}_{asset}_{component_name}_{asset_version}{seq}{ext}",
            ),
        ]
        return lucidity_resolver(templates)

    def get_task_path(self, task):
        data = {
            "project": task.get("project").get("name"),
        }

        if task.get("entity_type").get("name") == "Shot":
            data["sequence"] = task.get("sequence").get("name")
            data["shot"] = task.get("entity").get("name")
        else:
            data["asset_build"] = task.get("entity").get("name")

        if task.get("task_type"):
            task_name = task.get("task_type").get("name")
            task_category, shot_task = self.get_task_type(task_name)
            data["task_category"] = task_category
            data["shot_task"] = shot_task

        return data

    def get_output_file_path(self, output_file):
        data = {
            "project": output_file.get("project").get("name"),
            "asset_version": self.format_version(output_file.get("revision")),
            "asset": output_file.get("name"),
        }

        asset_category = self.get_asset_category(
            output_file.get("output_type").get("name")
        )
        if asset_category:
            data["asset_category"] = asset_category

        if output_file.get("entity"):
            data["sequence"] = output_file.get("entity").get("parent").get("name")
            data["shot"] = output_file.get("entity").get("name")
        elif output_file.get("asset_instance"):
            data["asset_build"] = output_file.get("asset_instance").get("name")

        if output_file.get("task_type"):
            task_name = output_file.get("task_type").get("name")
            task_category, shot_task = self.get_task_type(task_name)
            data["task_category"] = task_category
            data["shot_task"] = shot_task

        return data

    def get_publish_path(self, entity):
        if entity.get("type") == "Task":
            hierarchy = self.get_task_path(entity)
        elif entity.get("type") == "OutputFile":
            hierarchy = self.get_output_file_path(entity)

        path, _ = lucidity.format(hierarchy, self.templates)
        path = os.path.join(self.mount_point, path)
        return system_format(path)

    def get_work_path(self, entity):
        if entity.get("type") == "Task":
            hierarchy = self.get_task_path(entity)
        elif entity.get("type") == "OutputFile":
            hierarchy = self.get_output_file_path(entity)

        hierarchy["task_category"] = "WORK"
        hierarchy["shot_task"] = entity.get("task_type").get("name")

        path, _ = lucidity.format(hierarchy, self.templates)
        path = os.path.join(self.mount_point, path)
        return system_format(path)


class StructureLong(DefaultStructure):
    def get_root_folders(self):
        return {
            "01_PRODUCTION": {"STORYBOARD": None, "BREAKDOWN": None},
            "02_LIBRARY": {
                "SHOOTING": None,
                "ELEMENTS": {
                    "REFS": {"DD": None, "AGENCE": None, "REAL": None},
                    "STOCKSHOTS": None,
                    "FONT_PACKSHOT": None,
                },
                "MOF": None,
            },
            "03_IN": {
                "_MEDIASHUTTLE": None,
                "FROM_LAB": None,
                "FROM_VENDOR": None,
                "FROM_EDITING": None,
            },
            "04_ASSET": None,
            "05_SEQUENCE": None,
            "06_OUT": {"DELIVERY": None, "WIP": None},
        }

    def get_shot_folders(self):
        return {"_INGEST": None, "WORK": None}


class StructurePub(DefaultStructure):
    def get_root_folders(self):
        return {
            "01_PRODUCTION": {"STORYBOARD": None, "BREAKDOWN": None},
            "02_LIBRARY": {
                "SHOOTING": None,
                "ELEMENTS": {
                    "REFS": {"DD": None, "AGENCE": None, "REAL": None},
                    "STOCKSHOTS": None,
                    "FONT_PACKSHOT": None,
                },
                "SOUND": {"IN": None, "OUT": None},
                "MOF": None,
            },
            "03_IN": {"_MEDIASHUTTLE": None, "FROM_LAB": None, "FROM_VENDOR": None,},
            "04_ASSET": None,
            "05_SEQUENCE": None,
            "06_OUT": {"DELIVERY": None, "WIP": None, "EDIT": None},
            "07_LABO": {
                "CONFO": {"DDTOOLS": None},
                "ASSISTANTS": {
                    "AFTER_EFFECTS": None,
                    "PREMIERE": None,
                    "PHOTOSHOP": None,
                },
            },
        }

    def get_shot_folders(self):
        return {"_INGEST": None, "WORK": None}
