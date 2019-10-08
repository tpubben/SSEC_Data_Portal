from django.shortcuts import redirect


def mark_repaired(request, survey_id, leak_id):
    from .models import Deficiency, DeficiencyHistory, SurveyDate
    import datetime

    user = request.user
    survey = SurveyDate.objects.get(pk=survey_id)
    leak = Deficiency.objects.get(pk=leak_id)
    today = datetime.datetime.today()

    leak.deficiency_signoff = user
    leak.deficiency_signoff_date = today
    leak.deficiency_repaired = True
    leak.save()

    DeficiencyHistory.objects.create(surveydate_id_fk=survey, history_leak_id=leak, history_action='Undo Repair',
                                     history_actor=user, history_date=today)

    return redirect('report_view', survey_id=survey_id)


def mark_not_repaired(request, survey_id, leak_id):
    from .models import Deficiency, DeficiencyHistory, SurveyDate
    import datetime
    today = datetime.datetime.today()
    survey = SurveyDate.objects.get(pk=survey_id)
    user = request.user
    leak = Deficiency.objects.get(pk=leak_id)

    DeficiencyHistory.objects.create(surveydate_id_fk=survey, history_leak_id=leak, history_action='Undo Repair',
                                     history_actor=user, history_date=today)

    leak.deficiency_signoff = None
    leak.deficiency_signoff_date = None
    leak.deficiency_repaired = False
    leak.save()

    return redirect('report_view', survey_id=survey_id)
