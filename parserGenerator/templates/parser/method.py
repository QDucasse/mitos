    def parse{{name}}(self):
        self.indentator.indent('Parsing {{name}}')
        {% for exp in expecting %}
            self.expect({{exp}})
        {% endfor %}
        self.indentator.dedent()


