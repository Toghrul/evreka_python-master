from datetime import datetime, timedelta
from django import template
from django.template import Node, TemplateSyntaxError
from evrekaTest.models import Bin, Route, RouteDetailRecord

register = template.Library()


@register.filter(name='float_round2100')
def compute_exact_id(value):
    if value:
        return str(round(value * 100, 2))
    else:
        return "0"


@register.filter(name='float_round1')
def compute_exact_id2(value):
    if value:
        return round(value, 1)
    else:
        return "0"


@register.filter(name='bar_color_full')
def compute_color(value):
    if value > 0.7:
        return 'danger'
    elif value < 0.35:
        return "success"
    else:
        return 'warning'


@register.filter(name='bar_color_batt')
def compute_color(value):
    if value > 0.7:
        return 'success'
    elif value < 0.35:
        return "danger"
    else:
        return 'warning'


@register.simple_tag(name='current_average')
def current_average(value):
    if value == "fullness":
        l = [b.current_record.fullness_rate for b in Bin.objects.all() if b.current_record is not None]
        if not l:
            l = [0.0]
        return round(float(sum(l)) / float(len(l)) * 100, 2)
    elif value == "co2":
        return round(sum([r.co2_emission() for r in Route.objects.all()]) * 100, 2)
    else:
        return 0


@register.simple_tag(name='visited_bins_yesterday')
def visited_bins_yesterday():
    yesterday = (datetime.now() - timedelta(days=1)).date()
    visited_bins = RouteDetailRecord.objects.filter(route__date__startswith=yesterday)

    return visited_bins.count()


@register.simple_tag(name='total_bins')
def total_bins():
    return Bin.objects.all().count()


class CustomNode(Node):
    def __init__(self, variable_name, value):
        self.variable = variable_name
        self.value = value

    def render(self, context):
        context[self.variable] = self.value
        return ''

@register.tag("define_custom_variable")
def define_custom_variable(parser, token):
    """
    Usage::

        {% define_custom_variable as variable True %}

        or

        {% define_custom_variable as variable False %}

    Context'e 'variable' isminde boolean deger inject eder.
    """
    # token.split_contents() isn't useful here because this tag doesn't accept variable as arguments
    args = token.contents.split()
    if len(args) != 4 or args[1] != 'as':
        raise TemplateSyntaxError("'define_custom_variable' requires 'as variable boolean_value' (got %r)" % args)
    return CustomNode(args[2], args[3])