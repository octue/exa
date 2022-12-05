import logging
from django_gcp.tasks import OnDemandTask
from example.models import ERROR_STATUS, IN_PROGRESS_STATUS, FooFightingQuestion, FooFightingTest


logger = logging.getLogger(__name__)


class FooFightingTestTask(OnDemandTask):
    """An on-demand task to prepare and ask a question to foo-fighting-service

    This process is done in an async task, rather than immediately in a request,
    because it can take several seconds to create the resources required for the question
    """

    def enqueue(self, *args, **kwargs):
        print("FFS HERE")
        returned = super().enqueue(*args, **kwargs)
        print("RET", returned)

    def run(self, foo_fighting_test_id=None, **__):
        """Run a series of FooFightingQuestions to load test the hardware

        Question results should contain:
         - The number of iterations of the mandelbrot calculation completed in the duration of the question
         - The duration of the questions, which will be equal to `max_duration` if `randomise_duration` is false, otherwise will be `0 <= duration <= max_duration`

        :param int foo_fighting_test_id: The id of the test run
        :param int number_of_questions: The number of questions that will get created and sent to the foo-fighting service.
        :param int max_duration: The duration of calculation in seconds that each service will run for.
        :param bool randomise_duration: Randomise durations of calculation if True. If False, all calculations will run for max_durations seconds.
        :param int mandelbrot_array_size: The dimension of the mandelbrot array that will be calculated.
        """

        test = FooFightingTest.objects.get(id=foo_fighting_test_id)

        for idx in range(test.number_of_questions):
            logger.info("Creating question %s of %s for FooFightingTest %s", idx + 1, test.number_of_questions, test.id)

            question = FooFightingQuestion(foo_fighting_test=test, calculation_status=IN_PROGRESS_STATUS)
            question.save()

            try:
                logger.info("Running FooFightingQuestionTask with question_id=%s", question.id)
                question.ask()
            except Exception as e:
                question.calculation_status = ERROR_STATUS
                question.save()
                raise e
