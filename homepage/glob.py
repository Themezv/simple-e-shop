def globalTemplateVariable(request):
    if request.is_ajax():
        extended_template = "homepage/base_ajax.html"
    else:
        extended_template = "homepage/base.html"
    return {"extended_template": extended_template}