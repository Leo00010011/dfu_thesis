from report.template import ReportTemplate


def pipeline(patient, p, a, v):
    template = ReportTemplate()
    template.add_patient(**patient)
    template.add_measurement(p, a, v, patient['datetime'])
    print(template.buffer)
    template.output(f"./output/reports/{''.join(list(map(lambda x: x[0], patient['name'].split())))}-{patient['age']}-{patient['sex']}-{'-'.join(patient['datetime'].split('/'))}.pdf", "")