from femtocrux.femtostack.common import CompilerFrontend


class TFLiteCompiler(CompilerFrontend):
    def __init__(self, *args, **kwargs):
        raise ValueError("TFLiteCompiler deprecated in this release")
