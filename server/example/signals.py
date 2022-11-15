import logging
from django.dispatch import receiver
from django_twined.models import ServiceUsageEvent
from django_twined.signals import exception_received, result_received
from example.models import ERROR_STATUS, SUCCESS_STATUS


logger = logging.getLogger(__name__)


@receiver(exception_received, sender=ServiceUsageEvent)
def update_question_status(_, service_usage_event, **__):
    """Update Question status when an exception is received"""
    logger.info("Exception received for question %s", service_usage_event.question_id)
    question = service_usage_event.question.as_subclass()
    question.calculation_status = ERROR_STATUS
    question.save()


@receiver(result_received, sender=ServiceUsageEvent)
def update_question_output_values(_, service_usage_event, **__):
    """Update Question status when a result is received"""
    logger.info("Result received for question %s", service_usage_event.question_id)
    question = service_usage_event.question.as_subclass()
    question.calculation_status = SUCCESS_STATUS
    question.save()
