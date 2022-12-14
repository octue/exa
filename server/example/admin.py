from django.contrib import admin
from django_twined.admin import QuestionAdmin

from .models import FooFightingQuestion, FooFightingTest


class FooFightingTestAdmin(admin.ModelAdmin):
    search_fields = ["id", "notes"]
    list_display = ("id", "created", "number_of_questions", "max_duration", "randomise_duration")
    list_filter = ("created", "number_of_questions", "max_duration", "randomise_duration")
    actions = ["launch_ask_questions"]
    date_hierarchy = "created"

    def launch_ask_questions(self, request, queryset):
        """Overridden from superclass to dispatch question via a queue"""
        from .tasks import FooFightingTestTask  # noqa: F401, pylint: disable=import-outside-toplevel

        rows_updated = queryset.count()
        for test in queryset.all():
            FooFightingTestTask().enqueue(foo_fighting_test_id=str(test.id))

        if rows_updated == 1:
            message_bit = "1 test was"
        else:
            message_bit = f"{rows_updated} tests were"
        self.message_user(request, f"{message_bit} enqueued")

    launch_ask_questions.short_description = "Launch run for selected test(s)"


class FooFightingQuestionAdmin(QuestionAdmin):
    search_fields = ["id", "service_revision__name", "foo_fighting_test__id", "foo_fighting_test__notes"]
    list_display = ("id", "created", "asked", "answered", "calculation_status")
    list_select_related = ("foo_fighting_test",)
    list_filter = (
        "asked",
        "calculation_status",
        "service_revision__name",
        "service_revision__tag",
    )
    date_hierarchy = "created"
    readonly_fields = (
        "answered",
        "asked",
        "calculation_status",
        "created",
        "id",
        "log_records",
        "monitor_messages",
        "result",
        "delivery_acknowledgement",
        "latest_heartbeat",
        "exceptions",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "service_revision",
                    "foo_fighting_test",
                    "asked",
                    "answered",
                    "created",
                    "calculation_status",
                    "latest_heartbeat",
                )
            },
        ),
        ("Delivery Acknowledgement", {"classes": ("collapse",), "fields": ("delivery_acknowledgement",)}),
        ("Log Records", {"classes": ("collapse",), "fields": ("log_records",)}),
        ("Monitor Messages", {"classes": ("collapse",), "fields": ("monitor_messages",)}),
        ("Result", {"classes": ("collapse",), "fields": ("result",)}),
        ("Exceptions", {"classes": ("collapse",), "fields": ("exceptions",)}),
    )

    # TODO these staticmethods should be part of the QuestionAdmin mixin
    @staticmethod
    def delivery_acknowledgement(obj):
        """Show the delivery acknowledgement entry"""
        return obj.delivery_acknowledgement.data

    @staticmethod
    def exceptions(obj):
        """Show concatenated series of exceptions"""
        return [event.data for event in obj.exceptions]

    @staticmethod
    def latest_heartbeat(obj):
        return obj.latest_heartbeat.data

    @staticmethod
    def log_records(obj):
        """Show concatenated series of log records"""
        logstream = ""
        for event in obj.log_records:
            record = event.data["log_record"]
            logstream += f"{record['levelname']} {record['filename']}:{record['lineno']} {record['msg']}\n"
        return logstream

    @staticmethod
    def monitor_messages(obj):
        """Show concatenated series of monitor_messages"""
        return [event.data for event in obj.monitor_messages]

    @staticmethod
    def result(obj):
        """Show concatenated series of monitor_messages"""
        return obj.result.data

    def has_add_permission(self, request, obj=None):
        """Prevent people from adding questions directly (they're created by the test runs)"""
        return False

    def has_change_permission(self, request, obj=None):
        """Prevent people from changing questions after they've been asked"""
        return self._question_is_not_asked(obj)


admin.site.register(FooFightingTest, FooFightingTestAdmin)
admin.site.register(FooFightingQuestion, FooFightingQuestionAdmin)
