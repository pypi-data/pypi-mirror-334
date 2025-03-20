from itertools import chain

import Testrail_utils.pytest_tr_api_client.service as service
from Testrail_utils.pytest_tr_api_client.modules.bdd_classes import TrFeature
from Testrail_utils.pytest_tr_api_client.modules.exceptions import TestRailError
from Testrail_utils.pytest_tr_api_client.modules.plan import Plan


def validate_scenario_tags(feature: TrFeature, test_rail):
    errors = []
    if test_rail.configuration.no_tag_in_feature_header is True:
        if len(feature.tags) != 0:
            errors.append(f'File "{feature.path}", line 1: Delete all tags from head of feature file')
    for scenario in feature.children:
        if "scenario" in scenario:
            scenario = scenario["scenario"]
            line = scenario["location"]["line"]
            tag_names = tuple(tag["name"] for tag in scenario["tags"])
            for one_of in test_rail.configuration.one_of_tags:
                found_tags = tuple(filter(lambda x: x in one_of, tag_names))
                if len(found_tags) > 1:
                    errors.append(f'File "{feature.path}", line {line}: Using more than 1 tag from group {one_of}')
                elif len(found_tags) == 0:
                    errors.append(f'File "{feature.path}", line {line}: Missing any tags from {one_of}')
            if "/rest/" not in feature.path.lower() and "/web/" not in feature.path.lower():
                for one in test_rail.configuration.at_least_one:
                    if not any((x in one for x in tag_names)):
                        errors.append(f'File "{feature.path}", line {line}: Missing at least one tag from {one}')

    return errors


def validate_configs(configuration: str, tr_client) -> None:
    bad_conf = []
    configs = tuple(x.name.lower() for x in chain.from_iterable([x.configs for x in tr_client.configs.get_configs()]))
    for param in service.trim(configuration).split(", "):
        if param.lower() not in configs:
            bad_conf.append(param)
    if len(bad_conf) != 0:
        raise TestRailError(f'Wrong configuration name: {", ".join(bad_conf)}')


def validate_plan_id(plan_id: int, tr_client) -> None:
    if not isinstance(tr_client.plans.get_plan(plan_id), Plan):
        raise TestRailError("Wrong plan id")
