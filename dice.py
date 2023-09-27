class Dice:
    def __init__(
        self,
        username,
        password,
        keywords,
        blacklist,
        resume,
        cache_path,
        wait_s,
        postedDate="THREE",
        location="",
    ):
        self.username = username
        self.password = password
        self.keywords = keywords
        self.blacklist = blacklist
        self.resume = resume
        self.cache_path = cache_path
        self.wait_s = wait_s
        self.postedDate = postedDate
        self.location = location


# Create Dice Object Here
diceObject = Dice(
    username="",
    password="",
    keywords="SPRINGBOOT",
    blacklist="",
    resume="",  # absolute path to your resume
    cache_path="",  # CAN BE BLANK. cached_data path is auto generated
    wait_s=10,
    location="",  # CAN BE BLANK
    postedDate="THREE",  # ONE, THREE, ANY
)
