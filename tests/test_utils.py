import io
from datetime import date

from services.pdf_service import generate_project_report


class Dummy:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def test_pdf_generation_smoke():
    project = Dummy(name='Demo Project', description='A test project')
    task = Dummy(title='Task 1', status='To Do')
    release = Dummy(version='v1.0', release_date=date.today(), status='Success')
    buf = generate_project_report(project, tasks=[task], releases=[release])
    assert isinstance(buf, io.BytesIO)
    data = buf.getvalue()
    assert data[:4] == b'%PDF'
