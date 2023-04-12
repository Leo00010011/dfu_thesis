from report.template import ReportTemplate


def pipeline(patient, p, a, v):
    template = ReportTemplate()
    template.add_patient(**patient)
    template.add_measurement(p, a, v, patient['datetime'])
    path = 'output/reports/'
    date = f"{patient['real_date'].day}-{patient['real_date'].month}-{patient['real_date'].year}"
    name = '_'.join([patient['name'],str(patient['age']),date])
    final_name = f'{path}{name}.pdf'
    template.output(final_name, 'F')

    