class Idol_struct:
    def __init__ (self, idol_values):
        self.link, self.source_id, self.name, self.shared_key, self.rowid = idol_values
        self.matched = -1
        self.matched_total = 0
        self.best_match = []
    def to_tuple(self):
        return (self.link, self.source_id, self.name, self.shared_key, self.rowid)
    def __str__(self):
        return f"Idol: {self.name}({self.shared_key}) src: {self.source_id}"
    
