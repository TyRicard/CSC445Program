# Name: Ty Ricard
# Student no.: V00909036

class Variable:

    def __init__(self, identifier, point, row, col):
        self.id = identifier
        self.point = point
        self.row = row
        self.col = col
        self.value = None
        self.basis = False if row == -1 else True
        

    def __repr__(self):
        string = "(id: " + str(self.id) + ", row: " + str(self.row) + ", col: " + str(self.col) + ")"
        return string


    def get_id(self):
        return self.id


    def get_row(self):
        return self.row


    def set_row(self, new_row):
        self.row = new_row
    

    def get_col(self):
        return self.col
    

    def set_col(self, new_col):
        self.col = new_col


    def is_in_basis(self):
        return self.basis
    

    def toggle_basis_status(self):
        self.basis = not self.basis


    def is_point(self):
        return self.point

    
    def get_value(self):
        return self.value
    

    def set_value(self, new_value):
        self.value = new_value
 

    def pivot_variable(self, row, col):
        self.set_row(row)
        self.set_col(col)
        self.toggle_basis_status()