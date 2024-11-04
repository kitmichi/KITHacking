from database import update_study_schedule


def test_update_study_schedule():
    session = update_study_schedule.update_study_schedule()
    modules = session.query(update_study_schedule.Module).all()
    assert len(modules) != 0
