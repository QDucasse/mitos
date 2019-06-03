    def parse(self, tokens):
        '''
        Main function: launches the parsing operation
        ---
        Args:
        Returns
        '''
        self.tokens = tokens
        #print(self.tokens)
        self.tokens = self.remove_comments()
        self.parse{{main}}()
