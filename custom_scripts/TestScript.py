from extras.scripts import Script


class TestScript(Script):
    class Meta:
        name = "Test"

    def run(self, data, commit):
        self.log_success("It works")
        return "OK"
