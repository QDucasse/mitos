{# Template to generate a test method of the Parser class #}
    def test{{name}}(self):
        next=self.show_next().kind
        testing_list={{string_list}}
        test=(next in testing_list)
        {%- for d in dependance_list -%}{#For each element we call the appropriated test method#}
        test=(test or self.test{{d}}()) 
        {%- endfor %}
        return(test)


