from .rule_template import RuleTemplate


class RuleDDF00105(RuleTemplate):
    """
    DDF00105: A scheduled activity/decision instance must only reference an epoch that is defined within the same study design as the scheduled activity/decision instance.

    Applies to: ScheduledActivityInstance, ScheduledDecisionInstance
    Attributes: epoch
    """

    def __init__(self):
        super().__init__(
            "DDF00105",
            RuleTemplate.ERROR,
            "A scheduled activity/decision instance must only reference an epoch that is defined within the same study design as the scheduled activity/decision instance.",
        )

    def validate(self, config: dict) -> bool:
        data = config["data"]
        items = data.instances_by_klass("ScheduledActivityInstance")
        items += data.instances_by_klass("ScheduledDecisionInstance")
        for item in items:
            if "epochId" in item:
                epoch = data.instance_by_id(item["epochId"])
                if epoch:
                    item_parent = data.parent_by_klass(item["id"], "StudyDesign")
                    epoch_parent = data.parent_by_klass(epoch["id"], "StudyDesign")
                    if item_parent["id"] != epoch_parent["id"]:
                        self._add_failure(
                            "Epoch defined in a different study design",
                            item["instanceType"],
                            "epochId",
                            data.path_by_id(item["id"]),
                        )
        return self._result()
