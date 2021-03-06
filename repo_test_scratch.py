from repo.transaction import Transaction
from model.account import Account
from model.source import Source, CanineInfo, EnvironmentInfo
from repo.kit_repo import KitRepo
from repo.account_repo import AccountRepo
from repo.source_repo import SourceRepo
from repo.survey_template_repo import SurveyTemplateRepo
from repo.survey_answers_repo import SurveyAnswersRepo
import datetime
import json
import util.vue_adapter

# TODO: Refactor me into proper unit tests!


def json_converter(o):
    if isinstance(o, datetime.datetime):
        return str(o)
    return o.__dict__


ACCT_ID = "aaaaaaaa-bbbb-cccc-dddd-eeeeffffffff"
DOGGY_ID = "dddddddd-dddd-dddd-dddd-dddddddddddd"
PLANTY_ID = "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"

with Transaction() as t:
    kit_repo = KitRepo(t)
    kit = kit_repo.get_kit("eba20873-b88d-33cc-e040-8a80115d392c", "#6á$E")
    print("Kit: ")
    print(json.dumps(kit, default=json_converter, indent=2))

    acct_repo = AccountRepo(t)
    acct_repo.delete_account(ACCT_ID)
    acc = Account(ACCT_ID,
                  "foo@bar.com",
                  "globus",
                  "Dan",
                  "H",
                  '{"a":5, "b":7}',
                  "USER")
    print(acct_repo.create_account(acc))
    t.commit()

with Transaction() as t:
    acct_repo = AccountRepo(t)
    acc = acct_repo.get_account(ACCT_ID)
    print("Account: ")
    print(json.dumps(acc, default=json_converter, indent=2))

with Transaction() as t:
    acct_repo = AccountRepo(t)
    acc = acct_repo.get_account(ACCT_ID)
    acc.last_name = "The Greatest"
    acct_repo.update_account(acc)
    acc = acct_repo.get_account(ACCT_ID)
    print("Account: ")
    print(json.dumps(acc, default=json_converter, indent=2))
    t.commit()

with Transaction() as t:
    source_repo = SourceRepo(t)
    source_repo.delete_source(ACCT_ID, DOGGY_ID)
    source_repo.delete_source(ACCT_ID, PLANTY_ID)
    source_repo.create_source(Source.create_canine(
        DOGGY_ID,
        ACCT_ID,
        CanineInfo("Doggy")))
    source_repo.create_source(Source.create_environment(
        PLANTY_ID,
        ACCT_ID,
        EnvironmentInfo("Planty", "The green one")))

    doggy = source_repo.get_source(ACCT_ID, DOGGY_ID)
    planty = source_repo.get_source(ACCT_ID, PLANTY_ID)
    all_sources = source_repo.get_sources_in_account(ACCT_ID)
    just_plants = source_repo.get_sources_in_account(ACCT_ID, "environment")

    print("Doggy:")
    print(json.dumps(doggy, default=json_converter, indent=2))

    print("Planty:")
    print(json.dumps(planty, default=json_converter, indent=2))

    print("All:")
    print(json.dumps(all_sources, default=json_converter, indent=2))

    print("Just Plants:")
    print(json.dumps(just_plants, default=json_converter, indent=2))
    t.commit()

with Transaction() as t:
    survey_template_repo = SurveyTemplateRepo(t)
    ids = survey_template_repo.list_survey_ids()
    print(ids)

    the_stuff = survey_template_repo.get_survey_template(ids[0])
    # print(json.dumps(the_stuff.groups[0].questions[10],
    #                  default=json_converter,
    #                  indent=2))

    in_vue = util.vue_adapter.to_vue_schema(the_stuff)
    # print(json.dumps(in_vue, default=json_converter, indent=2))

    with open("surveySchema.json", "w") as outFile:
        outFile.write(json.dumps(in_vue, default=json_converter, indent=2))

with Transaction() as t:
    survey_answers_repo = SurveyAnswersRepo(t)
    survey_ids = survey_answers_repo.list_answered_surveys(
        'd8592c74-7fc4-2135-e040-8a80115d6401',
        'Name - 7O],Gß[1Y1')

    print(survey_ids)

    survey_model = survey_answers_repo.get_answered_survey(
        'd8592c74-7fc4-2135-e040-8a80115d6401',
        survey_ids[0])

    print(survey_model)

    answer_id = survey_answers_repo.submit_answered_survey(
        'd8592c74-7fc4-2135-e040-8a80115d6401',
        "DOGGY!",
        "en_us",
        1,
        survey_model
    )

    survey_model2 = survey_answers_repo.get_answered_survey(
        'd8592c74-7fc4-2135-e040-8a80115d6401',
        answer_id)

    print(survey_model2)
    print(survey_model == survey_model2)

    survey_answers_repo.delete_answered_survey(ACCT_ID, answer_id)

