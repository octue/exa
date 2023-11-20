import logging
from django.db import models
from django_twined.models import Question, ServiceUsageEvent, get_default_service_revision
from octue.resources import Manifest


logger = logging.getLogger(__name__)


NO_STATUS = -100
BAD_INPUT_STATUS = -3
TIMEOUT_STATUS = -2
ERROR_STATUS = -1
IN_PROGRESS_STATUS = 0
SUCCESS_STATUS = 1

STATUS_CODE_MESSAGE_MAP = {
    NO_STATUS: "No status",
    BAD_INPUT_STATUS: "Failed (invalid inputs)",
    TIMEOUT_STATUS: "Failed (timeout)",
    ERROR_STATUS: "Failed (error)",
    IN_PROGRESS_STATUS: "In progress",
    SUCCESS_STATUS: "Complete",
}

STATUS_CODE_CHOICES = tuple((k, v) for k, v in STATUS_CODE_MESSAGE_MAP.items())


class FooFightingTest(models.Model):
    created = models.DateTimeField(editable=False, auto_now_add=True)
    number_of_questions = models.IntegerField(
        blank=False,
        null=False,
        help_text="The number of questions that will get created and sent to the foo-fighting service.",
    )
    max_duration = models.IntegerField(
        blank=False, null=False, help_text="The duration of calculation in seconds that each service will run for."
    )
    randomise_duration = models.BooleanField(
        default=False,
        help_text="Randomise durations of calculation if True. If False, all calculations will run for max_durations seconds.",
    )
    notes = models.TextField(blank=True, null=True)


class FooFightingQuestion(Question):
    """Questions made to the FooFighting service (which analyses the fighting of foos"""

    created = models.DateTimeField(editable=False, auto_now_add=True)

    calculation_status = models.IntegerField(default=-100, choices=STATUS_CODE_CHOICES)

    foo_fighting_test = models.ForeignKey(
        FooFightingTest, null=False, on_delete=models.CASCADE, related_name="foo_fighting_questions"
    )

    # TODO the following properties should be placed in a mixin in django_twined!!!

    @property
    def calculation_status_message(self):
        """Short verbose (human-readable, for display) text indicating status of the question"""
        return STATUS_CODE_MESSAGE_MAP[self.calculation_status]

    @property
    def delivery_acknowledgement(self):
        """Returns a ServiceUsageEvent of type 'delivery_acknowledgement' for this question

        Will return None if delivery is not yet acked, or warn on multiple events received whilst returning the first.
        """
        try:
            return self.service_usage_events.get(data__type="delivery_acknowledgement")
        except ServiceUsageEvent.DoesNotExist:
            return None
        except ServiceUsageEvent.MultipleObjectsReturned:
            logger.warning(
                "MultipleObjectsReturned detected for delivery_acknowledgement ServiceUsageEvent on question %s",
                self.id,
            )
            return self.service_usage_events.filter(data__type="delivery_acknowledgement").first()

    @property
    def exceptions(self):
        """Return a queryset of all ServiceUsageEvents of type 'exception' for this question"""
        return self.service_usage_events.order_by("publish_time").filter(data__type="exception").all()

    @property
    def result(self):
        """Returns a ServiceUsageEvent of type 'result' for this question

        Will return None if delivery is not yet acked, or warn on multiple 'result' events received whilst returning the first.
        """
        try:
            return self.service_usage_events.get(data__type="result")
        except ServiceUsageEvent.DoesNotExist:
            return None
        except ServiceUsageEvent.MultipleObjectsReturned:
            logger.warning(
                "MultipleObjectsReturned detected for result ServiceUsageEvent on question %s",
                self.id,
            )
            return self.service_usage_events.filter(data__type="result").first()

    @property
    def log_records(self):
        """Return a queryset of all ServiceUsageEvents of type 'log_record' for this question"""
        return self.service_usage_events.order_by("publish_time").filter(data__type="log_record").all()

    @property
    def monitor_messages(self):
        """Return a queryset of all ServiceUsageEvents of type 'monitor_message' for this question"""
        return self.service_usage_events.order_by("publish_time").filter(data__type="monitor_message").all()

    @property
    def latest_heartbeat(self):
        """Return the latest ServiceUsageEvent of type 'heartbeat'"""
        return self.service_usage_events.order_by("-publish_time").filter(data__type="heartbeat").first()

    class Meta:
        """Metaclass defining default ordering for FooFighterQuestions"""

        ordering = ["-created"]

    def __str__(self):
        return f"{str(self.id)[:8]}"

    def ask(self, save=True):
        """Ask a question to a service_revision.
        Overridden from django_twined to save the service revision used to ask the question.
        :param boolean save: If true, this question will be saved in order to update the 'asked' time and 'service_revision'
        """
        subscription, push_url, service_revision = super().ask(save=False)
        self.service_revision = service_revision
        if save:
            self.save()

        return subscription, push_url, service_revision

    def get_input_values(self):
        """Prepare and return input_values for the question"""
        return {
            "max_duration": int(self.foo_fighting_test.max_duration),
            "randomise_duration": self.foo_fighting_test.randomise_duration,
            "test_id": str(self.foo_fighting_test.id),
        }

    def get_input_manifest(self):
        """Return no input manifest for the question."""
        return None

    def get_service_revision(self):
        """If no service revision is set, then simply use the default, otherwise use the specified version"""
        if getattr(self, "service_revision", None) is None:
            return get_default_service_revision("octue", "exa-foo-fighting-service")
        return self.service_revision
