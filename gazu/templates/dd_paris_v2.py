from lucidity import Template


def register():
    return [
        Template("project", "{project}"),
        # -------------------- BASIC -----------------------
        Template("sequence", "{@project}/05_SEQUENCE/{sequence}"),
        Template("shot", "{@sequence}/{shot}"),
        Template("task", "{@shot}/{task_category}/{shot_task}"),
        Template("asset_build", "{@project}/04_ASSET/{asset_build}"),
        Template("ab_task", "{@asset_build}/{task_category}/{shot_task}"),
        # -------------------- VERSION ---------------------
        Template("asset_version", "{@shot}/{asset}_{asset_version}"),
        Template("asset_version_task", "{@task}/{asset}_{asset_version}"),
        Template(
            "asset_version_sources_seq",
            "{@sequence}/_INGEST/{asset_category}/{asset}_{asset_version}",
        ),
        Template(
            "asset_version_sources",
            "{@shot}/_INGEST/{asset_category}/{asset}_{asset_version}",
        ),
        Template(
            "asset_version_task_category",
            "{@task}/{asset_category}/{asset}_{asset_version}",
        ),
        Template("ab_asset_version", "{@asset_build}/{asset}_{asset_version}"),
        Template("ab_asset_version_task", "{@ab_task}/{asset}_{asset_version}"),
        Template(
            "ab_asset_version_task_category",
            "{@ab_task}/{asset_category}/{asset}_{asset_version}",
        ),
    ]
