from .rule_template import RuleTemplate


class RuleDDF00106(RuleTemplate):
    """
    DDF00106: A scheduled activity instance must only reference an encounter that is defined within the same study design as the scheduled activity instance.

    Applies to: ScheduledActivityInstance
    Attributes: encounter
    """

    def __init__(self):
        super().__init__(
            "DDF00106",
            RuleTemplate.ERROR,
            "A scheduled activity instance must only reference an encounter that is defined within the same study design as the scheduled activity instance.",
        )

    def validate(self, config: dict) -> bool:
        data = config["data"]
        items = data.instances_by_klass("ScheduledActivityInstance")
        for item in items:
            if "encounterId" in item:
                encounter = data.instance_by_id(item["encounterId"])
                if encounter:
                    item_parent = data.parent_by_klass(item["id"], "StudyDesign")
                    encounter_parent = data.parent_by_klass(
                        encounter["id"], "StudyDesign"
                    )
                    if item_parent["id"] != encounter_parent["id"]:
                        self._add_failure(
                            "Encounter defined in a different study design",
                            item["instanceType"],
                            "encounterId",
                            data.path_by_id(item["id"]),
                        )
        return self._result()
