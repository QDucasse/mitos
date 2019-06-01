{# Template to generate a method of the Parser class #}
    def parse{{name}}(self):
        self.indentator.indent('Parsing {{name}}')
        {%set indent={'flag':False}%}{#Global variable to know if indentation is necesary or not#}
        {%- for c in generator %}{#For each element we associate the appropiate method#}
            {%- if indent['flag'] %}    {%endif%}{#Reading of the glogal variable#}
            {%- if c[1]==1 -%}self.expect({{c[0]}})
            {%- elif c[1]==0 -%}self.parse{{c[0]}}()
            {%-elif c=="rep-begin"-%}while():
                {%-if indent.update({'flag':True}) -%}{#Method to update the global variable#}
                {%-endif-%}
            {%-elif c=="opt-begin"-%}if():
                {%-if indent.update({'flag':True}) -%}
                {%-endif-%}
            {%-elif c=="rep-end" or c=="opt-end"-%}
                {%-if indent.update({'flag':False}) -%}
                {%-endif-%}
            {% endif %}
        {% endfor -%}
        self.indentator.dedent()


