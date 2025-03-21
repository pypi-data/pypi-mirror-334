
class BaseMixin:

    @staticmethod
    def pars_func(param, group, re_pattern):
        result = re_pattern.match(param)
        if result:
            arg = result.group(group)
            return arg