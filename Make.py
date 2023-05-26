from PropEnv import PropEnv


class Make():

    def __init__(self):
        pass

    def default_env_file(self, path):
        propEnv = self.default_env()
        propEnv.save_json(path)


    def default_light_source_file(self, path):
        lightSource = self.default_light_source()
        lightSource.save_json(path)


    def default_prop_setup_file(self, path):
        propSetup = self.default_prop_setup()
        propSetup.save_json(path)


    def default_env(self):
        propEnv = PropEnv()
        propEnv.fill_cube(fill=1, start_p=[0, 0, 0], end_p=[1.0, 1.0, 0.25])
        return propEnv


    def default_light_source(self):
        raise NotImplementedError()


    def default_prop_setup(self):
        raise NotImplementedError()














