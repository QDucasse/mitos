{# Template to generate a method of the Parser class #}
    def parse{{name}}(self):
        self.indentator.indent('Parsing {{name}}')
        {%set indent={'flag':False,'flag1':False}%}{#Global variable to know if indentation is necesary or not#}
        {%- for i in range(n) %}{#For each element we associate the appropriated method#}
            {%- if indent['flag'] %}    {%endif%}{#Reading of the glogal variable#}
            {%- if indent['flag1'] %}    {%if indent.update({'flag1':False}) %}{%endif%}{%endif%}{#Reading of the glogal variable#}
            {%- if generator[i][1]==1 -%}
            self.expect({{generator[i][0]}})
            {%- elif generator[i][1]==0 -%}
            self.parse{{generator[i][0]}}()
            {%-elif generator[i]=="rep-begin"-%}
                {%- if generator[i+1][1]==1 -%}
            while(self.show_next().kind == {{generator[i+1][0]}}):
                {%- elif generator[i+1][1]==0 -%}
            while(self.test{{generator[i+1][0]}}()):
                {%- elif generator[i+1]=="or-begin" -%}
            while(self.
                    {%- for k in range(i+2,n)-%}
                        {%- if generator[k][1]==0 -%}
                            test{{generator[k][0]}}() or self.
                        {%- elif generator[k][1]==1 -%}
                            show_next().kind == self.except('{{generator[k][0]}}') or 
                        {%- elif generator[k+2]=="or-end"-%}
                            {%- if generator[k+1][1]==0 -%}
                            test{{generator[k+1][0]}}()):
                            {%- elif generator[k+1][1]==1 -%}
                            show_next().kind == self.except('{{generator[k+1][0]}}')):
                            {%-else-%}{{generator[k+1]}}
                            {%-endif-%}
                            {%- break -%}
                        {%-endif-%}
                    {%-endfor-%}
                {%- endif -%}
                {%-if indent.update({'flag':True}) -%}{#Method to update the global variable#}{%-endif-%}
            {%-elif generator[i]=="opt-begin"-%}
                {%- if generator[i+1][1]==1 -%}
            if(self.show_next().kind == {{generator[i+1][0]}}):
                {%- elif generator[i+1][1]==0 -%}
            if(self.test{{generator[i+1][0]}}()):
                {%- elif generator[i+1]=="or-begin" -%}
            if(self.
                    {%- for k in range(i+2,n)-%}
                        {%- if generator[k][1]==0 -%}
                            test{{generator[k][0]}}() or self.
                        {%- elif generator[k][1]==1 -%}
                            show_next().kind == self.except('{{generator[k][0]}}') or 
                        {%- elif generator[k+2]=="or-end"-%}
                            {%- if generator[k+1][1]==0 -%}
                            test{{generator[k+1][0]}}()):
                            {%- elif generator[k+1][1]==1 -%}
                            show_next().kind == self.except('{{generator[k+1][0]}}')):
                            {%-else-%}{{generator[k+1]}}
                            {%-endif-%}
                            {%- break -%}
                        {%-endif-%}
                    {%-endfor-%}
                {%- endif -%}
                {%-if indent.update({'flag':True}) -%}{#Method to update the global variable#}{%-endif-%}
            {%-elif generator[i]=="or-begin"-%}
                {%- if generator[i+1][1]==1 -%}
            if(self.show_next().kind == {{generator[i+1][0]}}):
                {%- elif generator[i+1][1]==0 -%}
            if(self.test{{generator[i+1][0]}}()):
                {%- endif -%}
                {%-if indent.update({'flag1':True}) -%}
                {%-endif-%}
            {%-elif generator[i]=="or"-%}
                {%-if indent.update({'flag1':True}) -%}
                {%-endif-%}
                {%- if generator[i+1][1]==1 -%}
            elif(self.show_next().kind == {{generator[i+1][0]}}):
                {%- elif generator[i+1][1]==0 -%}
            elif(self.test{{generator[i+1][0]}}()):
                {%-endif-%}
            {%-elif generator[i]=="rep-end" or generator[i]=="opt-end" or generator[i]=="end"-%}
                {%-if indent.update({'flag':False}) -%}
                {%-endif-%}
            {%- endif %}
        {% endfor -%}
        self.indentator.dedent()


