    def parse(self, tokens, remove_comments_whitespace=False):
        '''
        Main function: launches the parsing operation
        ---
        Args:
        Returns
        '''
        self.tokens = tokens
        #print(self.tokens)
        if remove_comments_whitespace:
            self.tokens = self.remove_comments_whitespace()
        else:
            self.tokens = self.remove_comments()
        self.parse{{main}}()
