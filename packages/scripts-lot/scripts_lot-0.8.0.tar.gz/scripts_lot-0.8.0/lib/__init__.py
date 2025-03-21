from x1  import get_name as x1
from x2  import get_name as x2
from x3  import get_name as x3
from x4  import get_name as x4



class Script:
    @staticmethod
    def get_ga_text():
        x1()
        x2()
        x3()
        x4()
        return "GA"

    @staticmethod
    def get_kmeans_text():
        return "KMEANS"

